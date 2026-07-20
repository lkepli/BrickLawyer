import os
from pathlib import Path

import joblib

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", Path(__file__).resolve().parent.parent / "models" / "ledgar_tfidf_svm.joblib")
)

_pipeline = joblib.load(MODEL_PATH)


def predict_clause(text: str) -> dict:
    probs = _pipeline.predict_proba([text])[0]
    best_idx = probs.argmax()

    return {
        "predicted_label": _pipeline.classes_[best_idx],
        "probability": float(probs[best_idx]),
        "status": "ok",
    }
