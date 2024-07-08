# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-27 00:07:43 UTC+8
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union, Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class StructureSQLFilterLogic:
    """
    SQL where clauses for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLFilterLogic
        >>> filter_logic = StructureSQLFilterLogic(name="id", logic="=")
        >>> str(filter_logic)
        'id = %s'
    """

    name: str
    logic: str  # option: = , != ...
    value: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "value", f"%({self.name})s")

    def __str__(self):
        return f"{self.name} {self.logic} {self.value}"


@dataclass(frozen=True)
class StructureSQLFilterOption:
    """
    SQL where clauses for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLFilterOption
        >>> filter_option = StructureSQLFilterOption(option="and", filter_field=[
        >>>     StructureSQLFilterLogic(name="id", logic="="),
        >>>     StructureSQLFilterLogic(name="name", logic="="),
        >>> ])
        >>> str(filter_option)
        'and id = %s and name = %s'
    """

    option: Optional[str]
    filter_field: Union[Sequence[StructureSQLFilterLogic], Sequence[StructureSQLFilterOption]]

    def __str__(self):
        return f" {self.option} ".join([str(element) for element in self.filter_field])


@dataclass(frozen=True)
class StructureSQLJoinCondition:
    """
    SQL join condition for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLJoinCondition
        >>> join_condition = StructureSQLJoinCondition(table1="table1", field1="id", table2="table2", field2="id")
        >>> str(join_condition)
        'table1.id = table2.id'
    """

    table1: str
    field1: str
    table2: str
    field2: str

    def __str__(self):
        return f"{self.table1}.{self.field1} = {self.table2}.{self.field2}"


@dataclass(frozen=True)
class StructureSQLJoinLogic:
    """
    SQL join logic for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLJoinLogic, StructureSQLJoinCondition
        >>> join_logic = StructureSQLJoinLogic(type="inner", table="table1", condition=StructureSQLJoinCondition(table1="table1", field1="id", table2="table2", field2="id"))
        >>> str(join_logic)
        'inner table1 on table1.id = table2.id'
    """

    type: str
    table: str
    condition: StructureSQLJoinCondition

    def __str__(self):
        return f"{self.type} {self.table} on {self.condition}"


@dataclass(frozen=True)
class StructureSQLJoinOption:
    """
    SQL join option for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLJoinOption, StructureSQLJoinLogic
        >>> join_option = StructureSQLJoinOption(option=[
        >>>     StructureSQLJoinLogic(type="inner", table="table1", condition=StructureSQLJoinCondition(table1="table1", field1="id", table2="table2", field2="id")),
        >>>     StructureSQLJoinLogic(type="inner", table="table2", condition=StructureSQLJoinCondition(table1="table2", field1="id", table2="table3", field2="id")),
        >>> ])
        >>> str(join_option)
        'inner table1 on table1.id = table2.id inner table2 on table2.id = table3.id'
    """

    option: Sequence[StructureSQLJoinLogic]

    def __str__(self):
        return " ".join([str(element) for element in self.option])


@dataclass(frozen=True)
class StructureSQLGroupByOption:
    """
    SQL group by option for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLGroupByOption
        >>> group_by_option = StructureSQLGroupByOption(field_list=["id", "name"])
        >>> str(group_by_option)
        'id, name'
    """

    field_list: Sequence[str]

    def __str__(self):
        return ", ".join(self.field_list)


@dataclass(frozen=True)
class StructureSQLOrderByOption:
    """
    SQL order by option for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLOrderByOption
        >>> order_by_option = StructureSQLOrderByOption(field_list=["id", "name"])
        >>> str(order_by_option)
        'id, name'
    """

    field_list: Sequence[str]

    def __str__(self):
        return ", ".join(self.field_list)


@dataclass(frozen=True)
class StructureSQLLimitOption:
    """
    SQL limit option for a data source.

    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLLimitOption
        >>> limit_option = StructureSQLLimitOption(limit=10, offset=0)
        >>> str(limit_option)
        '10 offset 0'
    """

    limit: int
    offset: int = field(default=0)

    def __str__(self):
        return f"{self.limit} offset {self.offset}"


@dataclass
class StructureSQLExecuteParams:
    """
    Execcute Query parameters for a data source.

    Attrs:
        expression: The SQL expression to execute.
        params: The parameters to substitute into the expression.
    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLExecuteParams
        >>> ExecuteParams(expression="select * from table where id = %s", params=[1])
        QueryParams(expression='select * from table where id = %s', params=[1])
    Note:
        The `params` attribute can be a list, tuple, or dictionary. If it is a list or tuple,
        the values will be substituted in the order they appear in the list or tuple. If it is a dictionary,
        the values will be substituted by their keys.
    """

    expression: str
    params: Optional[Union[List[Any], Tuple[Any, ...], Dict[str, Any]]] = field(default=None)


@dataclass
class StructureSQLInsertManyParams:
    """
    Multiple Execute Query parameters for a data source.

    Attrs:
        expression: The SQL expression to execute.
        params: The parameters to substitute into the expression.
    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLInsertManyParams
        >>> parasm = [
        >>>     ("郝淑慧", 18),
        >>>     ("李雪琴", 19)
        >>> ]
        >>> InsertManyParams(expression="insert into table (name, age) values (%s, %s)", params=parasm)
        MultipleParams(expression='insert into table (name, age) values (%s, %s)', params=[('郝淑慧', 18), ("李雪琴", 19)])
    """

    expression: str
    params: Union[List[Union[List[Any], Tuple[Any, ...], Dict[str, Any]]], Tuple[Union[List[Any], Tuple[Any, ...], Dict[str, Any]], ...]]
