from paddleocr import PaddleOCR
import re
import traceback

class OCRClient:
    """Generic OCR for any flyer style using PaddleOCR 3.3.2"""
    
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=False,  # Disable rotated text detection for better performance
            lang='en'
        )
    
    def extract_text(self, image_path: str) -> str:
        """
        Extract and group text by horizontal lines.
        Works for any flyer design.
        """
        try:
            print(f"Extracting text with PaddleOCR...")
            
            # Run OCR
            result = self.ocr.ocr(image_path)
            
            if not result or len(result) == 0:
                print(f"No text detected")
                return ""
            
            # Get first page (dictionary)
            page = result[0]
            
            # Extract data
            texts = page.get('rec_texts', [])
            scores = page.get('rec_scores', [])
            boxes = page.get('dt_polys', [])
            
            print(f"Found {len(texts)} text items")
            
            # Group text by horizontal lines
            grouped_text = self.group_text_by_lines(texts, boxes, scores)
            
            # Apply only generic corrections
            corrected_text = self.apply_generic_corrections(grouped_text)
            
            print(f"Extracted {len(corrected_text)} chars")
            
            return corrected_text
        
        except Exception as e:
            print(f"Error: {traceback.format_exc()}")
            raise Exception(f"OCR error: {str(e)}")
    
    def group_text_by_lines(self, texts: list, boxes: list, scores: list) -> str:
        """
        Group text items on same horizontal line.
        """
        # Use lower threshold to catch more text
        items = []
        for text, box, score in zip(texts, boxes, scores):
            if score > 0.3 and text.strip():
                y_center = (box[0][1] + box[2][1]) / 2
                x_left = box[0][0]
                items.append({
                    'text': text,
                    'y': y_center,
                    'x': x_left,
                    'score': score
                })
        
        if not items:
            return ""
        
        # Sort by Y (top to bottom), then X (left to right)
        items.sort(key=lambda item: (item['y'], item['x']))
        
        # Group into lines based on Y position
        lines = []
        current_line = []
        last_y = items[0]['y']
        
        for item in items:
            # Same line if within 30px vertically
            if abs(item['y'] - last_y) < 30:
                current_line.append(item['text'])
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [item['text']]
                last_y = item['y']
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def apply_generic_corrections(self, text: str) -> str:
        """
        No image-specific fixes.
        """
        # Fix common date ordinals
        text = re.sub(r'(\d+)th\b', lambda m: self._fix_ordinal(m.group(1)), text)
        
        # Fix common time patterns
        text = re.sub(r'(\d+)am', r'\1am', text, flags=re.IGNORECASE)
        text = re.sub(r'(\d+)pm', r'\1pm', text, flags=re.IGNORECASE)
        
        # Fix common abbreviations
        text = text.replace('NJ ', 'NJ ')  # Ensure space after state
        
        return text
    
    def fix_ordinal(self, number: str) -> str:
        """Fix ordinal suffixes (1st, 2nd, 3rd, 4th, etc.)"""
        n = int(number)
        if 11 <= n <= 13:
            return f"{n}th"
        elif n % 10 == 1:
            return f"{n}st"
        elif n % 10 == 2:
            return f"{n}nd"
        elif n % 10 == 3:
            return f"{n}rd"
        else:
            return f"{n}th"