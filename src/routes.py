from src import app
from flask import jsonify, request
from werkzeug.wrappers import BaseResponse
import src.controllers as c
from werkzeug.exceptions import HTTPException
from typing import Union


# Error Handling

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


# Endpoints

@app.route("/api", methods=["GET"])
def root_get() -> str:
    return "API operational."


@app.route("/api/tags", methods=["GET", "POST"])
def tags() -> BaseResponse:
    if request.method == "GET":
        return jsonify(str(c.TagController().get_all()))
    elif request.method == "POST":
        return jsonify(c.TagController().create(request.get_json()))


@app.route("/api/tags/<tag_identifier>", methods=["GET"])
def tags_name(tag_identifier: Union[str, int]) -> BaseResponse:
    if type(tag_identifier) == str:
        return jsonify(str(c.TagController().get_by_name(tag_identifier)))
    elif type(tag_identifier) == int:
        return jsonify(str(c.TagController().get_by_primary(tag_identifier)))


@app.route('/api/users', methods=['GET', 'POST'])
def users() -> BaseResponse:
    pass


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

