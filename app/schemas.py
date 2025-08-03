from pydantic import BaseModel

class PromptInput(BaseModel):
    prompt: str

class PromptOutput(BaseModel):
    id: int
    prompt: str
    response: str
