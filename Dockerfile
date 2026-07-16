FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY bricklawyer ./bricklawyer
COPY api ./api

RUN mkdir -p raw_data models

CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}
