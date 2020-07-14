FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc socat

#COPY ./code /code
WORKDIR /app

ENTRYPOINT [ "bash", "/app/startService.sh" ]
#ENTRYPOINT [ "ls", "/code" ]
