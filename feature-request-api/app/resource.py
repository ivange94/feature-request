from flask import request
from flask_restful import Resource
from app.model import Ticket, TicketSchema, db

ticket_schema = TicketSchema()


class TicketListResource(Resource):
    def get(self):
        ticket_schema = TicketSchema(many=True)
        tickets = ticket_schema.dump(Ticket.query.all()).data
        return {'status': 'success', 'data': tickets}, 200

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = ticket_schema.load(json_data)
        if errors:
            return errors, 422

        ticket = Ticket.query.filter_by(title=data['title']).first()
        if ticket:
            return {'message': 'Ticket already exists'}, 400

        ticket = Ticket(
            title=data['title'],
            description=data['description'],
            client=data['client'],
            target_date=data['target_date'],
            product_area=data['product_area'],
            priority=data['priority']
        )

        db.session.add(ticket)
        db.session.commit()

        result = ticket_schema.dump(ticket).data
        return {'status': 'success', 'data': result}, 201

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = ticket_schema.load(json_data)
        if errors:
            return errors, 422

        ticket = Ticket.query.get(data['id'])
        if not ticket:
            return {'message': 'Ticket does not exist'}, 400

        ticket.title = data['title']
        ticket.description = data['description']
        ticket.client = data['client']
        ticket.product_area = data['product_area']
        ticket.priority = data['priority']
        ticket.target_date = data['target_date']

        db.session.commit()

        result = ticket_schema.dump(ticket).data

        return {'status': 'success', 'data': result}, 204


class TicketResource(Resource):
    def get(self, id):

        return Ticket.query.get(id), 404
