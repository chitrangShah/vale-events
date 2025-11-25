from fastapi import FastAPI
from .features.process_events.endpoint import router as process_router

def create_app() -> FastAPI:
    """
    Create and configure FastAPI app.
    
    Returns:
        FastAPI app instance
    """
    
    app = FastAPI(
        title="Vale Events Backend",
        description="Backend service for processing Vale events",
        version="1.0.0"
    )
    
    # TODO: Add middleware, exception handlers, etc. here
    
    # Feature routers
    app.include_router(process_router)
    
    return app

app = create_app()

@app.get("/")
async def root():
    return {"message": "Welcome to the Vale Events Backend API"}

# Health check endpoint
@app.get("/api/health", tags=["health"])
async def health_check():
    return {"status": "ok"}