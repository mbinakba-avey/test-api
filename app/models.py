from sqlmodel import SQLModel, Field
from typing import Optional

class PromptRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    prompt: str
    response: str
