# usbmissile

Missile Control: missile_center.py (Python)
Missile REST API: api/ (Python API-Hour)
Missile Frontend: frontend/ (AngularJS)


REST API
API Hour Installation: http://pythonhosted.org/api_hour/installation.html
To start rest api got in the restapi folder
Execute the following command : api_hour missile_api:Container

you can then access your Rest API using curl :
curl -i http:/7localhost:8000/left
curl -i http:/7localhost:8000/right
curl -i http:/7localhost:8000/up
curl -i http:/7localhost:8000/down
curl -i http:/7localhost:8000/fire
curl -i http:/7localhost:8000/fireall
curl -i http:/7localhost:8000/stopf
