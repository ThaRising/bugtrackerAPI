from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import IssueController
from .comment import rest_model as comment
from . import CollectionFactory, ItemFactory

api = Namespace("issues", description="Issue Resource Endpoint")
controller = IssueController

rest_model = api.model("Issue", {
    "id": flask_fields.Integer(),
    "title": flask_fields.String(),
    "reporter": flask_fields.Integer(),
    "assignee": flask_fields.Integer(),
    "description": flask_fields.String(),
    "comments": flask_fields.Nested(comment, skip_none=False),
    "type": flask_fields.Integer(),
    "status": flask_fields.Integer(),
    "priority": flask_fields.Integer()
})

collection = CollectionFactory(controller, rest_model)
item = ItemFactory(controller, rest_model)

json_args_post = {
    "title": fields.Str(validate=validate.Length(min=1), required=True),
    "reporter": fields.Int(validate=lambda v: v > 0, required=True),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v >= 0, required=False),
    "status": fields.Int(validate=lambda v: v >= 0, required=False),
    "priority": fields.Int(validate=lambda v: v >= 0, required=False)
}

json_args_patch = {
    "title": fields.Str(validate=validate.Length(min=1), required=False),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v >= 0, required=False),
    "status": fields.Int(validate=lambda v: v >= 0, required=False),
    "priority": fields.Int(validate=lambda v: v >= 0, required=False)
}


@api.route("/")
@api.response(200, "Request successfully executed")
@api.response(201, "Object has been successfully created")
@api.response(422, "Bad formatting in Arguments or bad headers")
class IssueCollection(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @use_kwargs(collection.query_args, locations=("query",))
    def get(self, **kwargs):
        return collection.get(**kwargs)

    @api.param("title", "Visible title of the Issue", required=True, _in="body", example="Pls do this!")
    @api.param("reporter", "Database ID of the reporting user", required=True, _in="body", example=1)
    @api.param("assignee", "Database ID of the assigned user", _in="body", example=2)
    @api.param("description", "Issue description", _in="body", example="Hey X, please do this!")
    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return collection.post(**kwargs)
