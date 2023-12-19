FROM python:3.9

RUN apt-get update
RUN apt-get install -y python3 pip
COPY requirements.txt . 
RUN pip install requirements.txt


COPY ./app /app
COPY ./tests /tests

ENTRYPOINT ["bash", "/app/entrypoint.sh"]
#ENTRYPOINT ["bash"]
#ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "15400"]