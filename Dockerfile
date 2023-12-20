FROM python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install gettext-base libsasl2-dev python3-dev libldap2-dev libssl-dev libldap-common

WORKDIR /app
COPY . /app

RUN python3 -m pip install -r /app/requirements.txt
