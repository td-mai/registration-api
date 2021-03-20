# REGISTRATIONAPI
A REST API for registration

## Configuration

View config/config.json

## Docker containers deployment

$ docker-compose up -d

To view results, 4 docker containers are running:

$ docker images

$ docker ps

## Tests

$ curl -d '{"email":"user01@gmail.com", "password":"myPass*1"}' -H "Content-Type: application/json" -X POST http://172.18.0.5:5000/api/register

View activation code in smtpapi service page. Example: http://172.18.0.4:5001/

Send activation code to activate:

$ curl -d '{"code": 1783}' -H "Content-Type: application/json" -H "Authorization: Basic $(echo -n user01@gmail.com:myPass*1 | base64)" -X POST http://172.18.0.5:5000/api/activate





