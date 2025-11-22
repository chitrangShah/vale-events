
import ollama
import json
from pathlib import Path
from shared.models import Event


class LLMClient:
    """Handles LLM-based text parsing and JSON structuring"""
    
    def __init__(self):
        self.model = "llama3.2"
        self.prompt_template = """
            You are an expert at extracting event information from OCR text.

            Below is raw OCR text extracted from an event flyer/image. 
            Parse this text and extract event details.

            Return ONLY valid JSON with these exact fields (use null if not found):

            {{
            "name": "name of the event",
            "date": "YYYY-MM-DD or MM/DD/YYYY or other format",
            "time": "HH:MM AM/PM format",
            "location": "venue name",
            "address": "full street address",
            "description": "brief description",
            "links": ["url1", "url2"],
            "contact": "phone number or email"
            }}

            Instructions:
            - Clean up any OCR errors or garbled text
            - Be precise with dates
            - Be precise with times
            - Extract all URLs you find
            - If date is a range, use the start date
            - Use null for any field you cannot find
            - Do not include any extra text, explanations, or formatting
            - Ensure the JSON is valid
            - Do not assume any information not present in the OCR text

            OCR Text:
            {ocr_text}

            Return ONLY the JSON object, nothing else.
        """
    
    def process_text(self, ocr_text: str, image_path: str) -> Event:
        """
        Parse OCR text and extract structured event data using LLM
        """
        
        # Prompt setup
        prompt = self.prompt_template.format(ocr_text=ocr_text)
        
        # Call Ollama
        response = ollama.chat(
            model=self.model,
            messages=[{
                "role": "user", 
                "content": prompt
            }]
        )
        
        content = response['message']['content']
        
        # Clean markdown code blocks if present
        if '```json' in content:
            content = content.split('```json')[1].split('```')[0]
        elif '```' in content:
            content = content.split('```')[1].split('```')[0]
        
        # Parse JSON response
        event_data = json.loads(content.strip())
        
        # Setup Event model
        image_name = Path(image_path).stem
        
        event = Event(
            id=f"{image_name}",
            image_path=image_path,
            raw_ocr_text=ocr_text,  # Store original OCR output
            **event_data
        )
        
        return event