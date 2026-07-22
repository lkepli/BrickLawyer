# BrickLawyer

BrickLawyer is a legal NLP prototype for classifying contract clauses into predefined legal clause categories.

The project uses the LEDGAR dataset from LexGLUE and provides a supervised machine learning API for predicting the most likely legal clause label from a given contract clause.

## Project links

- [Trello board](https://trello.com/b/1FPKeobY/bricklawyer)

## Current model

The current prediction pipeline uses:

- TF-IDF vectorization
- Linear SVM classifier
- probability calibration with `CalibratedClassifierCV`
- full LEDGAR label set as the main classification target
- top-20 label experiment as an earlier comparison

We originally tested a Logistic Regression baseline and later compared it with a Linear SVM model. The Linear SVM approach performed better across the main evaluation metrics, so it became the selected model for the prediction endpoint.

Because `LinearSVC` does not support `predict_proba` directly, the classifier is wrapped with `CalibratedClassifierCV`. This allows the API to return a calibrated confidence/probability estimate together with the predicted label.

Current validation results for the full-label baseline are approximately:

- Accuracy: around 83%
- Macro F1: around 75%
- Weighted F1: around 82%

## Confidence handling

The API returns a `status` value based on the model confidence.

- If `confidence >= 0.6`, the response status is `ok`.
- If `confidence < 0.6`, the response status indicates a low-confidence prediction.

This allows the frontend to warn the user when the model is uncertain.

## Data

The dataset is loaded from Hugging Face:

- `coastalcph/lex_glue`
- subset: `ledgar`

Raw data and local dataset cache should be stored under `raw_data/`.

This folder is ignored by Git and should not be committed.

## API

The backend uses FastAPI.

Available endpoints:

- `GET /`
- `POST /predict`

Example prediction request:

```json
{
  "text": "This agreement shall be governed by the laws of the State of New York."
}
```

Example prediction response:

```json
{
  "predicted_label": "Governing Laws",
  "probability": 0.87,
  "status": "ok"
}
```

## Setup

Create and activate the project Python environment:

```bash
pyenv virtualenv 3.10.6 bricklawyer
pyenv local bricklawyer
```

If the virtual environment already exists, only run:

```bash
pyenv local bricklawyer
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn api.main:app --reload
```

Or, if using the Makefile:

```bash
make run_api
```

## Docker

Build the Docker image locally:

```bash
docker build -t bricklawyer-api .
```

Run the container locally:

```bash
docker run -p 8080:8080 bricklawyer-api
```

Then test the API at:

```text
http://localhost:8080/
http://localhost:8080/predict
```

## Deployment

The backend is prepared for deployment on Google Cloud Run.

The Docker image contains the FastAPI application, runtime dependencies, and the trained model artifact required for prediction.

Deployment steps include:

- build the Docker image
- push the image to Google Artifact Registry
- deploy the image to Cloud Run
- test the public API endpoints

## Project status

Completed:

- initial EDA notebook
- label distribution and class imbalance analysis
- baseline TF-IDF + Logistic Regression model
- Linear SVM comparison
- selected TF-IDF + calibrated Linear SVM model
- full-label and top-20 comparison
- backend/API structure
- model integration into the `/predict` endpoint
- confidence score returned from the API
- low-confidence status handling
- Docker image preparation
- deployment configuration preparation
- Streamlit frontend
- frontend/API integration

In progress:

- GCP Cloud Run deployment testing
- final documentation cleanup
- demo flow and presentation
