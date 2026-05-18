from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker
import uuid
from sqlalchemy import select
from sqlalchemy.orm.attributes import flag_modified
import asyncio

from app.config import settings
from app.db.database import async_session_maker
from app.db.models import Project
from app.services.s3 import download_file_from_s3
from app.services.pdf_parser import extract_text_from_pdf
from app.ai.analyzer import analyze_gdd


broker = RabbitBroker(settings.rabbitmq_url)
app = FastStream(broker)


@broker.subscriber("gdd_analysis_queue")
async def handle_gdd_analysis(
    project_id_str: str,
    logger: Logger
):
    project_id = uuid.UUID(project_id_str)

    async with async_session_maker() as session:
        query = select(Project).where(Project.id == project_id)
        response = await session.execute(query)
        project = response.scalar_one_or_none()

        if not project or not project.gdd_file_key:
            return
        
        db_lock = asyncio.Lock()

        async def update_progress(agent_name: str, status: str):
            async with db_lock:
                await session.refresh(project)

                if project.thought_process is None:
                     project.thought_process = {}

                project.thought_process[agent_name] = {"status": status}
                flag_modified(project, "thought_process")
                await session.commit()
        
        try:
            file_bytes = await download_file_from_s3(project.gdd_file_key)
            text = await extract_text_from_pdf(file_bytes)

            analyze_gdd_result = await analyze_gdd(text, logger, update_progress)
            logger.info(str(analyze_gdd_result))
            project.report_data = analyze_gdd_result
            await session.commit()

        except Exception as e:
                project.report_data = {"error": str(e)}
                logger.exception(f"error in worker.py! \n")
                await session.commit()
