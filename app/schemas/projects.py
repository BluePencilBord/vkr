from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
import uuid
from datetime import datetime


class ProjectResponse(BaseModel):
    id: uuid.UUID
    title: str
    gdd_file_key: Optional[str]
    gdd_url: Optional[str] = None
    thought_process: Optional[Dict[str, Any]] = None
    report_data: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes = True)
