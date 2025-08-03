from fastapi import FastAPI, Depends
from sqlmodel import Session
from contextlib import asynccontextmanager

from app.models import Prompt
from app.database import create_db_and_tables, get_session
from app.langchain_client import get_langchain_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/infer")
def infer(prompt: str, 
          session: Session = Depends(get_session)):
    response = get_langchain_response(prompt)
    prompt_entry = Prompt(prompt=prompt, response=response)
    session.add(prompt_entry)
    session.commit()
    session.refresh(prompt_entry)
    return {"id": prompt_entry.id, "prompt": prompt, "response": response}
