from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from .models import BookStatus

class BookBase(BaseModel):
    title: str = Field(..., description="The title of the book")
    description: str = Field(..., description="Brief description of the book")
    genre: str = Field(..., description="Book genre (e.g., Fantasy, Mystery)")
    target_audience: str = Field(..., description="Target audience (e.g., Young Adult, Adult)")
    style: str = Field(..., description="Writing style (e.g., Descriptive, Concise)")
    tone: str = Field(..., description="Narrative tone (e.g., Humorous, Serious)")
    length: str = Field(..., description="Book length (e.g., Novel, Novella)")

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    status: BookStatus
    content: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class GenerationRequest(BookBase):
    additional_instructions: Optional[str] = Field(None, description="Additional instructions for generation")
    creativity_level: float = Field(0.7, ge=0.0, le=1.0, description="Level of creativity (0.0 to 1.0)")
    quality_threshold: float = Field(9.8, ge=0.0, le=10.0, description="Minimum quality threshold (0.0 to 10.0)")

class GenerationMetadata(BaseModel):
    timestamp: datetime
    version: str
    quality_metrics: Dict[str, Any]

class GenerationResponse(BaseModel):
    content: Dict[str, Any]
    metadata: GenerationMetadata

    class Config:
        from_attributes = True