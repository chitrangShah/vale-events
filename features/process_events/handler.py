
from pathlib import Path
from shared.clients.ocr_client import OCRClient
from shared.models import Output


class ProcessEventsHandler:
    def __init__(self):
        self.ocr_client = OCRClient()
        self.images_dir = Path("data/images")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
    def execute_ocr(self, force: bool =- False) -> Output:
        
        """Execute OCR on the given image and return the extracted text."""
        result = Output(
            processed=0, 
            skipped=0,
            errors=[])
        
        for image_path in self.images_dir.glob("*.jpg"):
            try:
                extracted_text = self.ocr_client.extract_text(str(image_path))
                if extracted_text:
                    result.processed += 1
                else:
                    result.skipped += 1
            except Exception as e:
                result.errors.append(f"Error processing {image_path.name}: {str(e)}")
                
        return result
    
    