from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker
import uuid
from sqlalchemy import select
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
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                file_bytes = await download_file_from_s3(project.gdd_file_key)
                text = await extract_text_from_pdf(file_bytes)

                analyze_gdd_result = await analyze_gdd(text, logger)
                logger.info(str(analyze_gdd_result))
                project.report_data = analyze_gdd_result
                await session.commit()

            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    logger.warning(f"Поймали 429 лимит. Ждем 15 секунд... (Попытка {attempt + 1})")
                    await asyncio.sleep(15) # Ждем, пока сервера остынут
                else:
                    project.report_data = {"error": str(e)}
                    logger.exception(f"error in worker.py! \n")
                    await session.commit()
