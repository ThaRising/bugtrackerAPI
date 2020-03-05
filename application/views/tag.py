from flask_restplus import Resource, Namespace
from flask_restplus import fields as flask_fields
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from application.controllers import TagController
from . import CollectionFactory, ItemFactory

api = Namespace("tags", description="Tag Resource Endpoint")
controller = TagController

rest_model = api.model("Tag", {
    "id": flask_fields.Integer(),
    "name": flask_fields.String(),
    "background": flask_fields.String(),
    "color": flask_fields.String()
})

collection = CollectionFactory(controller, rest_model)
item = ItemFactory(controller, rest_model)

json_args_post = {
    "name": fields.Str(validate=validate.Length(min=1), required=True),
    "background": fields.Str(validate=lambda v: len(v) == 6, required=False),
    "color": fields.Str(validate=lambda v: len(v) == 6, required=False)
}

json_args_patch = {
    "name": fields.Str(validate=validate.Length(min=1), required=False),
    "background": fields.Str(validate=lambda v: len(v) == 6, required=False),
    "color": fields.Str(validate=lambda v: len(v) == 6, required=False)
}


@api.route("/")
@api.response(200, "Request successfully executed")
@api.response(201, "Object has been successfully created")
@api.response(422, "Bad formatting in Arguments or bad headers")
class TagCollection(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @use_kwargs(collection.query_args, locations=("query",))
    def get(self, **kwargs):
        return collection.get(**kwargs)

    @api.param("name", "Visible name of the Tag", required=True, _in="body", example="Frontend")
    @api.param("background", "Tag background color, 6 digit hex color value without a #", _in="body", example="ffffff")
    @api.param("color", "Tag foreground color, 6 digit hex color value without a #", _in="body", example="000000")
    @use_kwargs(json_args_post, locations=("json",))
    def post(self, **kwargs):
        return collection.post(**kwargs)


@api.route("/<string:tag_id>")
@api.param("tag_id", "May be any valid identifier for a Tag", _in="path")
@api.response(200, "Request successfully executed")
@api.response(422, "Bad formatting in Arguments or bad headers")
@api.response(500, "Unknown server error during deletion")
class TagItem(Resource):
    @api.param("fields", "Used to filter returned fields by name, Syntax: url?fields=id,name", _in="query")
    @api.param("filter", "Used to specify the type of tag identifier, Syntax: url?filter=name", _in="query")
    @use_kwargs(item.query_args, locations=("query",))
    def get(self, tag_id: str, **kwargs):
        return item.get(tag_id, **kwargs)

    @api.param("tag_id", "Database ID of the Tag to be modified", _in="path")
    @api.param("name", "Visible name of the Tag", _in="body", example="Updated Frontend")
    @api.param("background", "Tag background color, 6 digit hex color value without a #", _in="body", example="212121")
    @api.param("color", "Tag foreground color, 6 digit hex color value without a #", _in="body", example="f0f0f0")
    @use_kwargs(json_args_patch, locations=("json",))
    def patch(self, tag_id: str, **kwargs):
        return item.patch(tag_id, **kwargs)

    @api.param("tag_id", "Database ID of the Tag to be deleted", _in="path")
    def delete(self, tag_id: str):
        return item.delete(tag_id)
