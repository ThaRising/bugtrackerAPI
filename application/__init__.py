from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(env_type: str = "dev"):
    app = Flask(__name__, instance_relative_config=False)
    if env_type == "dev":
        app.config.from_object("application.config.DevelopmentConfig")
    elif env_type == "test":
        app.config.from_object("application.config.TestingConfig")
    else:
        app.config.from_object("application.config.Config")

    db.init_app(app)

    with app.app_context():
        from . import views
        from . import models
        app.add_url_rule("/api/tags", view_func=views.TagEndpoint.as_view("tag_endpoint"))
        app.add_url_rule("/api/tags/<item_name>", view_func=views.TagItemEndpoint.as_view("tag_item_endpoint"))

        return app
