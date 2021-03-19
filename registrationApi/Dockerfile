FROM python:3.9.2

COPY . /usr/src/registrationapi/
# install dependencies
COPY ./requirements.txt /usr/src/registrationapi/requirements.txt

WORKDIR /usr/src/registrationapi

RUN pip install -r ./requirements.txt

RUN cd /usr/src/registrationapi/docs && make html

WORKDIR /usr/src/registrationapi

EXPOSE 5000

CMD gunicorn wsgi:app --bind 0.0.0.0:5000 --max-requests 10000 --timeout 5