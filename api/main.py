import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from bricklawyer.predict import predict_clause

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "http://localhost,http://localhost:3000").split(",") if o.strip()],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClauseRequest(BaseModel):
    text: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(req: ClauseRequest):
    return predict_clause(req.text)
