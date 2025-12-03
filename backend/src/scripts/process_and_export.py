"""
Process events locally and export to frontend.
Run this script when you add new images.
TODO: Automate this in CI/CD pipeline and use Facebook API to retrieve images periodically.
"""

import datetime
from pathlib import Path
import json
import shutil
from src.features.process_events.handler import ProcessEventsHandler


def process_and_export():
    """Process events and copy results to frontend."""
    
    print("Processing events...")
    
    # Process events
    handler = ProcessEventsHandler()
    result = handler.execute(force=False)
    
    print(f"Processed: {result.processed}")
    print(f"Errors: {len(result.errors)}")
    
    # Write errors to file
    if result.errors:
        # Create logs directory
        logs_dir = Path(__file__).parent.parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Write error log
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        error_file = logs_dir / f"errors_{timestamp}.log"
        
        with open(error_file, 'w') as f:
            f.write("Processing Errors\n")
            f.write("="*60 + "\n\n")
            
            for i, error in enumerate(result.errors, 1):
                f.write(f"Error {i}:\n")
                f.write(f"{error}\n\n")
        
        print(f"\nErrors logged to: {error_file}")
    
    # Export to frontend
    backend_events = Path("data/events")
    frontend_static = Path("../frontend/static/api")
    
    # Create frontend API directory
    frontend_static.mkdir(parents=True, exist_ok=True)
    
    # Collect all events
    all_events = []
    for event_file in backend_events.glob("*.json"):
        with open(event_file, 'r') as f:
            event = json.load(f)
            all_events.append(event)
    
    # Write events.json to frontend
    with open(frontend_static / "events.json", 'w') as f:
        json.dump({
            "events": all_events,
            "count": len(all_events)
        }, f, indent=2)
    
    # Copy images to frontend
    backend_images = Path("data/images")
    frontend_images = Path("../frontend/static/images")
    frontend_images.mkdir(parents=True, exist_ok=True)
    
    valid_extensions = ['.jpg', '.jpeg', '.png']
    
    for image in backend_images.iterdir():
        
        if image.suffix.lower() not in valid_extensions:
            continue
        
        shutil.copy(image, frontend_images / image.name)
    
    print(f"\nExported {len(all_events)} events to frontend/static/api/")
    print("Exported images to frontend/static/images/")
    print("\nNext steps:")
    print("1. git add frontend/static/")
    print("2. git commit -m 'Update events'")
    print("3. git push")
    print("4. Vercel will auto-deploy")


if __name__ == "__main__":
    process_and_export()