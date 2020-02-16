import src.models as models
from src import db
from werkzeug.wrappers import BaseResponse
from typing import List


class Service:
    def __init__(self, model: db.Model):
        self.model: db.Model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_):
        if not isinstance(model_(), db.Model):
            raise TypeError("Model must be a SQLAlchemy Model class.")
        self._model = model_

    @model.deleter
    def model(self):
        raise AttributeError("Cannot delete model attribute.")

    def __repr__(self):
        return f"'{self.__class__.__name__}'('{self.model.__class__.__name__}')'"

    def __len__(self):
        return len(self.model.query.all())

    def __getitem__(self, item):
        if type(item) == int:
            return self.get_all()[item]
        elif type(item) == str or type(item) == dict:
            return self.get_by_attr(item)

    def create(self, params: dict) -> db.Model:
        created_object = self.model(**params)
        db.session.add(created_object)
        db.session.commit()
        return created_object

    def get_all(self) -> List[db.Model]:
        return self.model.query.all()

    def get_by_attr(self, key) -> db.Model:
        return self.model.query.filter_by(name=key).first()

    def update_by_attr(self, key, params: dict) -> db.Model:
        updated_model = self[key]
        for field, value in params.items():
            setattr(updated_model, field, value)
        db.session.commit()
        return updated_model

    def delete_by_attr(self, key) -> None:
        db.session.delete(self[key])
        db.session.commit()


class TagService(Service):
    def __init__(self):
        super(TagService, self).__init__(models.Tag)


class TypeService(Service):
    def __init__(self):
        super(TypeService, self).__init__(models.Type)


class UserService(Service):
    def __init__(self):
        super(UserService, self).__init__(models.User)


class CommentService(Service):
    def __init__(self):
        super(CommentService, self).__init__(models.Comment)

    def get_by_attr(self, key: dict) -> db.Model:
        return self.model.query.filter_by(**key).first()


class IssueService(Service):
    def __init__(self):
        super(IssueService, self).__init__(models.Issue)

    def get_by_attr(self, key: int) -> db.Model:
        return self.model.query.filter_by(id=key).first()
