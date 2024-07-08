# coding: utf-8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-30 14:20:28 UTC+8
"""

from fairylandfuture.core.superclass.files import BaseFile, BaseTextFile, BaseYamlFile, BaseJsonFile


class File(BaseFile): ...


class TextFile(BaseTextFile): ...


class YamlFile(BaseYamlFile): ...


class JsonFile(BaseJsonFile): ...


class OtherFile(BaseTextFile): ...
