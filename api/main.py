from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClauseRequest(BaseModel):
    text: str

class ClauseResponse(BaseModel):
    predicted_label: str
    confidence: float
    status: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=ClauseResponse)
def predict(req: ClauseRequest):
    return ClauseResponse(
        predicted_label="Governing Laws",
        confidence=0.87,
        status="mock prediction - model not connected yet"
    )
