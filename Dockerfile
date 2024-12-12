FROM python:3.11

RUN apt-get update

COPY . /app

#RUN apt-get install -y python3 pip
#COPY requirements.txt . 
#RUN pip install requirements.txt
WORKDIR /app
#RUN pip install requirements.txt

RUN pip install .

ENTRYPOINT ["bash", "/app/imaging_plaza_fair_indicator_api/entrypoint.sh"]