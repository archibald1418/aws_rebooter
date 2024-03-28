FROM python:3.11-alpine

WORKDIR /app

COPY ../requirements.txt ./src .
RUN pip install --no-cache-dir -r ./requirements.txt

CMD ["/bin/sh", "-c", "uvicorn --host 0.0.0.0 --port 8000  main:app"]
