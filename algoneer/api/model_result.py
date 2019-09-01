from .object import Object
from .manager import Manager
from algoneer.result import ModelResult as AModelResult

from typing import Dict, Any, Optional


class ModelResult(Object):
    Type = AModelResult

    @property
    def data(self) -> Dict[str, Any]:
        return {}


class ModelResults(Manager[ModelResult]):
    Type = ModelResult

    def url(self, obj: Optional[ModelResult]) -> str:
        return ""
