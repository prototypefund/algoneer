import algoneer.dataset as dataset

from typing import Optional, Iterable

from ..dataschema import AttributeSchema

import abc


class Attribute(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self, dataset: "dataset.DataSet", column: str, schema: Optional[AttributeSchema]
    ) -> None:
        pass

    def __getattr__(self, attr):
        if attr.startswith("is_"):
            _type = attr[3:]
            if self.schema is not None and self.schema.type.name.lower() == _type:
                return True
            return False
        return super().__getattr__(attr)

    @property  # type: ignore
    @abc.abstractmethod
    def column(self) -> str:
        pass

    @column.setter  # type: ignore
    @abc.abstractmethod
    def column(self, column: str) -> None:
        pass

    @property  # type: ignore
    @abc.abstractmethod
    def roles(self) -> Iterable[str]:
        pass

    @property  # type: ignore
    @abc.abstractmethod
    def schema(self) -> Optional[AttributeSchema]:
        pass

    @schema.setter  # type: ignore
    @abc.abstractmethod
    def schema(self, schema: Optional[AttributeSchema]) -> None:
        pass

    @abc.abstractmethod
    def __len__(self) -> int:
        pass
