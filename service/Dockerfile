FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc socat

WORKDIR /app

ENTRYPOINT [ "bash", "/app/startService.sh" ]
