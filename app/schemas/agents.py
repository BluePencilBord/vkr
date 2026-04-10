from pydantic import BaseModel
from typing import Optional


class GDDChunks(BaseModel):
    narrative_chunk: Optional[str]
    core_mechanics_chunk: Optional[str]
    economy_monetization_chunk: Optional[str]
    market_analyst_chunk: Optional[str]
    technical_producer_chunk: Optional[str]


class RouterOutput(BaseModel):
    is_valid_gdd: bool
    error_message: Optional[str]
    chunks: Optional[GDDChunks]
    