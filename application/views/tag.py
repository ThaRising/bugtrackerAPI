from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import TagController
from . import Collection

api = Namespace("tags", description="Tag Resource Endpoint")

controller = TagController

tag = api.model("Tag", {
    "id": flask_fields.Integer(),
    "name": flask_fields.String(),
    "background": flask_fields.String(),
    "color": flask_fields.String()
})

json_args_post = {
    "name": fields.Str(validate=validate.Length(min=1), required=True),
    "background": fields.Str(validate=lambda v: len(v) == 6, required=False),
    "color": fields.Str(validate=lambda v: len(v) == 6, required=False)
}


@api.route("/")
class Tags(Resource, Collection):
    @use_kwargs(Collection.query_args, locations=("query",))
    def get(self, **kwargs):
        @api.marshal_with(tag, mask=Collection.mask(kwargs))
        def response():
            return [dict(i) for i in controller().get({})]
        return response()

    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        @api.marshal_with(tag)
        def response():
            return dict(controller().create(kwargs))
        return response()


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
            return [dict(i) for i in controller().get({filter_by: identifier})]
        return response(tag_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, tag_id: str, **kwargs):
        return dict(controller().update(int(tag_id), kwargs))

    def delete(self, tag_id: str):
        operation = controller().delete(int(tag_id))
        return 200 if operation else 500

