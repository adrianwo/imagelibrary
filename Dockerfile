FROM python:3.9.5-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc python3-dev netcat \
    && pip install psycopg2==2.9.9 

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]