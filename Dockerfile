FROM python:3.9-bullseye

RUN mkdir -p /app
WORKDIR /app
RUN pip install -U Flask pony psycopg2
ADD . /app

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]