from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import IssueController
from .comment import comment

api = Namespace("issues", description="Issue Resource Endpoint")

controller = IssueController

issue = api.model("Issue", {
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

query_args = {
    "fields": fields.DelimitedList(fields.Str())
}

json_args_post = {
    "title": fields.Str(validate=validate.Length(min=1), required=True),
    "reporter": fields.Int(validate=lambda v: v > 0, required=True),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v >= 0, required=False),
    "status": fields.Int(validate=lambda v: v >= 0, required=False),
    "priority": fields.Int(validate=lambda v: v >= 0, required=False)
}


@api.route("/")
@api.doc(post={"params": {"id": "test"}})
@api.response(422, "u succ")
class Issues(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))

        @api.marshal_with(issue, mask=mask)
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
    "title": fields.Str(validate=validate.Length(min=1), required=False),
    "assignee": fields.Int(validate=lambda v: v > 0, required=False),
    "description": fields.Str(required=False),
    "type": fields.Int(validate=lambda v: v >= 0, required=False),
    "status": fields.Int(validate=lambda v: v >= 0, required=False),
    "priority": fields.Int(validate=lambda v: v >= 0, required=False)
}


@api.route("/<string:issue_id>")
@api.param("issue_id", "May be any valid identifier for an Issue")
@api.response(404, "Not a valid identifier")
class Issue(Resource):
    @use_kwargs(query_args, locations=("query",))
    def get(self, issue_id: str, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))
        filter_by = kwargs.get("filter")

        @api.marshal_with(issue, mask=mask)
        def response(identifier: str):
            return [dict(i) for i in controller().get({filter_by: identifier})]
        return response(issue_id)

    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, issue_id: str, **kwargs):
        return dict(controller().update(int(issue_id), kwargs))

    def delete(self, issue_id: str):
        operation = controller().delete(int(issue_id))
        return 200 if operation else 500

