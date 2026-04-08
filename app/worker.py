from faststream import FastStream
from faststream.rabbit import RabbitBroker
import uuid
from sqlalchemy import select

from app.config import settings
from app.db.database import async_session_maker
from app.db.models import Project
from app.services.s3 import download_file_from_s3
from app.services.pdf_parser import extract_text_from_pdf
from app.ai.analyzer import analyze_gdd


broker = RabbitBroker(settings.rabbitmq_url)
app = FastStream(broker)


@broker.subscriber("gdd_analysis_queue")
async def handle_gdd_analysis(project_id_str: str):
    project_id = uuid.UUID(project_id_str)

    async with async_session_maker() as session:
        query = select(Project).where(Project.id == project_id)
        response = await session.execute(query)
        project = response.scalar_one_or_none()

        if not project or not project.gdd_file_key:
            return
        
        try:
            file_bytes = await download_file_from_s3(project.gdd_file_key)
            text = await extract_text_from_pdf(file_bytes)

            project.report_data = await analyze_gdd(text)
            await session.commit()

        except Exception as e:
            Project.report_data = {"error": str(e)}
            await session.commit()

