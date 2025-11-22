from pydantic import BaseModel, Field
from datetime import datetime

class Event(BaseModel):
    id: str = Field(..., description="Unique identifier for the event")
    name: str = Field(None, description="Name of the event")
    description: str = Field(None, description="Detailed description of the event")
    date: datetime = Field(None, description="Date of the event")
    time: str = Field(None, description="Time of the event")
    location: str = Field(None, description="Location where the event will take place")
    address: str = Field(None, description="Address of the event location")
    links: list[str] = Field(default_factory=list, description="List of related links for the event")
    contact: str = Field(None, description="Contact email or phone number for event inquiries")
    raw_ocr_text: str = Field(None, description="Raw OCR text associated with the event")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the event was extracted")
    