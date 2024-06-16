
FROM python:3.10-slim


WORKDIR /app


COPY inference/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt


COPY inference /app/inference
COPY model /app/model


ENV PYTHONPATH=/app/inference


RUN python -m nltk.downloader stopwords


EXPOSE 8000


CMD ["uvicorn", "inference.app:app", "--host", "0.0.0.0", "--port", "8000"]
