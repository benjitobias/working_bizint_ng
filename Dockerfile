FROM python:3.11.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY bizint_ng/requirements.txt ./
RUN pip install -r requirements.txt

#COPY bizint_ng ./

