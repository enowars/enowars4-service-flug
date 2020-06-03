FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc

COPY . /service-flug
WORKDIR /service-flug

EXPOSE 1337

CMD ["./start_service.sh" ]
