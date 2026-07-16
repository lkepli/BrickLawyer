FROM python:3.10

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY bricklawyer bricklawyer
COPY api api

RUN mkdir /raw_data
RUN mkdir /models

CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}
