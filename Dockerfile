FROM python:3.9

RUN mkdir /app 
COPY ./app /app/app
COPY README.md /app
COPY pyproject.toml /app/

WORKDIR /app


ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry

## you could install use requirements instead of pip to install deps
#RUN poetry export -f requirements.txt --output requirements.txt

#RUN pip install -r requirements.txt 

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

EXPOSE 8000

ENTRYPOINT [ "python", "app/server.py" ]