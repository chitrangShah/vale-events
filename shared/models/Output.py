from pydantic import BaseModel, Field

class Output(BaseModel):
    processed: int
    skipped: int
    errors: list[str]
    