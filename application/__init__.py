from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

db = SQLAlchemy()
api = Api(
    title="OrcTracker API",
    version="0.4a",
    description="OrcTracker Project REST API."
)


def create_app(env_type: str = "dev"):
    app = Flask(__name__, instance_relative_config=False)
    if env_type == "dev":
        app.config.from_object("application.config.DevelopmentConfig")
    elif env_type == "test":
        app.config.from_object("application.config.TestingConfig")
    else:
        app.config.from_object("application.config.Config")

    db.init_app(app)
    api.init_app(app)

    with app.app_context():
        from .views.tag import api as tag_namespace
        api.add_namespace(tag_namespace, path="/api/tags")
        from . import models

        return app
