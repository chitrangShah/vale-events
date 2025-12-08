import json
from pathlib import Path
from src.shared.clients.llm_client import LLMClient
from src.shared.models import Output


class ProcessEventsHandler:
    def __init__(self):
        self.llm_client = LLMClient()
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
                existing_events = list(self.events_dir.glob(f"{image_path.stem}*.json"))
                if existing_events and not force:
                    print(f"Skipping existing: {image_path.stem} ({len(existing_events)} events)")
                    result.skipped += len(existing_events)
                    continue
                
                print(f"Processing: {image_path.name}")
                
                # Extract event(s) directly from image - may return multiple
                events = self.llm_client.parse_events_from_image(str(image_path))
                
                # Save each event
                for event in events:
                    event_file = self.events_dir / f"{event.id}.json"
                    with open(event_file, 'w') as f:
                        json.dump(event.dict(), f, indent=2)
                    print(f"    Event: {event.name} ({event.date})")
                
                result.processed += len(events)
                
            except Exception as e:
                result.errors.append(f"Error processing {image_path.name}: {str(e)}")
                
        return result