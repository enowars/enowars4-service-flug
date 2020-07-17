FROM python:3.8
LABEL maintainer="ENOFLAG <mail@enoflag.de>"

WORKDIR /checker
COPY ./requirements.txt /checker/requirements.txt

RUN pip3 install -r requirements.txt
COPY . .

ENTRYPOINT [ "bash", "entry.sh" ]
