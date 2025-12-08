from pydantic import BaseModel, Field
from typing import Optional

class Event(BaseModel):
    # Required fields
    id: str
    image_path: str
    raw_ocr_text: Optional[str] = None
    extracted_at: str
    
    # Core event info (at least name should be present)
    name: str = Field(description="Event name or title")
    
    # Optional fields (normalized)
    date: Optional[str] = Field(None, description="Event date in YYYY-MM-DD format or text like 'Mondays in December'")
    time: Optional[str] = Field(None, description="Event time (e.g., '9am-2pm', '6:30-7:30 PM')")
    
    # Location fields
    location: Optional[str] = Field(None, description="Venue or location name")
    address: Optional[str] = Field(None, description="Full street address with city, state, zip")
    
    # Details
    description: Optional[str] = Field(None, description="Event description or details")
    
    # Contact & registration
    contact: Optional[str] = Field(None, description="Phone number or email")
    links: list[str] = Field(default_factory=list, description="URLs for registration, info, etc.")
    
    # Pricing (optional)
    price: Optional[str] = Field(None, description="Price or pricing tiers")
    
    # Additional info
    organization: Optional[str] = Field(None, description="Organizing entity")