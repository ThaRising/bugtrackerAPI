from src import app
from flask import jsonify, request
from werkzeug.wrappers import BaseResponse
import src.services
from werkzeug.exceptions import HTTPException


# Error Handling

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


# Endpoints

@app.route("/")
def hello() -> str:
    return "API operational."


@app.route("/tags", methods=["GET", "POST"])
def tags() -> BaseResponse:
    if request.method == "GET":
        return jsonify(src.services.TagService().get_all())
    elif request.method == "POST":
        return jsonify(src.services.TagService().create(request.get_json()))


@app.route("/tags/<tag_name>", methods=["GET"])
def tags_name(tag_name: str) -> BaseResponse:
    if request.method == "GET":
        return jsonify(src.services.TagService().get_by_name(tag_name))
