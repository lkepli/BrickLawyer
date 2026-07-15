cd ….# Run the API locally

## 1. Activate virtual environment
source venv/bin/activate

## 2. Start the server
uvicorn api.main:app --reload

## 3. Test endpoints
Health: http://127.0.0.1:8000/health
Docs:   http://127.0.0.1:8000/docs
