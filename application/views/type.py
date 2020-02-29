from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import TypeController

api = Namespace("types", description="Type Resource Endpoint")

controller = TypeController


type = api.model("Type", {
    "id": flask_fields.Integer(),
    "name": flask_fields.String()
})

json_args_post = {
    "name": fields.Str(validate=validate.Length(min=1), required=True)
}


@api.route("/")
class Types(Resource):
    @api.marshal_with(type)
    def get(self):
        return [dict(i) for i in Typ().get({})]

    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return dict(controller().create(kwargs))


query_args = {
    "filter": fields.Str(validate=validate.Length(min=2), missing="id")
}

json_args_patch = {
    "name": fields.Str(validate=validate.Length(min=1), required=False),
}


@api.route("/<string:type_id>")
@api.param("type_id", "May be any valid identifier for a Type")
@api.response(404, "Not a valid identifier")
class Type(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, type_id: str, **kwargs):
        filter_by = kwargs.get("filter")

        @api.marshal_with(type)
        def response(identifier: str):
            return [dict(i) for i in controller().get({filter_by: identifier})]
        return response(type_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, type_id: str, **kwargs):
        return dict(controller().update(int(type_id), kwargs))

    def delete(self, type_id: str):
        operation = controller().delete(int(type_id))
        return 200 if operation else 500

