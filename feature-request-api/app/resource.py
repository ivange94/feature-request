from flask import request
from flask_restful import Resource
from app.model import Ticket, TicketSchema, db

ticket_schema = TicketSchema()


class TicketListResource(Resource):
    def get(self):
        ticket_list_schema = TicketSchema(many=True)
        tickets = ticket_list_schema.dump(Ticket.query.all()).data
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

        title = data['title']
        description = data['description']
        client = data['client']
        target_date = data['target_date']
        product_area = data['product_area']
        priority = data['priority']

        if title and description and client and target_date and product_area and priority and priority > 0:
            new_ticket = Ticket(
                title=title,
                description=description,
                client=client,
                target_date=target_date,
                product_area=product_area,
                priority=priority
            )

            tickets = Ticket.query.filter_by(client=client).order_by(Ticket.priority).all()
            tickets.insert(new_ticket.priority - 1, new_ticket)
            for i, ticket in enumerate(tickets, 1):
                ticket.priority = i

            db.session.add(new_ticket)
            db.session.commit()

            result = ticket_schema.dump(new_ticket).data
            return {'data': result}, 201
        else:
            return {'message', 'Some fields are missing or invalid. Not Priority cannot be less than 1'}, 400

    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        data, errors = ticket_schema.load(json_data)
        if errors:
            return errors, 422

        ticket = Ticket.query.get(data['id'])
        if not ticket:
            return {'message': 'Ticket does not exist'}, 404

        similar_ticket = Ticket.query.filter_by(title=data['title']).first()
        if similar_ticket and similar_ticket is not ticket:
            return {'message': 'A ticket with similar title already exists'}, 400

        ticket.title = data['title']
        ticket.description = data['description']
        ticket.client = data['client']
        ticket.product_area = data['product_area']
        ticket.priority = data['priority']
        ticket.target_date = data['target_date']

        db.session.commit()

        result = ticket_schema.dump(ticket).data
        return {'status': 'success', 'data': result}, 200


class TicketResource(Resource):
    def get(self, id):
        ticket = Ticket.query.get(id)
        if not ticket:
            return {'message': 'Ticket does not exist'}, 404

        result = ticket_schema.dump(ticket).data
        return {'status': 'success', 'data': result}, 200

    def delete(self, id):
        ticket = Ticket.query.get(id)
        if not ticket:
            return {'message': 'Ticket does not exist'}, 404

        db.session.delete(ticket)
        db.session.commit()
        return {'message': 'Deleted'}, 204