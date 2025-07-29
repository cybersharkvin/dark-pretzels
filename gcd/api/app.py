from fastapi import FastAPI
from pydantic import BaseModel

from ..models.inference import generate
from ..models.performance import metrics
from ..services.execution import execute
from ..models.loader import load_model

app = FastAPI()

class AskRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/ask")
async def ask(req: AskRequest):
    result = await generate(req.question)
    return execute(result)

@app.get("/metrics")
async def get_metrics():
    return metrics()

@app.get("/health")
async def health():
    return {"status": "ok"}
