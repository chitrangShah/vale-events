
from pathlib import Path
from shared.clients.llm_client import LLMClient
from shared.clients.ocr_client import OCRClient
from shared.models import Output


class ProcessEventsHandler:
    def __init__(self):
        self.ocr_client = OCRClient()
        self.llm_client = LLMClient()
        self.images_dir = Path("data/images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
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
                # Step 1: Extract text using OCR
                extracted_text = self.ocr_client.extract_text(str(image_path))
                
                # Step 2: Process text using LLM to extract event data
                event = self.llm_client.process_text(
                    ocr_text=extracted_text, 
                    image_path=str(image_path)
                )
                print(f"Extracted Event from {image_path.name}: {event.json()}")
                
                result.processed += 1
                
            except Exception as e:
                result.errors.append(f"Error processing {image_path.name}: {str(e)}")
                
        return result
    
    