# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-07-03 22:33:18 UTC+8
"""

import numbers

from fairylandfuture.core.superclass.object.property import BasePropertyDescriptor


class CharField(BasePropertyDescriptor):

    def __init__(self, column_name, max_length=None):
        self._value = None
        self.column_name = column_name
        self.max_length = max_length

        if self.max_length is None:
            raise ValueError("You must spcify max_length for CharField.")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("String value need.")
        if len(value) > self.max_length:
            raise ValueError("String value len excess len.")
        self._value = value


class IntField(BasePropertyDescriptor):

    def __init__(self, column_name):
        self._value = None
        self.column_name = column_name

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("Integer value need.")
        self._value = value
