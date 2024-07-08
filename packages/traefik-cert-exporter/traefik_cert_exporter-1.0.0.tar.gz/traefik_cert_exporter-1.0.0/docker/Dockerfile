FROM python:3.12-slim

RUN apt-get update && apt-get install -y cron

COPY . /app
WORKDIR /app

RUN pip install .

ENV CRON_SCHEDULE="0 0 1 * *"
ENV STORAGE_FILE="traefik/acme.json"
ENV OUTPUT_PATH="certs/"
ENV ON_START=1

COPY docker/entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
