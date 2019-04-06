import os
import datetime

import pytest

from app import create_app
from app.model import db, Ticket

app = None


@pytest.fixture()
def client():
    test_config = {
        'TESTING': True,
        'DEBUG': True
    }

    global app
    app = create_app(test_config=test_config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Add one ticket for testing purposes
        ticket = Ticket(
            title='Test',
            description='Test',
            client='Client A',
            product_area='Policies',
            priority=1,
            target_date=datetime.datetime.utcnow().date()
        )
        db.session.add(ticket)
        db.session.commit()
    client = app.test_client()

    yield client


def test_get_ticket_success(client):
    """Should get ticket with given ID"""
    res = client.get('/api/tickets/1')
    assert(res.status_code == 200)

    ticket = res.json['data'];
    assert(ticket['title'] == 'Test')
    assert(ticket['description'] == 'Test')
    assert(ticket['id'] == 1)


def test_get_ticket_404_error(client):
    """Should return 404 if ticket is absent"""
    # first confirm ticket doesn't exist
    with app.app_context():
        ticket = Ticket.query.get(4)
        assert(ticket is None)

    # now try to get ticket via REST
    res = client.get('/api/tickets/4')
    assert(res.status_code == 404)

    res_message = res.json['message']
    assert(res_message == 'Ticket does not exist')


def test_get_all_tickets(client):
    """Get all tickets in database. Currently just 1"""
    res = client.get('/api/tickets')
    assert(res.status_code == 200)

    tickets = res.json['data']
    assert(len(tickets) == 1)


def test_delete_ticket_if_exist(client):
    """Should delete a ticket"""
    # Confirm ticket is present
    with app.app_context():
        ticket = Ticket.query.get(1)
        assert(ticket is not None)

    # Now delete ticket
    res = client.delete('/api/tickets/1')
    assert(res.status_code == 204)

    # Now confirm ticket was deleted
    with app.app_context():
        ticket = Ticket.query.get(1)
        assert(ticket is None)


def test_delete_ticket_404_error(client):
    """Should return 404 if trying to delete a ticket that doesn't exist"""
    # First we make sure ticket with ID 4 doesn't exist
    with app.app_context():
        ticket = Ticket.query.get(4)
        assert(ticket is None)

    # Now try to delete ticket with ID 4
    res = client.delete('/api/tickets/4')
    assert(res.status_code == 404)

    res_message = res.json['message']
    assert(res_message == 'Ticket does not exist')


def test_create_ticket(client):
    """Should create ticket if it doesn't exist"""
    # We currently have 1 ticket. Let's verify
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)

    res = client.post('/api/tickets', json={
        'title': 'New Ticket',
        'description': 'New Ticket',
        'client': 'Client A',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-09-09'
    })

    assert(res.status_code == 201)

    created = res.json['data']
    assert(created['title'] == 'New Ticket')

    # We should now have 2 tickets in the system
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 2)


def test_post_ticket_exists_error(client):
    """Should return 400 if trying to create a ticket that already exists"""
    # We'll try to add a ticket with title 'Test'. This should not work
    # first let's confirm this ticket exist and it's the only ticket
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)
        assert(tickets[0].title == 'Test')

    # Now let's try to add a ticket with title 'Test
    res = client.post('/api/tickets', json={
        'title': 'Test',
        'description': 'New Ticket',
        'client': 'Client A',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-09-09'
    })

    assert(res.status_code == 400)

    res_message = res.json['message']
    assert(res_message == 'Ticket already exists')

    # Now let's very that no ticket was added
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)


def test_post_no_data_provided_error(client):
    """Should return 400 if no data is sent with the request"""

    # Let's confirm there's just 1 ticket in the system
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)

    # make a post with empty body
    res = client.post('/api/tickets', json={})

    assert(res.status_code == 400)

    res_message = res.json['message']
    assert(res_message == 'No input data provided')

    # Now let's very that no ticket was added
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)

