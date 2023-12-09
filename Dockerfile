FROM python:3.8

RUN mkdir app
RUN mkdir app/data

WORKDIR /app

COPY kombat.py /app
COPY data/*.json /app/data

ENTRYPOINT ["/bin/bash"]
