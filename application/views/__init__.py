from flask_restplus import marshal
from flask import make_response
from webargs import fields, validate


class CollectionFactory:
    query_args = {
        "fields": fields.DelimitedList(fields.Str())
    }

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model

    def get(self, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))
        return marshal([dict(i) for i in self.controller().get({})], self.model, mask=mask), 200

    def post(self, **kwargs):
        return marshal(dict(self.controller().create(kwargs)), self.model), 201


class ItemFactory:
    query_args = {
        "fields": fields.DelimitedList(fields.Str()),
        "filter": fields.Str(validate=validate.Length(min=2), missing="id")
    }

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model

    def get(self, identifier, **kwargs):
        mask = "*" if not kwargs.get("fields") else ",".join(kwargs.get("fields"))
        filter_by = kwargs.get("filter")
        return marshal([dict(i) for i in self.controller().get({filter_by: identifier})], self.model, mask=mask), 200

    def patch(self, identifier, **kwargs):
        return marshal([dict(i) for i in self.controller().update(int(identifier), kwargs)], self.model), 200

    def delete(self, identifier):
        operation = self.controller().delete(int(identifier))
        return make_response("", 200) if operation else make_response("", 404)


from .comment import api as comment_api
from .issue import api as issue_api
from .type import api as type_api
from .user import api as user_api
from .tag import api as tag_api

__all__ = ["comment_api", "issue_api", "tag_api", "type_api", "user_api"]
