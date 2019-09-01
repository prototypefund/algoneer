from .object import Object
from .manager import Manager
from algoneer.dataschema import DataSchema as ADataSchema

from typing import Dict, Any, Optional


class DataSchema(Object):
    Type = ADataSchema

    @property
    def data(self) -> Dict[str, Any]:
        return {}


class DataSchemas(Manager[DataSchema]):
    Type = DataSchema

    def url(self, obj: Optional[DataSchema]) -> str:
        return ""
