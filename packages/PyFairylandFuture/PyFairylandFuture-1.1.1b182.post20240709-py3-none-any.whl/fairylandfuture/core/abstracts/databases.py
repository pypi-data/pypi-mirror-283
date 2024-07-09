# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-12 22:23:51 UTC+8
"""

import abc
from typing import List

from fairylandfuture.structures.builder.expression import StructureSQLExecuteParams, StructureSQLInsertManyParams


class AbstractMySQLConnector(abc.ABC):

    @abc.abstractmethod
    def reconnect(self) -> None: ...


class AbstractMySQLOperation(abc.ABC):

    @abc.abstractmethod
    def execute(self, params: StructureSQLExecuteParams) -> bool: ...

    def insert(self, params: StructureSQLExecuteParams) -> bool:
        return self.execute(params)

    def delete(self, params: StructureSQLExecuteParams) -> bool:
        return self.execute(params)

    def update(self, params: StructureSQLExecuteParams) -> bool:
        return self.execute(params)

    @abc.abstractmethod
    def select(self, params: StructureSQLExecuteParams): ...

    @abc.abstractmethod
    def multiple(self, params: List[StructureSQLExecuteParams]) -> bool: ...

    @abc.abstractmethod
    def insertmany(self, params: StructureSQLInsertManyParams) -> bool: ...
