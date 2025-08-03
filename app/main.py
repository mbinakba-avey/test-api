from fastapi import FastAPI, Depends
from sqlmodel import Session
from contextlib import asynccontextmanager
from app.schemas import PromptInput, PromptOutput
from app.models import PromptRecord
from app.database import create_db_and_tables, get_session
from app.langchain_client import get_langchain_response


@asynccontextmanager
async def lifespan(app: FastAPI):    
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/infer", response_model=PromptOutput)
def infer(prompt_input: PromptInput, session: Session = Depends(get_session)):
    prompt = prompt_input.prompt
    response = get_langchain_response(prompt)

    prompt_entry = PromptRecord(prompt=prompt, response=response)
    session.add(prompt_entry)
    session.commit()
    session.refresh(prompt_entry)

    return prompt_entry
