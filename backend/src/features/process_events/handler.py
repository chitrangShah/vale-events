
import json
from pathlib import Path
from src.shared.clients.llm_client import LLMClient
from src.shared.clients.ocr_client import OCRClient
from src.shared.models import Output


class ProcessEventsHandler:
    def __init__(self):
        self.ocr_client = OCRClient()
        self.llm_client = LLMClient()
        self.images_dir = Path("data/images")
        self.events_dir = Path("data/events")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)
        
    def execute(self, force: bool = False) -> Output:
        
        """
        Execute OCR on the given image and return the extracted text.
        Execute LLM processing to extract structured event data from the OCR text.
        """
        
        result = Output(
            processed=0, 
            skipped=0,
            errors=[])
        
        for image_path in self.images_dir.glob("*.jpg"):
            try:
                print(f"Processing: {image_path.name}")
                
                # Step 1: Extract text using OCR
                extracted_text = self.ocr_client.extract_text(str(image_path))
                
                # Step 2: Process text using LLM to extract event data
                event = self.llm_client.parse_event(
                    ocr_text=extracted_text, 
                    image_path=str(image_path)
                )
                print(f"Extracted Event from {image_path.name}")
                
                # Step 3: Save event data to JSON file
                event_file = self.events_dir / f"{image_path.stem}.json"
                if event_file.exists() and not force:
                    print(f"Skipping existing event file: {event_file.name}")
                    result.skipped += 1
                    continue
                
                with open(event_file, 'w') as f:
                    json.dump(event.dict(), f, indent=2)
                
                result.processed += 1
                
            except Exception as e:
                result.errors.append(f"Error processing {image_path.name}: {str(e)}")
                
        return result
    
    