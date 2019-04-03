from flask_restful import Resource, Api


class TicketListResource(Resource):
    def get(self):
        return {'hello': 'world'}


class TicketResource(Resource):
    def get(self, id):
        return {'id': id}