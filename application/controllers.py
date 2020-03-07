from application import db
from flask import abort
import application.models.models as models
from sqlalchemy import exc
from typing import Union, Dict, List, Optional


class Controller:
    def __init__(self, model: db.Model) -> None:
        self.model: db.Model = model

    @property
    def model(self) -> db.Model:
        return self._model

    @model.setter
    def model(self, model_: any) -> None:
        if not isinstance(model_(), db.Model):
            raise TypeError("Model must be a SQLAlchemy Model class.")
        self._model = model_

    @model.deleter
    def model(self) -> None:
        raise AttributeError("Cannot delete model attribute.")

    def get(self, params) -> Optional[List[db.Model]]:
        return self.model.query.filter_by(**params).all()

    def create(self, params: Dict[str, Union[str, int]]) -> db.Model:
        try:
            created_object = self.model(**params)
            db.session.add(created_object)
            db.session.commit()
        except exc.IntegrityError or ValueError:
            db.session.rollback()
            return abort(400)
        return created_object

    def update(self, key: int, params: Dict[str, Union[str, int]]) -> Optional[db.Model]:
        update_model = self.model.query.get(key)
        if not update_model or update_model is None:
            return
        return self.model().update(update_model, params)

    def delete(self, key: Union[int, dict]) -> bool:
        delete_model = self.model.query.get(key)
        if not delete_model or delete_model is None:
            return False
        self.model().delete(delete_model)
        return True


class TagController(Controller):
    def __init__(self) -> None:
        super(TagController, self).__init__(models.Tag)


class TypeController(Controller):
    def __init__(self):
        super(TypeController, self).__init__(models.Type)


class UserController(Controller):
    def __init__(self):
        super(UserController, self).__init__(models.User)


class CommentController(Controller):
    def __init__(self):
        super(CommentController, self).__init__(models.Comment)


class IssueController(Controller):
    def __init__(self):
        super(IssueController, self).__init__(models.Issue)

    def create(self, params: Dict[str, Union[str, int]]) -> db.Model:
        try:
            tags = params.pop("tags", None)
            created_object = self.model(**params)
            db.session.add(created_object)
            db.session.commit()
            if tags and tags is not None:
                for tag in tags:
                    db_tag = models.Tag.query.get(tag)
                    created_object.tags.append(db_tag)
                db.session.commit()
        except exc.IntegrityError or ValueError:
            db.session.rollback()
            return abort(400)
        return created_object
