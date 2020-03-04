from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import CommentController

api = Namespace("comments", description="Comment Resource Endpoint")

controller = CommentController

comment = api.model("Comment", {
    "id": flask_fields.Integer(),
    "parent_id": flask_fields.Integer(),
    "author": flask_fields.Integer(),
    "content": flask_fields.String(),
    "created": flask_fields.String(attribute="created_on")
})

query_args = {
    "fields": fields.DelimitedList(fields.Str())
}

json_args_post = {
    "parent_id": fields.Int(validate=lambda v: v > 0, required=True),
    "author": fields.Int(validate=lambda v: v > 0, required=True),
    "content": fields.Str(validate=validate.Length(min=1), required=True)
}


@api.route("/")
class Comments(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))

        @api.marshal_with(comment, mask=mask)
        def response():
            return [dict(i) for i in controller().get({})]
        return response()

    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return dict(controller().create(kwargs))


query_args = {
    "fields": fields.DelimitedList(fields.Str()),
    "filter": fields.Str(validate=validate.Length(min=2), missing="id")
}

json_args_patch = {
    "content": fields.Str(validate=validate.Length(min=1), required=True)
}


@api.route("/<string:comment_id>")
@api.param("comment_id", "May be any valid identifier for a Comment")
@api.response(404, "Not a valid identifier")
class Comment(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, tag_id: str, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))
        filter_by = kwargs.get("filter")

        @api.marshal_with(comment, mask=mask)
        def response(identifier: str):
            return [dict(i) for i in controller().get({filter_by: identifier})]
        return response(tag_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, tag_id: str, **kwargs):
        return dict(controller().update(int(tag_id), kwargs))

    def delete(self, tag_id: str):
        operation = controller().delete(int(tag_id))
        return 200 if operation else 500

