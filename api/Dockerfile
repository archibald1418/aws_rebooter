FROM python:3.11-alpine

WORKDIR /app

COPY ../requirements.txt ./src .
RUN pip install --no-cache-dir -r ./requirements.txt

CMD uvicorn main:app \
    --host 0.0.0.0 --port 8000 \
    --reload \
    --forwarded-allow-ips='*'
# allows proxying

