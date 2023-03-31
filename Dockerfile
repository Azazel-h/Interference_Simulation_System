FROM python

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install gettext-base && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip3 install -r /app/requirements.txt
RUN python3 /app/manage.py makemigrations fabry_perot michelson && python3 /app/manage.py migrate
