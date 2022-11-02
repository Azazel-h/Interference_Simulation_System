FROM python

COPY requirements.txt req.txt
RUN pip3 install -r req.txt

COPY docker/setup.sh setup.sh
RUN chmod +x setup.sh

EXPOSE 8000

CMD ./setup.sh
