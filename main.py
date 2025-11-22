from fastapi import FastAPI
from features.process_events.endpoint import router as process_router

# Create FastAPI app instance
app = FastAPI(
    title="Vale Events Extractor",
    description="API for extracting events from local event images using OCR technology.",
    version="1.0.0"
)

# Include feature routers
app.include_router(process_router)

# HEalth check endpoint
@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "ok"}