# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-04 上午10:38:31 UTC+8
"""

import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class BaseStructure:

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return json.dumps(self.__dict__)
