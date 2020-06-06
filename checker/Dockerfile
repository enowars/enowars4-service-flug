FROM python:3.8
LABEL maintainer="ENOFLAG <mail@enoflag.de>"

WORKDIR /checker
COPY ./requirements.txt /checker/requirements.txt

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt 
COPY . .

ENTRYPOINT [ "bash", "entry.sh" ]
