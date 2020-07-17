FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc socat

RUN groupadd pilot
RUN useradd pilot --gid pilot

WORKDIR /app
COPY ./app /app

ENTRYPOINT [ "bash", "/app/startService.sh" ]
