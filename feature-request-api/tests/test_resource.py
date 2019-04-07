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


def test_create_ticket_should_reorder_ticket_priority_for_client(client):
    # We currently have 1 ticket for Client A with priority 1
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 1)
        assert(tickets[0].priority == 1)

    # Let's create a new ticket for client A with priority one.
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

    # Existing ticket's priority should have shifted to 2
    with app.app_context():
        ticket = Ticket.query.get(1) # This was the first and only ticket so we know it's ID is 1
        assert(ticket.priority == 2)


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


def test_put_should_update_ticket(client):
    with app.app_context():
        ticket = Ticket.query.get(1)
        assert(ticket.title == 'Test')

    res = client.put('/api/tickets', json={
        'id': 1,
        'title': 'Now Test 2',
        'description': 'Some ticket',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-08-09'
    })

    assert(res.status_code == 200)

    with app.app_context():
        ticket = Ticket.query.get(1)
        assert(ticket.title == 'Now Test 2')


def test_put_no_data_error(client):
    """PUT expects a json body. Return 400 error if body is not present"""

    res = client.put('/api/tickets')
    assert(res.status_code == 400)


def test_trying_to_update_a_ticket_that_does_not_exist_should_return_404(client):
    # Let's confirm that ticket with ID 4 does not exist
    with app.app_context():
        ticket = Ticket.query.get(4)
        assert(ticket is None)

    # now let's try to update ticket with ID 4
        # Now let's try to add a ticket with title 'Test
        res = client.put('/api/tickets', json={
            'id': '4',
            'title': 'Some ticket that does not exist',
            'description': 'No body',
            'client': 'Client A',
            'priority': 1,
            'product_area': 'Policies',
            'target_date': '2019-09-09'
        })

        assert(res.status_code == 404)

        res_message = res.json['message']
        assert(res_message == 'Ticket does not exist')


def test_if_updating_title_make_sure_title_is_not_already_taken(client):
    # Let's add one more ticket
    client.post('/api/tickets', json={
        'title': 'Some ticket',
        'description': 'Some ticket',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-08-09'
    })

    # let's confirm we have 2 tickets in the system
    with app.app_context():
        tickets = Ticket.query.all()
        assert(len(tickets) == 2)

    # Now let's try to edit the title of 'Some ticket' to 'Test'
    res = client.put('/api/tickets', json={
        'id': 2,
        'title': 'Test',
        'description': 'Some ticket',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-08-09'
    })

    assert(res.status_code == 400)

    res_message = res.json['message']
    assert(res_message == 'A ticket with similar title already exists')
