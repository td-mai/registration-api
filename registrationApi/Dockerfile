FROM python:3.9.2

# set environment variables
ENV FLASK_ENV production
ENV FLASK_RUN_PORT 5000
ENV SECRET_KEY '8wt#&^6u+xZA(LOfBwJL'
 
COPY . /usr/src/registrationapi/
# install dependencies
COPY ./requirements.txt /usr/src/registrationapi/requirements.txt

WORKDIR /usr/src/registrationapi

RUN pip install -r ./requirements.txt

RUN cd /usr/src/registrationapi/docs && make html

WORKDIR /usr/src/registrationapi

ENV CONFIG_FILE /usr/src/registrationapi/config.json

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:5000 wsgi:app --max-requests 10000 --timeout 5