from fastapi import FastAPI
from pydantic import BaseModel
from agents.root_agent import root_agent

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
async def chat(req: ChatRequest):
    response = await root_agent(req.message)
    return {"response": response}