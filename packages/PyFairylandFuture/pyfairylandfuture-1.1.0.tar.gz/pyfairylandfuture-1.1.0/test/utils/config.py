# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-24 12:49:52 UTC+8
"""

import yaml

from typing import Dict, Any
from pathlib import Path

from fairylandfuture.constants.enums import EncodingEnum


class TestConfig:

    def __init__(self, path: Path):
        self.path = path

    def __read(self):
        with open(self.path, mode="r", encoding=EncodingEnum.utf_8.value) as stream:
            content = yaml.safe_load(stream)

        return content

    @property
    def config(self) -> Dict[str, Any]:
        return self.__read()
