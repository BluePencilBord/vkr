from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.db.database import get_async_session
from app.db.models import Project, User
from app.schemas.projects import ProjectResponse
from app.services.s3 import upload_file_to_s3, get_presigned_url
from app.api.dependencies import get_current_user
from app.worker import broker


router = APIRouter()


async def upload_to_s3(file: UploadFile, project_id: uuid.UUID) -> str:
    pass


@router.post("/upload_gdd", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def upload_gdd(
    title: str = Form(...),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    allowed_extensions = ["pdf", "docx"]
    file_ext = file.filename.split(".")[-1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Неподдерживаемый формат. Загрузите PDF или DOCX"
        )
    
    new_project = Project(
        user_id = current_user.id,
        title = title
    )

    session.add(new_project)
    await session.flush()

    try:
        file_bytes = await file.read()

        s3_file_key = f"uploads/{new_project.id}.{file_ext}"

        await upload_file_to_s3(
            file_bytes = file_bytes,
            file_name = s3_file_key,
            content_type = file.content_type
        )
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code = 500, detail = f"Ошибка загрузки в S3: {str(e)}")
    
    new_project.gdd_file_key = s3_file_key
    await session.commit()
    await session.refresh(new_project)

    return new_project


@router.get("/projects", response_model=list[ProjectResponse])
async def get_user_projects(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(Project).where(Project.user_id == current_user.id)
    result = await session.execute(query)
    projects = result.scalars().all()

    projects_response = []

    for proj in projects:
        proj_data = ProjectResponse.model_validate(proj)

        if proj.gdd_file_key:
            proj_data.gdd_url = await get_presigned_url(proj.gdd_file_key)
        
        projects_response.append(proj_data)

    return projects_response


@router.post("/{project_id}/analyze", status_code=status.HTTP_202_ACCEPTED)
async def start_analysis(
    project_id: uuid.UUID,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
):
    query = select(Project).where(Project.id == project_id, Project.user_id == current_user.id)
    response = await session.execute(query)
    project = response.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Проект не найден"
        )

    await broker.publish(str(project.id), queue="gdd_analysis_queue")

    return {"message": "Анализ документа запущен"}
