FROM python:3.11-alpine

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./src ./src

VOLUME ./db

# dev build
CMD uvicorn src.app:run_app --host 0.0.0.0 --port 8000  \
        --reload \
        --forwarded-allow-ips='*' \
        --proxy-headers

# TODO: this should be a production build
#CMD gunicorn src.app:run_app -b 0.0.0.0:8000  \
         -w 4
#        -k uvicorn_worker.UvicornWorker \
#        --forwarded-allow-ips='*' \
#        --capture-output
