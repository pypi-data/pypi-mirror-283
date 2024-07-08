# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-26 23:52:32 UTC+8
"""

from typing import Optional, Sequence

from fairylandfuture.core.superclass.builders import BaseBuilderMySQL
from fairylandfuture.structures.builder.expression import (
    StructureSQLFilterOption,
    StructureSQLJoinOption,
    StructureSQLGroupByOption,
    StructureSQLOrderByOption,
    StructureSQLLimitOption,
)
from fairylandfuture.modules.exceptions import SQLSyntaxError


class QueryMySQLBuilder(BaseBuilderMySQL):
    """
    MySQL query builder.

    :param table: The table name.
    :type table: str
    :param fields: The fields to select.
    :type fields: Optional[Sequence[str]]

    Attributes:
        table: The table name.
        fields: The fields to select.
        sql: The SQL query string.
    Usage:
        >>> from fairylandfuture.structures.builder.expression import StructureSQLFilterLogic
        >>> builder = QueryMySQLBuilder(table="users", fields=["id", "name", "age"])
        >>> builder.operation()
        "select * from users;"
        >>> builder.operation(where=StructureSQLFilterOption("and", filter_field=(StructureSQLFilterLogic("id", "="))))
        "select * from users where id = %(id)s;"
        >>> builder.operation(where=StructureSQLFilterOption("or", filter_field=(StructureSQLFilterLogic("id", "="), StructureSQLFilterLogic("id", "in"))))
        "select * from users where id = %(id)s or id in (%(id_1)s, %(id_2)s);"
    """

    def __init__(self, table: str, fields: Optional[Sequence[str]] = None):
        super().__init__(table=table)
        self.fields = fields
        if not self.fields:
            self.sql = f"select * from {self.table};"
        else:
            self.sql = f"select {', '.join(fields)} from {self.table};"

    def operation(
        self,
        join: Optional[StructureSQLJoinOption] = None,
        where: Optional[StructureSQLFilterOption] = None,
        group_by: Optional[StructureSQLGroupByOption] = None,
        order_by: Optional[StructureSQLOrderByOption] = None,
        limit: Optional[StructureSQLLimitOption] = None,
    ) -> str:
        """
        Build the SQL query string.

        :param join: MySQL join option.
        :type join: StructureSQLJoinOption
        :param where: MySQL filter option.
        :type where: StructureSQLFilterOption
        :param group_by: MySQL group by option.
        :type group_by: StructureSQLGroupByOption
        :param order_by: MySQL order by option.
        :type order_by: StructureSQLOrderByOption
        :param limit: MySQL limit option.
        :type limit: StructureSQLLimitOption
        :return: MySQL query string.
        :rtype: str
        """
        join = f"{join}" if join else ""
        where = f"where {where}" if where else ""
        if group_by:
            if group_by.field_list == self.fields:
                group_by = f"group_by {group_by}"
            else:
                raise SQLSyntaxError("group_by fields must be in select fields.")
        else:
            group_by = ""
        order_by = f"order_by {order_by}" if order_by else ""
        limit = f"limit {limit}" if limit else ""
        sql = " ".join((self.sql.rstrip(";"), join, where, group_by, order_by, limit))

        return " ".join(sql.split()) + ";"

    def to_string(self) -> str:
        """
        Return the SQL query string.

        :return: MySQL query string.
        :rtype: str
        """
        return self.sql

    def __str__(self):
        return self.sql


class InsertMySQLBuilder(BaseBuilderMySQL):
    """
    MySQL insert builder.

    :param table: The table name.
    :type table: str
    :param fields: The fields to insert.
    :type fields: Sequence[str]

    Attributes:
        table: The table name.
        fields: The fields to insert.
        sql: The SQL query string.
    Usage:
        >>> builder = InsertMySQLBuilder(table="users", fields=["id", "name", "age"])
        >>> builder.operation(values={"id": 1, "name": "John", "age": 25})
        "insert into users (id, name, age) values (%(id)s, %(name)s, %(age)s);"
        >>> builder.operation(values={"id": 2, "name": "Mary", "age": 30})
        "insert into users (id, name, age) values (%(id)s, %(name)s, %(age)s);"
    """

    def __init__(self, table: str, fields: Sequence[str]):
        super().__init__(table=table)
        self.fields = fields
        self.sql = f"insert into {self.table} ({', '.join(fields)}) values ({', '.join(['%({})s'.format(field) for field in fields])});"

    def to_string(self):
        """
        Return the SQL query string.

        :return: MySQL insert string.
        :rtype: str
        """
        return self.sql

    def __str__(self):
        return self.sql
