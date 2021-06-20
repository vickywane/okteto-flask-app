FROM python:3.7-alpine as python

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /flask_app

ENV FLASK_APP=app.py
COPY . .
RUN pytest

