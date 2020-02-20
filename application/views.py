from application import db
from flask import jsonify, request, make_response
from flask import current_app as app
from flask.wrappers import Response
from werkzeug.wrappers import BaseResponse
import application.controllers as c
from werkzeug.exceptions import HTTPException
from typing import Union, Tuple
from flask.views import MethodView


# Helper-Functions

def split_query() -> Tuple[list, dict]:
    """
    :return: Query-String split by key-only pairs (keys) and key-value pairs (pairs)
    """
    keys = [j for j in request.args.keys() if not request.args.get(j)]
    pairs = {j: request.args.get(j) for j in request.args.keys() if request.args.get(j)}
    return keys, pairs


def response_maker(content: Union[db.Model, list], code: int) -> Response:
    """
    :param content: Any amount of model instances
    :param code: Desired response code
    :return: Flask Response object containing a json version of the content parameter and the appropriate status code
    """
    code = 404 if code is 200 and not content else code
    if type(content) == list and isinstance(content[0], db.Model):
        content = [dict(i) for i in content]
    elif isinstance(content, db.Model):
        content = dict(content)
    return make_response(jsonify(content), code)


# Error-Handling

@app.errorhandler(Exception)
def handle_error(error_: Exception) -> BaseResponse:
    """
    :param error_: Python Exception object
    :return: werkzeug BaseResponse object containing a properly formatted json version of the error
    """
    code = 500
    if isinstance(error_, HTTPException):
        code = error_.code
    return jsonify(error=str(error_)), code


# Endpoints

class TagEndpoint(MethodView):
    """ /api/tags """
    def __init__(self):
        self.controller = c.TagController

    def get(self) -> BaseResponse:
        """ GET /api/tags?query """
        if not request.args:
            content = self.controller().get_all()
            return response_maker(content, 200)
        else:
            keys, pairs = split_query()
            models = self.controller().get_all()
            content = self.controller().limit_return_parameters(models, keys)[:pairs.get("size")]
            return response_maker(content, 200)

    def post(self) -> BaseResponse:
        """ POST /api/tags content-type: application/json """
        content = self.controller().create(request.get_json())
        return response_maker(content, 201)


class TagItemEndpoint(MethodView):
    """ /api/tags/<item_name> """
    def __init__(self):
        self.controller = c.TagController

    def get(self, item_name: str) -> BaseResponse:
        """ GET /api/tags/<item_name>?query """
        if not request.args:
            content = self.controller().get_by_primary(int(item_name))
            return response_maker(content, 200)
        else:
            keys, pairs = split_query()
            if pairs.get("filter") == "id":
                content = self.controller().get_by_primary(int(item_name))
                content = self.controller().limit_return_parameters(content, keys)
                return response_maker(content, 200)
            elif pairs.get("filter") == "name":
                content = self.controller().get_by_name(item_name)
                content = self.controller().limit_return_parameters(content, keys)
                return response_maker(content, 200)
            elif pairs.get("filter"):
                content = self.controller().get_by_attr({pairs.get("filter"): item_name})
                content = self.controller().limit_return_parameters(content, keys)
                return response_maker(content, 200)

    def patch(self, item_name: int) -> BaseResponse:
        """ PATCH /api/tags/<item_name> """
        content = self.controller().update_one(int(item_name), request.get_json())
        return response_maker(content, 200)

    def delete(self, item_name: int) -> BaseResponse:
        """ DELETE /api/tags/<item_name> """
        content = self.controller().delete_one(int(item_name))
        if not content:
            return response_maker(content, 404)
        else:
            return response_maker(content, 204)


@app.route("/api", methods=["GET"])
def root_get() -> str:
    return make_response("API operational.", 200)
