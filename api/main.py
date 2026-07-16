from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -------------------------------------------------
# Create FastAPI app
# -------------------------------------------------
app = FastAPI()

# -------------------------------------------------
# CORS middleware
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to your frontend URL
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------
# Request / Response models
# -------------------------------------------------
class ClauseRequest(BaseModel):
    text: str


class ClauseResponse(BaseModel):
    predicted_label: str
    confidence: float
    status: str


# -------------------------------------------------
# Endpoints
# -------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=ClauseResponse)
def predict(req: ClauseRequest):
    return ClauseResponse(
        predicted_label="Confidentiality", confidence=0.91, status="mock prediction"
    )
