import pytesseract
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

class OCRClient:
    """Client for performing OCR on images using Tesseract OCR engine."""
    def __init__(self):
        pass

    """Preprocess the image to enhance OCR accuracy."""
    def preprocess_image(self, image_path: str) -> Image.Image:    
        image = Image.open(image_path)
        image = ImageOps.grayscale(image)
        image = ImageEnhance.Contrast(image).enhance(2)
        image = image.filter(ImageFilter.MedianFilter())
        return image

    """Extract text from the image using Tesseract OCR."""
    def extract_text(self, image_path: str) -> str:
        try:
            # Preprocess the image
            preprocessed_image = self.preprocess_image(image_path)
        
            # Perform OCR
            text = pytesseract.image_to_string(preprocessed_image)
        
            # Return the extracted text without leading/trailing whitespace
            return text.strip()
        
        except Exception as e:
            print(f"Error during OCR extraction: {e}") 
            return ""