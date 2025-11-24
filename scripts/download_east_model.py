"""
Download the EAST text detection model
"""
import requests
from pathlib import Path

def download_east_model():
    """Download pre-trained EAST model"""
    
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / "frozen_east_text_detection.pb"
    
    if model_path.exists():
        print(f"✅ Model already exists at {model_path}")
        return
    
    print("📥 Downloading EAST model (approximately 84MB)...")
    
    # Download from OpenCV's repository
    url = "https://github.com/oyyd/frozen_east_text_detection.pb/raw/master/frozen_east_text_detection.pb"
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(model_path, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\r  Progress: {percent:.1f}%", end='')
    
    print(f"\n✅ Model downloaded to {model_path}")

if __name__ == "__main__":
    download_east_model()