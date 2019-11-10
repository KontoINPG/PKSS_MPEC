FROM python:3-alpine
WORKDIR /

ADD main.py main.py
ADD Temperatura.csv Temperatura.csv

RUN pip install bottle
RUN pip install requests

EXPOSE 8080
CMD python main.py