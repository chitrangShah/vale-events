from pydantic import BaseModel, Field
from datetime import datetime

class Event(BaseModel):
    id: str | None = None
    name: str
    time: str | None = None
    location: str | None = None
    address: str | None = None
    description: str | None = None
    links: list[str] = Field(default_factory=list)
    contact: str | None = None
    image_path: str
    raw_ocr_text: str | None = None
    extracted_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    