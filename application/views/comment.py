from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import CommentController
from . import CollectionFactory, ItemFactory

api = Namespace("comments", description="Comment Resource Endpoint")
controller = CommentController

rest_model = api.model("Comment", {
    "id": flask_fields.Integer(),
    "parent_id": flask_fields.Integer(),
    "author": flask_fields.Integer(),
    "content": flask_fields.String(),
    "created": flask_fields.String(attribute="created_on")
})

collection = CollectionFactory(controller, rest_model)
item = ItemFactory(controller, rest_model)

json_args_post = {
    "parent_id": fields.Int(validate=lambda v: v > 0, required=True),
    "author": fields.Int(validate=lambda v: v > 0, required=True),
    "content": fields.Str(validate=validate.Length(min=1), required=True)
}

json_args_patch = {
    "content": fields.Str(validate=validate.Length(min=1), required=True)
}


@api.route("/")
@api.response(200, "Request successfully executed")
@api.response(201, "Object has been successfully created")
@api.response(422, "Bad formatting in Arguments or bad headers")
class CommentCollection(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @use_kwargs(collection.query_args, locations=("query",))
    def get(self, **kwargs):
        return collection.get(**kwargs)

    @api.param("parent_id", "Database ID of the parent Issue", required=True, _in="body", example=1)
    @api.param("author", "Database ID of the authoring User", required=True, _in="body", example=3)
    @api.param("content", "Contents of the comment",
               required=True, _in="body", example="This is a nice comment, with content!")
    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return collection.post(**kwargs)


@api.route("/<string:comment_id>")
@api.param("comment_id", "May be any valid identifier for a Comment", _in="path")
@api.response(200, "Request successfully executed")
@api.response(422, "Bad formatting in Arguments or bad headers")
@api.response(500, "Unknown server error during deletion")
class CommentItem(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @api.param("filter", "Used to specify the type of comment identifier, Syntax: url?filter=name", _in="query")
    @use_kwargs(item.query_args, locations=("query",))
    def get(self, comment_id: str, **kwargs):
        return item.get(comment_id, **kwargs)

    @api.param("comment_id", "Database ID of the Comment to be modified", _in="path")
    @api.param("content", "New content of the comment", _in="body", example="This is a comment, with updated content!")
    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, comment_id: str, **kwargs):
        return item.patch(comment_id, **kwargs)

    @api.param("tag_id", "Database ID of the Comment to be deleted", _in="path")
    def delete(self, comment_id: str):
        return item.delete(comment_id)
