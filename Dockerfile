FROM python:3.11

RUN apt-get update
RUN apt-get install -y python3 pip
COPY requirements.txt . 
RUN pip install requirements.txt


COPY ./app /app

# Install poetry?
# Run with poetry?

#COPY ./tests /tests

ENTRYPOINT ["bash", "/app/entrypoint.sh"]