from typing import Dict, Any, Optional, TypeVar, Generic, Type, List

from algoneer import Object as AObject
import algoneer.api
import abc

T = TypeVar("T", bound=AObject)


class ObjectMeta(abc.ABCMeta):
    def __init__(cls, name: str, bases, namespace) -> None:
        """
        We add the mapped class to the mappings dictionary, which allows the
        session to determine the correct API object for a given Algoneer object.
        """
        if hasattr(cls, "Type"):
            mappings[cls.Type] = cls  # type: ignore
        super().__init__(name, bases, namespace)


class Object(Generic[T], metaclass=ObjectMeta):
    """
    All API objects inherit from this class. Each API object maps to a given
    Algoneer object.
    """

    Type: Type[T]

    def __init__(self, mapped_obj: T, session: Optional["algoneer.api.Session"] = None):
        self._mapped_obj = mapped_obj
        self._api_data: Optional[Dict[str, Any]] = None
        self._session = session

    @property
    def mapped_obj(self) -> T:
        return self._mapped_obj

    @property
    def session(self) -> Optional["algoneer.api.Session"]:
        return self._session

    @property
    def dependencies(self) -> List[AObject]:
        return []

    @property
    def dependants(self) -> List[AObject]:
        return []

    @property
    def data(self) -> Dict[str, Any]:
        return self.mapped_obj.dump()

    @property
    def api_data(self) -> Optional[Dict[str, Any]]:
        return self._api_data

    @api_data.setter
    def api_data(self, api_data: Dict[str, Any]) -> None:
        self._api_data = api_data

    @property
    def id(self) -> Optional[str]:
        if self._api_data is None:
            return None
        return self._api_data.get("id")

    @id.setter
    def id(self, id: Optional[str]) -> None:
        if self._api_data is None:
            self._api_data = {}
        self._api_data["id"] = id


mappings: Dict[Type[AObject], Type[Object]] = {}


def get_class_for(cls: Type[AObject]) -> Optional[Type[Object]]:
    for potential_cls in [cls] + list(cls.__bases__):
        if potential_cls in mappings:
            return mappings[potential_cls]
    return None
