from src import db
import src.services as services
from typing import Type, Union, Dict, List, Optional


class Controller:
    def __init__(self, service: Type[services.Service]) -> None:
        self.service: Type[services.Service] = service

    @property
    def service(self) -> Type[services.Service]:
        return self._service

    @service.setter
    def service(self, service_: any) -> None:
        if not issubclass(service_(), services.Service):
            raise TypeError("service must be a Service subclass.")
        self._service = service_

    @service.deleter
    def service(self) -> None:
        raise AttributeError("Cannot delete service attribute.")

    def create(self, params: Dict[str, Union[str, int]]) -> db.Model:
        return self.service().create(params)

    def update_one(self, key: Union[int, dict], params: Dict[str, Union[str, int]]) -> Union[db.Model, None]:
        update_model = None
        if type(key) == int:
            update_model = self.service().get_by_primary(key)
        elif type(key) == dict:
            update_model = self.service().get_by_attr(key)
        if not update_model or type(update_model) == list:
            return
        return self.service().update(update_model, params)

    def update_many(self, key: Dict[str, Union[int, str]], params: Dict[str, Union[int, str]]) -> \
            Union[List[db.Model], None]:
        update_models = self.service().get_by_attr(key)
        if not update_models:
            return
        updated_models = None
        for model in update_models:
            updated_models.append(self.service().update(model, params))
        return updated_models


    def delete(self, key: Union[int, str]) -> None:
        return self.service().delete_by_attr(key)

    def get_all(self) -> Union[List[db.Model], None]:
        return self.service().get_all()


class TagController(Controller):
    def __init__(self) -> None:
        super(TagController, self).__init__(services.TagService)

    def get_by_name(self, name: str) -> Union[db.Model, None]:
        return self.service()[name]
