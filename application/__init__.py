from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api
from sqlalchemy import exc

db = SQLAlchemy()
api = Api(
    title="OrcTracker API",
    version="1.0",
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
        api.add_namespace(comment_api, path="/comments")
        api.add_namespace(issue_api, path="/issues")
        api.add_namespace(tag_api, path="/tags")
        api.add_namespace(type_api, path="/types")
        api.add_namespace(user_api, path="/users")

        @app.after_request
        def add_headers(response):
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Headers'] = \
                "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            response.headers['Access-Control-Allow-Methods'] = "POST, GET, PATCH, DELETE"
            return response

        @api.errorhandler(exc.AmbiguousForeignKeysError)
        def handle_ambiguous_foreign_keys(error):
            return {'error': 'ERR_AMBIGUOUS_FOREIGN_KEYS',
                    'message': 'Some of the Database IDs that were provided match no entries in the database.'}, 400

        return app


__all__ = ["db", "api", "create_app"]
