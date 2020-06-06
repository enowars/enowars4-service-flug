FROM python:3.8
LABEL maintainer="ENOFLAG <mail@enoflag.de>"

RUN pip3 install enochecker==0.1.0  pwntools gunicorn[eventlet]

WORKDIR /checker
#COPY ./requirements.txt /checker/requirements.txt

COPY . .

ENTRYPOINT [ "bash", "entry.sh" ]
