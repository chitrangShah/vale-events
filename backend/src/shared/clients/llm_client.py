"""
LLM Client for extracting event data directly from images.
Uses Ollama with llama3.2-vision model.
"""

from pathlib import Path
import ollama
import json
from src.shared.models import Event
from datetime import datetime
from typing import Optional


class LLMClient:
    """
    Extracts event information directly from images using Ollama vision model.
    """
    
    def __init__(self, model_name: str = "llama3.2-vision"):
        """
        Initialize LLM client.
        
        Args:
            model_name: Ollama vision model name
        """
        self.model_name = model_name
    
    def parse_event_from_image(self, image_path: str) -> Event:
        """
        Extract event info directly from image using vision model.
        
        Args:
            image_path: Path to event flyer image
            
        Returns:
            Event object
        """
        # Build prompt
        prompt = self.build_prompt()
        
        try:
            # Call Ollama with image
            response = self.call_ollama_vision(prompt, image_path)
            
            # Validate response
            if not response or not response.strip():
                raise Exception("LLM returned empty response")
            
            # Extract JSON
            json_text = self.extract_json(response)
            
            if not json_text or not json_text.strip():
                print(f"Error: No JSON found in response")
                print(f"Raw response: {response[:300]}")
                raise Exception("No JSON found in LLM response")
            
            # Parse JSON
            try:
                data = json.loads(json_text)
            except json.JSONDecodeError as e:
                print(f"JSON parse error: {str(e)}")
                print(f"JSON text: {json_text[:300]}")
                
                print(f"JSON failed, using fallback parser...")
                data = self.parse_fallback_json(json_text)
            
            # Create event
            event = self.create_event(data, image_path)
            
            return event
        
        except Exception as error:
            raise Exception(f"Vision extraction failed: {str(error)}")
    
    def build_prompt(self) -> str:
        current_date = datetime.now()
        current_year = current_date.year
        
        prompt = f"""Extract event information from this flyer image.

        TODAY: {current_date.strftime('%Y-%m-%d')}

        RULES:
        - Date format: YYYY-MM-DD
        - If no year shown, use {current_year}
        - Ignore "EST" or "SINCE" years (those are business founding dates)
        - "STARTS [date]" means use that date
        - "[MONTH] [DAY]-[TIME]" like "December 6-2PM" means date is [MONTH] [DAY], time is [TIME]
        - "DOORS [time] / CONCERT [time]" means time range from doors to 3 hours after doors

        YOU MUST RESPOND WITH ONLY THIS JSON FORMAT - NO OTHER TEXT:
        {{"name": "event name", "organization": "host", "date": "YYYY-MM-DD", "time": "time range", "location": "venue", "address": "street address or null", "contact": "phone/email or null", "price": "cost or null"}}

        JSON:"""
    
        return prompt
    
    def call_ollama_vision(self, prompt: str, image_path: str) -> str:
        """
        Call Ollama vision API with image.
        
        Args:
            prompt: Prompt to send
            image_path: Path to image file
            
        Returns:
            Response text
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [image_path]
                }],
                options={
                    'temperature': 0.0,
                    'top_p': 0.1,
                    'top_k': 1,
                    'seed': 42,
                    'num_predict': 512
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            raise Exception(f"Ollama vision API error: {str(e)}")
    
    def extract_json(self, response: str) -> str:
        """
        Extract JSON from response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Clean JSON string
        """
        text = response.strip()
        
        # Handle markdown code blocks
        if '```' in text:
            parts = text.split('```')
            for part in parts:
                part = part.strip()
                if part.startswith('json'):
                    part = part[4:].strip()
                if part.startswith('{') and part.endswith('}'):
                    return part
        
        # Find JSON object in text
        start = text.find('{')
        end = text.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            return text[start:end+1]
        
        return text
    
    def create_event(self, data: dict, image_path: str) -> Event:
        """
        Create Event object from parsed data.
        
        Args:
            data: Parsed JSON
            image_path: Original image path
            
        Returns:
            Event object
        """
        name = self.get_name(data)
        
        # We need adjust date for flyers that omit year and explicitly use current year
        # Fix for new year events like "2026 New Year's Eve" on Dec 31 = Dec 31, 2025
        date = self.fix_year(self.clean(data.get('date')), name)
        
        return Event(
            id=Path(image_path).stem,
            name=name,
            organization=self.clean(data.get('organization')),
            date=date,
            time=self.clean(data.get('time')),
            location=self.clean(data.get('location')),
            address=self.clean(data.get('address')),
            description=self.clean(data.get('description')),
            contact=self.clean(data.get('contact')),
            price=self.clean(data.get('price')),
            links=[],
            image_path=image_path,
            raw_ocr_text="[Extracted via vision model]",
            extracted_at=datetime.now().isoformat()
        )
    
    def get_name(self, data: dict) -> str:
        """
        Get event name with validation.
        """
        name = data.get('name', '').strip()
        
        if not name or name.lower() in ['null', 'none']:
            name = 'Unknown Event'
        
        if len(name) > 100:
            name = name[:80].strip()
        
        return name
    
    def clean(self, value) -> Optional[str]:
        """
        Clean string value.
        """
        if value is None:
            return None
        
        text = str(value).strip()
        
        if text.lower() in ['null', 'none', 'n/a', '']:
            return None
        
        return text
    
    def fix_date(self, date_str: Optional[str]) -> Optional[str]:
        """
        Adjust date string to include year if missing.
        If year is not next year or missing, assume current year.
        Args:
            date_str: Original date string
        Returns:
            Adjusted date string
        """
        if date_str is None:
            return None
        
        try:
            current_year = datetime.now().year
            year = int(date_str[:4]) # Extract year
            
            # Append current year if missing or less than current year
            if year < current_year or not year:
                date_str = f"{current_year}{date_str[4:]}"

            return date_str
        except (ValueError, IndexError):        
            return date_str
        
    def parse_fallback_json(self, response: str) -> dict:
        """Parse non-JSON response (markdown, plain text)."""
        data = {}
        current_year = datetime.now().year
        
        lines = response.replace('*', '').split('\n')
        
        for line in lines:
            if ':' not in line:
                continue
        
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()
        
            if not value:
                continue
        
            if 'name' in key and 'event' in key:
                data['name'] = value
            elif 'host' in key or 'organization' in key:
                data['organization'] = value
            elif key == 'date':
                data['date'] = self.parse_date_text(value, current_year)
            elif key == 'time':
                data['time'] = value
            elif 'location' in key:
                data['location'] = value
            elif 'address' in key:
                data['address'] = value
            elif 'contact' in key:
                data['contact'] = value
            elif 'price' in key:
                data['price'] = value if value.lower() != 'free' else 'Free'
    
        if not data.get('name'):
            raise Exception("Could not extract event name")
        
        return data

    def parse_date_text(self, date_text: str, current_year: int) -> str:
        """Convert 'Sunday, December 7th' to 'YYYY-MM-DD'."""
        months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }
        
        lower = date_text.lower()
        
        for month_name, month_num in months.items():
            if month_name in lower:
                # Extract day number
                for word in lower.replace(',', ' ').split():
                    digits = ''.join(c for c in word if c.isdigit())
                    if digits:
                        day = int(digits)
                        return f"{current_year}-{month_num:02d}-{day:02d}"
    
        return None
    
    def fix_year(self, date_str: Optional[str], event_name: str = "") -> Optional[str]:
        """
        Fix obviously wrong years.
        Special case: New Year's Eve 2026 = Dec 31, 2025
        """
        if not date_str:
            return None
    
        try:
            current_year = datetime.now().year
            year = int(date_str[:4])
            month = int(date_str[5:7])
            day = int(date_str[8:10])
            
            # New Year's Eve special case
            # "2026 New Year's Eve" on Dec 31 = Dec 31, 2025
            name_lower = event_name.lower()
            if month == 12 and day == 31 and 'new year' in name_lower:
                # Year on flyer is the year being celebrated, not event date
                return f"{year - 1}-12-31"
            
            # Standard fix: if year is in past or too far future, use current year
            if year < current_year or year > current_year + 1:
                return f"{current_year}{date_str[4:]}"
            
            return date_str
            
        except (ValueError, IndexError):
            return date_str