# Feature Request

Simple Feature Request App. This app let's employees create feature requests after speaking with clients.

### Prerequisites

Docker and Docker Compose

## Installing

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

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
