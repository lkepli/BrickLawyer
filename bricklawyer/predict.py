import os
from pathlib import Path

import joblib

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", Path(__file__).resolve().parent.parent / "models" / "ledgar_tfidf_logreg.joblib")
)

_pipeline = joblib.load(MODEL_PATH)


def predict_clause(text: str) -> dict:
    predicted_label = _pipeline.predict([text])[0]

    confidence = None
    if hasattr(_pipeline, "predict_proba"):
        confidence = float(_pipeline.predict_proba([text]).max())

    return {
        "predicted_label": predicted_label,
        "confidence": confidence,
        "status": "ok",
    }
