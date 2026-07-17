# BrickLawyer

BrickLawyer is a legal NLP prototype for classifying contract clauses into predefined legal clause categories.

The project uses the LEDGAR dataset from LexGLUE and starts with a classical supervised machine learning baseline using TF-IDF and Logistic Regression.

## Project links

- [Trello board](https://trello.com/b/1FPKeobY/bricklawyer)

## Current model

The current baseline model uses:

- TF-IDF vectorization
- Logistic Regression classifier
- full LEDGAR label set as the main baseline
- top-20 label experiment as a comparison

Current validation results for the full-label baseline:

- Accuracy: around 83%
- Macro F1: around 75%
- Weighted F1: around 82%

## Data

The dataset is loaded from Hugging Face:

- `coastalcph/lex_glue`
- subset: `ledgar`

Raw data and local dataset cache should be stored under `raw_data/`.

This folder is ignored by Git and should not be committed.

## API

The backend uses FastAPI.

Planned local endpoints:

- `GET /health`
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
  "confidence": 0.87,
  "status": "model prediction"
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

Or, if the Makefile is available:

```bash
make run_api
```

## Project status

Completed:

- initial EDA notebook
- label distribution and class imbalance analysis
- baseline TF-IDF + Logistic Regression model
- full-label and top-20 comparison
- backend/API structure
- model integration into the `/predict` endpoint

In progress:

- Docker and deployment preparation
