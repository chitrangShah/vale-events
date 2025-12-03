import json
from pathlib import Path
from src.shared.clients.llm_client import LLMClient
from src.shared.models import Output


class ProcessEventsHandler:
    def __init__(self):
        self.llm_client = LLMClient()  # Uses llama3.2-vision by default
        self.images_dir = Path("data/images")
        self.events_dir = Path("data/events")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.events_dir.mkdir(parents=True, exist_ok=True)
        
    def execute(self, force: bool = False) -> Output:
        """
        Process images using vision model to extract structured event data.
        """
        
        result = Output(
            processed=0, 
            skipped=0,
            errors=[])
        
        valid_extensions = ['.jpg', '.jpeg', '.png']
        
        for image_path in self.images_dir.iterdir():
            
            if image_path.suffix.lower() not in valid_extensions:
                continue
            
            try:
                # Check if already processed
                event_file = self.events_dir / f"{image_path.stem}.json"
                if event_file.exists() and not force:
                    print(f"Skipping existing: {event_file.name}")
                    result.skipped += 1
                    continue
                
                print(f"Processing: {image_path.name}")
                
                # Extract event data directly from image (no OCR step)
                event = self.llm_client.parse_event_from_image(str(image_path))
                print(f"Extracted: {event.name}")
                
                # Save event data
                with open(event_file, 'w') as f:
                    json.dump(event.dict(), f, indent=2)
                
                result.processed += 1
                
            except Exception as e:
                result.errors.append(f"Error processing {image_path.name}: {str(e)}")
                
        return result