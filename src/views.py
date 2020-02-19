from src import app
from flask import jsonify, request, make_response
from werkzeug.wrappers import BaseResponse
import src.controllers as c
from werkzeug.exceptions import HTTPException
from typing import Union, Tuple
from flask.views import MethodView


# Helpers

def split_query() -> Tuple[list, int]:
    limit_params = [j for j in request.args.keys() if not request.args.get(j)]
    limit_size = int(request.args.get("size")) if request.args.get("size") else None
    return limit_params, limit_size


# Error Handling

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


# Endpoints

class TagEndpoint(MethodView):
    """ /api/tags """
    def get(self) -> BaseResponse:
        if not request.args:
            return make_response(jsonify(str(c.TagController().get_all())), 200)
        else:
            limit_params, limit_size = split_query()
            models = c.TagController().get_all()
            info = c.TagController().limit_return_parameters(models, limit_params)[:limit_size]
            return make_response(jsonify(info), 200)

    def post(self):
        return make_response(jsonify(str(c.TagController().create(request.get_json()))), 201)


class TagItemEndpoint(MethodView):
    """ /api/tags/<item_name> """
    def get(self, item_name: int) -> BaseResponse:
        return make_response(jsonify(str(c.TagController().get_by_primary(item_name))), 200)

    def patch(self, item_name: int) -> BaseResponse:
        return make_response(jsonify(str(c.TagController().update_one(int(item_name), request.get_json()))), 200)

    def delete(self, item_name: int) -> BaseResponse:
        if c.TagController().delete_one(int(item_name)):
            return make_response(jsonify(status="SUCCESS"), 204)
        else:
            return make_response(jsonify(status="ERR_NOT_FOUND"), 404)


class UserEndpoint(MethodView):
    """ /api/users """
    def get(self):
        pass


@app.route("/api", methods=["GET"])
def root_get() -> str:
    return "API operational."


@app.route('/api/issues', methods=["GET", "POST"])
def issues() -> BaseResponse:
    if request.query_string:
        query = [i for i in request.query_string.decode("utf-8").split("&")]
        requested_parameters = [i for i in query if "=" not in i]
        requested_parameter_values = {i.split("=")[0]: i.split("=")[1] for i in query if "=" in i}
        size = None if "size" not in requested_parameter_values.keys() else int(requested_parameter_values.get("size"))
        if request.method == "GET":
            models = c.IssueController().get_all()
            return jsonify(str(c.IssueController().limit_return_parameters(models, requested_parameters)[:size]))
    if request.method == "GET":
        return jsonify(str(c.IssueController().get_all()))
    elif request.method == "POST":
        return jsonify(str(c.IssueController().create(request.get_json())))


app.add_url_rule("/api/tags", view_func=TagEndpoint.as_view("tag_endpoint"))
app.add_url_rule("/api/tags/<item_name>", view_func=TagItemEndpoint.as_view("tag_item_endpoint"))
