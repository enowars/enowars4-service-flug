FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc

COPY . /service-flug
WORKDIR /service-flug/build

EXPOSE 1337

CMD ["./CTF_service_flug_start.sh" ]
