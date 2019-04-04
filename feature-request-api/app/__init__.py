import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRETE_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'app.db'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

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

    from flask_migrate import Migrate
    migrate = Migrate(app, db)

    with app.app_context():
        db.drop_all()
        db.create_all()

    from app.resource import TicketListResource, TicketResource
    api.add_resource(TicketListResource, '/api/tickets')
    api.add_resource(TicketResource, '/api/tickets/<int:id>')

    return app
