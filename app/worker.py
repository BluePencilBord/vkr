from faststream import FastStream, Logger
from faststream.rabbit import RabbitBroker
import uuid
from sqlalchemy import select, update
import asyncio
import json

from app.config import settings
from app.db.database import async_session_maker
from app.db.models import Project
from app.services.s3 import download_file_from_s3
from app.services.document_parser import extract_text_from_document
from app.ai.analyzer import analyze_gdd
from app.db.redis import redis_client

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
        gdd_file_key = project.gdd_file_key

    async def update_progress(agent_name: str, status: str):
        redis_key = f"project:{project_id}:progress"

        await redis_client.hset(redis_key, agent_name, status)
        await redis_client.expire(redis_key, 7200)
    
    try:
        file_bytes = await download_file_from_s3(gdd_file_key)
        text = await extract_text_from_document(file_bytes, gdd_file_key)

        analyze_gdd_result = await analyze_gdd(text, logger, update_progress)
        
        async with async_session_maker() as session:
            await session.execute(
                update(Project)
                .where(Project.id == project_id)
                .values(report_data=str(analyze_gdd_result))
            )
            await session.commit()
            
    except Exception as e:
        logger.exception("error in worker.py!")
        async with async_session_maker() as session:
            await session.execute(
                update(Project)
                .where(Project.id == project_id)
                .values(report_data=f"Ошибка: {str(e)}")
            )
            await session.commit()
