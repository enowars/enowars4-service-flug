FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc socat

#COPY ./code /code
WORKDIR /code

ENTRYPOINT [ "bash", "/code/startService.sh" ]
#ENTRYPOINT [ "ls", "/code" ]
