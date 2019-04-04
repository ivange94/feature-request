from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    client = db.Column(db.String, nullable=False)
    target_date = db.Column(db.Date, nullable=False)
    product_area = db.Column(db.String, nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Ticket {}>'.format(self.title)


class TicketSchema(ma.Schema):
    id = fields.Integer()
    title = fields.String(required=True)
    description = fields.String(required=True)
    client = fields.String(required=True)
    target_date = fields.Date(required=True)
    product_area = fields.String(required=True)
    priority = fields.Integer(required=True)
