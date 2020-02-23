from flask import current_app as app
from flask import jsonify, make_response
from werkzeug.exceptions import HTTPException
from werkzeug.wrappers import BaseResponse


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


@app.route("/api/", methods=["GET"])
def root_get() -> str:
    return make_response("API operational.", 200)
