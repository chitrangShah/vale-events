"""
Entry point to run main.py for Vale Events
Check Python version and dependencies
Requires Python 3.12+

"""

import sys
import uvicorn

def check_python_version():
    if sys.version_info < (3, 12):
        print("Error. Requires Python 3.12+")
        print(f"Current version : { sys.version }")
        sys.exit(1)

if __name__ == "__main__":
    check_python_version()
    
    print("Starting Vale Events (Python 3.12)")
    print("Frontend: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    # Run web server
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000,
        reload=True) # Set auto reload for testing changes

    