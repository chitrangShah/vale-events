
from fastapi import APIRouter
from shared.models import Output
from features.process_events.handler import ProcessEventsHandler

# Router path: /process-events
router = APIRouter(prefix="/api", tags=["process"])

# Router logic
@router.post("/process", response_model=Output)
async def process_events(force: bool = False) -> Output:


    handler = ProcessEventsHandler()
    return handler.execute(force=force)
