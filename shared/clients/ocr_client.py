import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

class OCRClient:
    """Client for performing OCR on images using Tesseract OCR engine."""
    def __init__(self):
        pass

    """Preprocess the image to enhance OCR accuracy."""
    def preprocess_image(self, image_path: str) -> Image.Image:    
        image = Image.open(image_path)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Convert to grayscale
        image = image.convert('L')
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Sharpen
        image = image.filter(ImageFilter.SHARPEN)
        
        # Increase size if image is small (helps OCR)
        width, height = image.size
        if width < 1000 or height < 1000:
            scale = max(1000 / width, 1000 / height)
            new_size = (int(width * scale), int(height * scale))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        
        return image

    """Extract text from the image using Tesseract OCR."""
    def extract_text(self, image_path: str) -> str:
        try:
            # Preprocess the image
            preprocessed_image = self.preprocess_image(image_path)
        
            # Perform OCR
            text = pytesseract.image_to_string(preprocessed_image, lang='eng')
        
            # Return the extracted text without leading/trailing whitespace
            return text.strip()
        
        except Exception as e:
            print(f"Error during OCR extraction: {e}") 
            return ""