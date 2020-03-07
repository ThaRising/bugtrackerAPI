from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import IssueController
from .comment import rest_model as comment
from .tag import rest_model as tag
from . import CollectionFactory, ItemFactory
from application.models import data_models

api = Namespace("issues", description="Issue Resource Endpoint")
controller = IssueController

rest_model = api.model("Issue", {
    "id": flask_fields.Integer(),
    "title": flask_fields.String(),
    "tags": flask_fields.Nested(tag, skip_none=False),
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
    "tags": fields.List(fields.Int(), required=False),
    "reporter": fields.Int(validate=lambda v: v > 0, required=True),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v > 0, required=False),
    "status": fields.Int(validate=lambda v: data_models.validate_status(v), required=False),
    "priority": fields.Int(validate=lambda v: data_models.validate_priority(v), required=False)
}

json_args_patch = {
    "title": fields.Str(validate=validate.Length(min=1), required=False),
    "tags": fields.List(fields.Int(), required=False),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v >= 0, required=False),
    "status": fields.Int(validate=lambda v: v >= 0, required=False),
    "priority": fields.Int(validate=lambda v: v >= 0, required=False)
}


@api.route("/")
@api.response(422, "Bad formatting in Arguments or bad headers")
class IssueCollection(Resource):
    @api.response(200, "Request successfully executed")
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @use_kwargs(collection.query_args, locations=("query",))
    def get(self, **kwargs):
        return collection.get(**kwargs)

    @api.response(201, "Object has been successfully created")
    @api.param("title", "Visible title of the Issue", required=True, _in="body", example="Pls do this!")
    @api.param("reporter", "Database ID of the reporting user", required=True, _in="body", example=1)
    @api.param("assignee", "Database ID of the assigned user", _in="body", example=2)
    @api.param("description", "Issue description", _in="body", example="Hey X, please do this!")
    @api.param("type", "Database ID of the issue type", _in="body", example=2, default=1, enum=data_models.TYPE)
    @api.param("status",
               "Integer corresponding to the issues status", _in="body", example=2, default=1, enum=data_models.STATUS)
    @api.param("priority", "Integer corresponding to the issues priority level",
               _in="body", example=2, default=1, enum=data_models.PRIORITY)
    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return collection.post(**kwargs)


@api.route("/<string:issue_id>")
@api.param("issue_id", "May be any valid identifier for an Issue", _in="path")
@api.response(200, "Request successfully executed")
@api.response(422, "Bad formatting in Arguments or bad headers")
@api.response(500, "Unknown server error during deletion")
class TagItem(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @api.param("filter", "Used to specify the type of tag identifier, Syntax: url?filter=name", _in="query")
    @use_kwargs(item.query_args, locations=("query",))
    def get(self, issue_id: str, **kwargs):
        return item.get(issue_id, **kwargs)

    @api.param("issue_id", "Database ID of the Issue to be modified", _in="path")
    @api.param("name", "Visible name of the Tag", _in="body", example="Updated Frontend")
    @api.param("background", "Tag background color, 6 digit hex color value without a #", _in="body", example="212121")
    @api.param("color", "Tag foreground color, 6 digit hex color value without a #", _in="body", example="f0f0f0")
    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, issue_id: str, **kwargs):
        return item.patch(issue_id, **kwargs)

    @api.param("issue_id", "Database ID of the Issue to be deleted", _in="path")
    def delete(self, issue_id: str):
        return item.delete(issue_id)
