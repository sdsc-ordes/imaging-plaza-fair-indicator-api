FROM python:3.11

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install .

ENTRYPOINT ["bash", "/app/imaging_plaza_fair_indicator_api/entrypoint.sh"]