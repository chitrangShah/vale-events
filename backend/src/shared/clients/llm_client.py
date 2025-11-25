"""
LLM Client for parsing OCR text into structured event data.
Uses Ollama with robust error handling.
"""

from pathlib import Path
import ollama
import json
from src.shared.models import Event
from datetime import datetime
from typing import Optional


class LLMClient:
    """
    Parses OCR text into structured Event objects using Ollama LLM.
    """
    
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initialize LLM client.
        
        Args:
            model_name: Ollama model name
        """
        self.model_name = model_name
    
    def parse_event(self, ocr_text: str, image_path: str) -> Event:
        """
        Parse OCR text into Event object.
        
        Args:
            ocr_text: Raw text from OCR
            image_path: Path to original image
            
        Returns:
            Event object
        """
        # Validate OCR text is not empty
        if not ocr_text or len(ocr_text.strip()) < 10:
            raise Exception("OCR text is too short or empty")
        
        # Build prompt
        prompt = self.build_prompt(ocr_text)
        
        try:
            # Call Ollama
            response = self.call_ollama(prompt)
            
            # Validate response
            if not response or not response.strip():
                raise Exception("LLM returned empty response")
            
            # Extract JSON
            json_text = self.extract_json(response)
            
            # Validate JSON text
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
                raise Exception(f"Invalid JSON: {str(e)}")
            
            # Create event
            event = self.create_event(data, ocr_text, image_path)
            
            return event
        
        except Exception as error:
            raise Exception(f"LLM parsing failed: {str(error)}")
    
    def build_prompt(self, ocr_text: str) -> str:
        """
        Build extraction prompt.
        
        Args:
            ocr_text: OCR text to parse
            
        Returns:
            Complete prompt
        """
        current_year = datetime.now().year
        prompt = f"""Extract event information from this text and return ONLY valid JSON.

            TEXT:
            {ocr_text}

            RULES:
            1. Event name = Main event being advertised (e.g., "4th Annual Artisan Faire")
            2. Organization = Who hosts it (e.g., "Vale Coffee Shoppe")
            3. Location = Venue name only
            4. Address = Full street address
            5. Date = Convert to YYYY-MM-DD format
            - If year is NOT mentioned, use {current_year}
            - Example: "December 7th" → "{current_year}-12-07"
            - Example: "Sunday, December 7th" → "{current_year}-12-07"

            IMPORTANT:
            - Return ONLY valid JSON
            - No markdown code blocks
            - No explanations
            - Start with {{ and end with }}

            JSON Format:
            {{
            "name": "Event name",
            "organization": "Host organization",
            "date": "YYYY-MM-DD",
            "time": "Time range",
            "location": "Venue",
            "address": "Full address",
            "description": null,
            "contact": null,
            "price": null
            }}

            Return JSON now:"""
        
        return prompt
    
    def call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API.
        
        Args:
            prompt: Prompt to send
            
        Returns:
            Response text
        """
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                options={
                    'temperature': 0.0, # deterministic output
                    'top_p': 0.1,
                    'top_k': 1,
                    'seed': 42, # for reproducibility
                    'num_predict': 512 # reduce truncation
                }
            )
            
            return response['message']['content']
        
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
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
                
                # Skip 'json' keyword
                if part.startswith('json'):
                    part = part[4:].strip()
                
                # Check if valid JSON structure
                if part.startswith('{') and part.endswith('}'):
                    return part
        
        # Find JSON object in text
        start = text.find('{')
        end = text.rfind('}')
        
        if start != -1 and end != -1 and end > start:
            return text[start:end+1]
        
        # No JSON found
        return text
    
    def create_event(self, data: dict, ocr_text: str, image_path: str) -> Event:
        """
        Create Event object from parsed data.
        
        Args:
            data: Parsed JSON
            ocr_text: Original OCR text
            image_path: Original image path
            
        Returns:
            Event object
        """
        # Validate and get name
        name = self.get_name(data, ocr_text)
        
        # Create event
        return Event(
            id=Path(image_path).stem,
            name=name,
            organization=self.clean(data.get('organization')),
            date=self.clean(data.get('date')),
            time=self.clean(data.get('time')),
            location=self.clean(data.get('location')),
            address=self.clean(data.get('address')),
            description=self.clean(data.get('description')),
            contact=self.clean(data.get('contact')),
            price=self.clean(data.get('price')),
            links=[],
            image_path=image_path,
            raw_ocr_text=ocr_text,
            extracted_at=datetime.now().isoformat()
        )
    
    def get_name(self, data: dict, ocr_text: str) -> str:
        """
        Get event name with validation.
        
        Args:
            data: Parsed data
            ocr_text: OCR text for fallback
            
        Returns:
            Valid event name
        """
        name = data.get('name', '').strip()
        
        # Fallback if empty
        if not name or name.lower() in ['null', 'none']:
            lines = [l.strip() for l in ocr_text.split('\n') if l.strip()]
            name = ' '.join(lines[:3]) if lines else 'Unknown Event'
        
        # Truncate if too long
        if len(name) > 100:
            name = name[:80].strip()
        
        return name
    
    def clean(self, value) -> Optional[str]:
        """
        Clean string value.
        
        Args:
            value: Value to clean
            
        Returns:
            Cleaned string or None
        """
        if value is None:
            return None
        
        text = str(value).strip()
        
        if text.lower() in ['null', 'none', 'n/a', '']:
            return None
        
        return text