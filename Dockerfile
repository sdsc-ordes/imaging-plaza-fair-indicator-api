FROM python:3.11

RUN apt-get update
#RUN apt-get install -y python3 pip
#COPY requirements.txt . 
#RUN pip install requirements.txt
WORKDIR /app

##################################################
# Poetry setup
##################################################
FROM python as poetry

# Install poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

# Copy necessary files only
COPY imaging_plaza_fair_indicator_api ./imaging_plaza_fair_indicator_api
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
COPY .env.dist ./.env.dist
COPY README.md ./README.md
RUN apt-get update && \
    apt-get install -y gcc
    
RUN poetry config virtualenvs.create false

# Poetry install
RUN poetry install --no-interaction --no-ansi -vvv

##################################################
# imaging_plaza_fair_indicator_api
##################################################

COPY imaging_plaza_fair_indicator_api /app/imaging_plaza_fair_indicator_api
#COPY ./tests /tests

ENTRYPOINT ["bash", "/app/imaging_plaza_fair_indicator_api/entrypoint.sh"]