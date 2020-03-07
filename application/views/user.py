from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import UserController

api = Namespace("users", description="User Resource Endpoint")

controller = UserController

user = api.model("User", {
    "id": flask_fields.Integer(),
    "name": flask_fields.String()
})

json_args_post = {
    "name": fields.Str(validate=validate.Length(min=1), required=True)
}


@api.route("/")
class users(Resource):
    @api.marshal_with(user)
    def get(self):
        return [dict(i) for i in controller().get({})]

    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return dict(controller().create(kwargs))


query_args = {
    "filter": fields.Str(validate=validate.Length(min=2), missing="id")
}

json_args_patch = {
    "name": fields.Str(validate=validate.Length(min=1), required=False)
}


@api.route("/<string:user_id>")
@api.param("user_id", "May be any valid identifier for a User")
@api.response(404, "Not a valid identifier")
class User(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, user_id: str, **kwargs):
        filter_by = kwargs.get("filter")

        @api.marshal_with(user)
        def response(identifier: str):
            return [dict(i) for i in controller().get({filter_by: identifier})]
        return response(user_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, user_id: str, **kwargs):
        return dict(controller().update(int(user_id), kwargs))

    def delete(self, user_id: str):
        operation = controller().delete(int(user_id))
        return 200 if operation else 500

