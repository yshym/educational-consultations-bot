FROM python:3.8

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY . /code/

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install cmake

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev

RUN pip install "en_core_web_lg-3.0.0.tar.gz"

RUN sed "1,2d" .envrc > .env

ENTRYPOINT [ "bash", "entrypoint.sh" ]
