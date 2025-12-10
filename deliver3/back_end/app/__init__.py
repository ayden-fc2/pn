import os
from flask import Flask
from flask_cors import CORS
from . import db
from .api import auth, account, appointments, challenges, summary, metrics, family, delegation, invitations, reports

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'health_track.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(appointments.bp)
    app.register_blueprint(challenges.bp)
    app.register_blueprint(summary.bp)
    app.register_blueprint(metrics.bp)
    app.register_blueprint(family.bp)
    app.register_blueprint(delegation.bp)
    app.register_blueprint(invitations.bp)
    app.register_blueprint(reports.bp)

    return app
