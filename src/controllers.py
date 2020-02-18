from src import db
import src.services as services
from typing import Type, Union, Dict, List, Optional
import ast


class Controller:
    def __init__(self, service: Type[services.Service]) -> None:
        self.service: Type[services.Service] = service

    @property
    def service(self) -> Type[services.Service]:
        return self._service

    @service.setter
    def service(self, service_: any) -> None:
        if not issubclass(service_, services.Service):
            raise TypeError("service must be a Service subclass.")
        self._service = service_

    @service.deleter
    def service(self) -> None:
        raise AttributeError("Cannot delete service attribute.")

    def _check_if_one(self, key: Union[int, List[int], dict]) -> Optional[db.Model]:
        model = None
        if type(key) == int or type(key) == list:
            model = self.service().get_by_primary(key)
        elif type(key) == dict:
            model = self.service().get_by_attr(key)
            model = model[0] if model and not len(model) > 1 else None
        return model

    def create(self, params: Dict[str, Union[str, int]]) -> db.Model:
        return self.service().create(params)

    def update_one(self, key: Union[int, List[int], dict], params: Dict[str, Union[str, int]]) -> Optional[db.Model]:
        update_model = self._check_if_one(key)
        if not update_model:
            return
        return self.service().update(update_model, params)

    def update_many(self, key: Dict[str, Union[int, str]], params: Dict[str, Union[int, str]]) -> Optional[List[db.Model]]:
        update_models = self.service().get_by_attr(key)
        if not update_models:
            return
        updated_models = None
        for model in update_models:
            updated_models.append(self.service().update(model, params))
        return updated_models

    def delete_one(self, key: Union[int, dict]) -> bool:
        delete_model = self._check_if_one(key)
        if not delete_model:
            return False
        self.service().delete(delete_model)
        return True

    def delete_many(self, key: Dict[str, Union[int, str]]) -> bool:
        delete_models = self.service().get_by_attr(key)
        if not delete_models:
            return False
        for model in delete_models:
            self.service().delete(model)
        return True

    def get_all(self) -> Union[List[db.Model], None]:
        return self.service().get_all()

    def get_by_primary(self, id_):
        return self.service().get_by_primary(id_)

    def get_by_attr(self, params):
        return self.service().get_by_attr(params)

    def limit_return_parameters(self, id_: int, limit: List[str]) -> dict:
        total = ast.literal_eval(str(self.get_by_primary(id_)))
        return {key: total[key] for key in limit}


class GenericNameController(Controller):
    def get_by_name(self, name: str) -> Optional[db.Model]:
        model = self.service().get_by_attr({"name": name})
        if not model or not len(model) > 0:
            return
        return model[0]

    def get_connected_issues(self, name: str) -> Optional[List[db.Model]]:
        model = self.get_by_name(name)
        if model:
            return model.issues
        return


class TagController(GenericNameController):
    def __init__(self) -> None:
        super(GenericNameController, self).__init__(services.TagService)


class TypeController(GenericNameController):
    def __init__(self):
        super(TypeController, self).__init__(services.TypeService)


class UserController(Controller):
    def __init__(self):
        super(UserController, self).__init__(services.UserService)

    def get_by_name(self, name: str) -> Optional[db.Model]:
        model = self.service().get_by_attr({"name": name})
        if not model or not len(model) > 0:
            return
        return model[0]


class CommentController(Controller):
    def __init__(self):
        super(CommentController, self).__init__(services.CommentService)

    def update_one(self, key: Union[int, List[int], dict], params: Dict[str, str]) -> Optional[db.Model]:
        update_model = self._check_if_one(key)
        if not update_model:
            return
        self.service().update(update_model, {"content": params.get("content"), "edited": True})


class IssueController(Controller):
    def __init__(self):
        super(IssueController, self).__init__(services.IssueService)

    def add_comment(self, comment: db.Model):
        self.service().model.comments.append(comment)
