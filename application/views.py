from application import db
from flask import jsonify, request, make_response, abort
from flask import current_app as app
from flask.wrappers import Response
from werkzeug.wrappers import BaseResponse
import application.controllers as c
from werkzeug.exceptions import HTTPException
from typing import Union, Tuple
from flask.views import MethodView
import json


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

@app.errorhandler(406)
def handle_not_acceptable(error_) -> BaseResponse:
    return make_response(jsonify(error="ERR_NOT_ACCEPTABLE"), 406)


@app.errorhandler(400)
def handle_not_acceptable(error_) -> BaseResponse:
    return make_response(jsonify(error="ERR_BAD_REQUEST"), 400)


@app.errorhandler(415)
def handle_not_acceptable(error_) -> BaseResponse:
    return make_response(jsonify(error="ERR_NOT_JSON"), 415)


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




@app.route("/api", methods=["GET"])
def root_get() -> str:
    return make_response("API operational.", 200)
