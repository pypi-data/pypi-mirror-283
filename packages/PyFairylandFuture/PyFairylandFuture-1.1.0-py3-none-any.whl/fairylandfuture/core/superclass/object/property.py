# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-07-03 22:31:57 UTC+8
"""


class BasePropertyDescriptor:

    def __delete__(self, instance):
        super().__delete__(instance)
