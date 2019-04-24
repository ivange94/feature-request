# Feature Request

Simple Feature Request App. This app let's employees create feature requests after speaking with clients.

### Prerequisites

Docker and Docker Compose

## Run Application locally

### Run Backend Service

Move into the feature-request-api folder and run

`python3 -m venv venv`

`. venv/bin/activate`

`pip install -r requirements.txt`

`export FLASK_APP=app`

`flask run`

### Run Frontend Service

Move to web-app folder and execute

`python -m SimpleHTTPServer`

Access the web app at https://localhost:8000/

**NOTE** Here `python` refers to the python2 binary while `python3` refers to the python3 binary.

## Run Tests

Move to the feature-request-api folder and run

`pytest`

## Deploy

**NB** If not deploying locally, please change [baseUrl](https://github.com/ivange94/feature-request/blob/master/web-app/js/app.js#L2) to point to your backend server else the frontend will try query the wrong server when deployed.

Make sure you have [Docker Compose](https://docs.docker.com/compose/) installed.

* Clone the project `git clone https://github.com/ivange94/feature-request.git`
* cd feature-request
* docker-compose up

Visit http://0.0.0.0:8000/ to access the frontend web app.

If you would like to play with the backend API then you can access it at http://0.0.0.0:5000/

The Backend Service will be running at 
Endpoints exposed 

1) **POST** http://0.0.0.0:5000/api/tickets  Creates a new Ticket(feature request). Sample JSON

```json
{
	"title": "Test",
	"description": "Test",
	"client": "Client C",
	"product_area": "Policies",
	"target_date": "2019-09-19",
	"priority": 7
}
```

2) **PUT** http://0.0.0.0:5000/api/tickets updates a ticket. Pass in the ticket in the json body.

3) **GET** http://0.0.0.0:5000/api/tickets Get's a list of tickets

4) **GET** http://0.0.0.0:5000/api/tickets/{ID} Get's a single ticket with given ID

5) **DELETE** http://0.0.0.0:5000/api/tickets/{ID} Delete's ticket with ID.

## Built With

* [Flask](http://flask.pocoo.org/) - Backend API was built in Flask with extensions.
* [jQuery](https://jquery.com/) - jQuery was used in the frontend to make ajax calls to the backend
* [SQLite](https://www.sqlite.org/index.html) Database used. 
* [SQLAlchemy](https://www.sqlalchemy.org/) ORM

## Demo

A demo of this app can be accessed here [Feature Request](http://35.231.208.239:8080)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
