import os
from pathlib import Path

import joblib

MODEL_PATH = Path(
    os.getenv("MODEL_PATH", Path(__file__).resolve().parent.parent / "models" / "ledgar_tfidf_svm.joblib")
)

_pipeline = joblib.load(MODEL_PATH)


LOW_CONFIDENCE_THRESHOLD = 0.6


def predict_clause(text: str) -> dict:
    probs = _pipeline.predict_proba([text])[0]
    best_idx = probs.argmax()
    probability = float(probs[best_idx])

    return {
        "predicted_label": _pipeline.classes_[best_idx],
        "probability": probability,
        "status": "ok" if probability >= LOW_CONFIDENCE_THRESHOLD else "low_confidence",
    }
