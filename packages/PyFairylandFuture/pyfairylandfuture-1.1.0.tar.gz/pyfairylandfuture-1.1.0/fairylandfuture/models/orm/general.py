# coding: utf-8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-07-03 12:42:53 UTC+8
"""

import numbers

from typing import Sequence, Dict, Any, Optional

from fairylandfuture.core.metaclasses.model import ModelMeta


class BaseModel(metaclass=ModelMeta):

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

        super().__init__()

    def save(self):
        sql = f"insert into {self.table_name}({', '.join(self.fields)}) values ({', '.join(['%({})s'.format(field) for field in self.fields])})"
        params = {field: getattr(self, field) for field in self.fields}
        print(sql, params)


class BaseModelV2:

    def __init__(self, table_name: str, fields: Sequence[str]):
        self._table_name = table_name
        self._fields = fields

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def fields(self) -> Sequence[str]:
        return self._fields

    def save(self, data: Dict[str, Any], include_fields: Optional[Sequence[str]] = None, exclude_fields: Optional[Sequence[str]] = None):
        if include_fields:
            fields = include_fields
        else:
            if exclude_fields:
                fields = [field for field in self.fields if field not in exclude_fields]
            else:
                fields = self.fields

        sql = f"insert into {self.table_name}({', '.join(fields)}) values ({', '.join(['%({})s'.format(field) for field in fields])});"
        params = {field: data.get(field, None) for field in fields}

        return sql, params

    def update(self, data: Dict[str, Any], filter_id: int):
        if not data:
            raise ValueError("data is required")

        if not filter_id:
            raise ValueError("filters is required")
        else:
            if not isinstance(filter_id, numbers.Integral):
                raise ValueError("filter_id must be a positive integer")

        sql = f"update {self.table_name} set {', '.join(['{}=%({})s'.format(field, field) for field in data.keys()])} where id=%(filter_id)s;"
        params = {**data, "filter_id": filter_id}

        return sql, params

    def list(
        self,
        where: Optional[str] = None,
        order_by: Optional[str] = None,
        page: int = 1,
        size: int = 10,
        include_fields: Optional[Sequence[str]] = None,
        exclude_fields: Optional[Sequence[str]] = None,
    ):
        if include_fields:
            fields = include_fields
        else:
            if exclude_fields:
                fields = [field for field in self.fields if field not in exclude_fields]
            else:
                fields = self.fields

        if "id" not in fields:
            fields.insert(0, "id")

        if where and not where.startswith("where"):
            a = where.split("or")
            for where_or in where.split("or"):
                for where_and in where_or.split("and"):
                    print(where_and.strip().split("="))
            print(a)
            where = f"where {where.strip()}"
        else:
            where = ""

        if order_by and not order_by.startswith("order by"):
            order_by = f"order by {order_by.strip()}"
        else:
            order_by = ""
            

        limit = f"limit {size} offset {(page - 1) * size}"
        
        sql = " ".join(("select", ", ".join(fields), "from", self.table_name, where, order_by, limit))
        sql = " ".join(sql.split()) + ";"
        
        return sql
