import application.models as models
from application import db
from typing import List, Union, Dict, Optional
from sqlalchemy import exc
from flask import abort


class Service:
    def __init__(self, model: db.Model):
        self.model: db.Model = model

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_: any) -> None:
        if not isinstance(model_(), db.Model):
            raise TypeError("Model must be a SQLAlchemy Model class.")
        self._model = model_

    @model.deleter
    def model(self) -> None:
        raise AttributeError("Cannot delete model attribute.")

    def create(self, params: Dict[str, Union[str, int]]) -> db.Model:
        try:
            created_object = self.model(**params)
            db.session.add(created_object)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return abort(400)
        except ValueError:
            db.session.rollback()
            return abort(400)
        return created_object

    def update(self, model: db.Model, params: dict) -> Union[db.Model]:
        try:
            for field, value in params.items():
                setattr(model, field, value)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return abort(400)
        return model

    def delete(self, model: db.Model) -> None:
        """ Deletes a given row (represented by an instance of a db.Model class) inside of the database """
        db.session.delete(model)
        db.session.commit()

    def get(self, params) -> Optional[List[db.Model]]:
        """ Returns all rows of the given Table """
        return self.model.query.filter_by(**params).all()


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


class IssueService(Service):
    def __init__(self):
        super(IssueService, self).__init__(models.Issue)
