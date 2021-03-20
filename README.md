# REGISTRATIONAPI
A REST API for registration

## Configuration

View config/config.json

## Docker containers deployment

$ docker-compose up -d

To view results, 4 docker containers are running:

$ docker images

$ docker ps

## API Html Docs

API html docs is served in APIregistration index page http://172.18.0.5:5000

## Tests

$ curl -d '{"email":"user01@gmail.com", "password":"myPass*1"}' -H "Content-Type: application/json" -X POST http://172.18.0.5:5000/api/register

View activation code in smtpapi service page. Example: http://172.18.0.4:5001/

Send activation code to activate:

$ curl -d '{"code": 1783}' -H "Content-Type: application/json" -H "Authorization: Basic $(echo -n user01@gmail.com:myPass*1 | base64)" -X POST http://172.18.0.5:5000/api/activate

## Source code directory

Source code find in `registrationAPI` directory.

**To run in dev:**

$ python3 -m venv venv

$ . venv/bin/activate

$ pip install -r requirements.txt

$ export FLASK_ENV="development"

$ flask run

**To run unittests:**

$ pip install tox

$ pip install -r test/test-requirements.txt

$ tox

## Docker images

https://hub.docker.com/repository/docker/tdmai/registrationapi

https://hub.docker.com/repository/docker/tdmai/smtpapi




