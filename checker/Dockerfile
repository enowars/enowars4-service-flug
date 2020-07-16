FROM python:3.8
LABEL maintainer="ENOFLAG <mail@enoflag.de>"

WORKDIR /checker
#COPY ./requirements.txt /checker/requirements.txt

RUN pip3 install enochecker gunicorn[eventlet]
COPY . .

ENTRYPOINT [ "bash", "entry.sh" ]
