FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY bricklawyer ./bricklawyer
COPY api ./api
COPY models/ledgar_tfidf_svm.joblib ./models/ledgar_tfidf_svm.joblib

CMD exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}
