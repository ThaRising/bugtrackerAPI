from src import app
from src.models import Tag, Comment, User, Type, Issue


@app.route("/")
def hello():
    return "Hello World!"
