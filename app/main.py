from fastapi import FastAPI, Depends
from sqlmodel import Session
from contextlib import asynccontextmanager
from app.schemas import PromptInput, PromptOutput
from app.models import PromptRecord
from app.database import create_db_and_tables, get_session
from app.langchain_client import get_langchain_response
import uvicorn
import argparse

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



def main():
    parser = argparse.ArgumentParser(description="Run FastAPI app with specified host and port.")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port number to bind to")
    args = parser.parse_args()

    uvicorn.run("app.main:app", host=args.host, port=args.port, reload=True)

if __name__ == "__main__":
    main()