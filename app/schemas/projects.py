from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime


class ProjectResponse(BaseModel):
    id: uuid.UUID
    title: str
    gdd_file_key: Optional[str]
    gdd_url: Optional[str] = None
    report_data: Optional[dict] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)
