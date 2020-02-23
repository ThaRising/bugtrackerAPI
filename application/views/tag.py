from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import TagController

api = Namespace("tags", description="Tag Resource Endpoint")


tag = api.model("Tag", {
    "id": flask_fields.Integer(),
    "name": flask_fields.String(),
    "background": flask_fields.String(),
    "color": flask_fields.String()
})

query_args = {
    "fields": fields.DelimitedList(fields.Str())
}

json_args_post = {
    "name": fields.Str(validate=validate.Length(min=1), required=True),
    "background": fields.Str(validate=lambda v: len(v) == 6, required=False),
    "color": fields.Str(validate=lambda v: len(v) == 6, required=False)
}


@api.route("/")
class Tags(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))

        @api.marshal_with(tag, mask=mask)
        def response():
            return [dict(i) for i in TagController().get({})]
        return response()

    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return dict(TagController().create(kwargs))


query_args = {
    "fields": fields.DelimitedList(fields.Str()),
    "filter": fields.Str(validate=validate.Length(min=2), missing="id")
}

json_args_patch = {
    "name": fields.Str(validate=validate.Length(min=1), required=False),
    "background": fields.Str(validate=lambda v: len(v) == 6, required=False),
    "color": fields.Str(validate=lambda v: len(v) == 6, required=False)
}


@api.route("/<string:tag_id>")
@api.param("tag_id", "May be any valid identifier for a Tag")
@api.response(404, "Not a valid identifier")
class Tag(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, tag_id: str, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))
        filter_by = kwargs.get("filter")

        @api.marshal_with(tag, mask=mask)
        def response(identifier: str):
            return [dict(i) for i in TagController().get({filter_by: identifier})]
        return response(tag_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, tag_id: str, **kwargs):
        return dict(TagController().update(int(tag_id), kwargs))

    def delete(self, tag_id: str):
        operation = TagController().delete(int(tag_id))
        return 200 if operation else 500

