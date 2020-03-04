from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

db = SQLAlchemy()
api = Api(
    title="OrcTracker API",
    version="0.5a",
    description='OrcTracker Project REST API'
                '<style>.models {display: none !important}</style>'
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
        from .views import comment_api, issue_api, tag_api, type_api, user_api
        api.add_namespace(comment_api, path="/api/comments")
        api.add_namespace(issue_api, path="/api/issues")
        api.add_namespace(tag_api, path="/api/tags")
        api.add_namespace(type_api, path="/api/types")
        api.add_namespace(user_api, path="/api/users")
        from . import models

        return app


__all__ = ["db", "api", "create_app"]
