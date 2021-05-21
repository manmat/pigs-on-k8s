FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN mkdir -p /app
WORKDIR /app

COPY ./src/ /app/
ENV FLASK_APP=player.py

CMD flask run -h 0.0.0.0 -p 5000
