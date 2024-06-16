
FROM python:3.10-slim


WORKDIR /bot


COPY requirements.txt /bot/requirements.txt


RUN pip install --no-cache-dir -r /bot/requirements.txt


RUN apt-get update && apt-get install -y curl


COPY . /bot


CMD ["python", "main.py"]
