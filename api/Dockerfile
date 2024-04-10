FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src ./src

VOLUME /opt/users

CMD : \
    && touch /opt/users/users.json \
    && uvicorn src.main:app --host 0.0.0.0 --port 8000 \
        --reload \
        --forwarded-allow-ips='*'
# allows proxying

