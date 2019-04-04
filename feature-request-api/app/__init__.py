import os

from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRETE_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    CORS(app)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.model import db
    db.init_app(app)

    from flask_restful import Api
    api = Api(app)

    from app.model import migrate
    migrate.init_app(app=app, db=db)

    from app.resource import TicketListResource, TicketResource
    api.add_resource(TicketListResource, '/api/tickets')
    api.add_resource(TicketResource, '/api/tickets/<int:id>')

    return app
