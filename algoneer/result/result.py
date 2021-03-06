from typing import Any, Dict

from algoneer.object import Object

import abc


class Result(Object, abc.ABC):
    def __init__(self, data: Any):
        super().__init__()
        self._data = data

    def dump(self) -> Dict[str, Any]:
        return {"data": self.data, "name": self.name, "version": self.version}

    def load(self, data: Dict[str, Any]) -> None:
        pass

    @abc.abstractproperty
    def name(self) -> str:
        pass

    @abc.abstractproperty
    def version(self) -> str:
        pass

    @property
    def data(self) -> Any:
        return self._data

    def format(self, format: str) -> Any:
        pass


class ResultProxy:
    def __init__(self, result: Result) -> None:
        self._result = result

    @property
    def result(self) -> Result:
        return self._result

    @property
    def name(self) -> str:
        return self.result.name

    @property
    def version(self) -> str:
        return self.result.version

    @property
    def data(self) -> Any:
        return self.result.data

    def format(self, format: str) -> Any:
        return self.result.format
