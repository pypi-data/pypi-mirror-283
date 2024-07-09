# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-07-03 22:54:16 UTC+8
"""

from typing import Tuple, Dict, Any, Type

from fairylandfuture.core.superclass.object.property import BasePropertyDescriptor


class ModelMeta(type):

    def __new__(cls, name: str, bases: Tuple[Type, ...], attrs: Dict[str, Any]):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs)

        fields = dict()
        _meta = dict()
        for key, value in attrs.items():
            if isinstance(value, BasePropertyDescriptor):
                fields.update({key: value})

        attrs_meta = attrs.get("Meta", None)
        table_name = name.lower()
        if attrs_meta is not None:
            table_name = getattr(attrs_meta, "table_name", None)

        _meta.update(table_name=table_name)
        attrs.update({"_meta": _meta, "fields": fields, "table_name": table_name})
        attrs.pop("Meta")

        return super().__new__(cls, name, bases, attrs)
