FROM ubuntu:latest
RUN apt-get update && apt-get install -y make gcc

COPY ./code /service-flug
WORKDIR /service-flug

EXPOSE 7478

CMD ["bash" "./start_service.sh" ]
