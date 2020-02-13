from src.models import Tag
from src import db
from werkzeug.wrappers import BaseResponse


class TagService:
    def __init__(self):
        self.model = Tag

    def create(self, params: dict):
        create = self.model(**params)
        db.session.add(create)
        db.session.commit()
        return str(create)

    def get_all(self):
        query_results = str(self.model.query.all())
        return BaseResponse("Not found", status=404) if query_results is None else query_results

    def get_by_name(self, req_name: str) -> BaseResponse:
        query_result = str(self.model.query.filter_by(name=req_name).first())
        return BaseResponse("Not found", status=404) if query_result is None else query_result
