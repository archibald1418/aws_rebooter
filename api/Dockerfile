FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src ./src

VOLUME /opt/users

CMD uvicorn src.app:run_app --host 0.0.0.0 --port 8000 \
        --reload \
        --proxy-headers \
        --forwarded-allow-ips='*' \
	--log-config='src/log_conf.yaml'
# allows proxying

