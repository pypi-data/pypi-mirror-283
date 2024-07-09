# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-05-10 10:45:41 UTC+8
"""

from fairylandfuture.core.superclass.enumerate import BaseEnum


class DateTimeEnum(BaseEnum):
    """
    Date time enum.
    """

    date = "%Y-%m-%d"
    time = "%H:%M:%S"
    datetime = "%Y-%m-%d %H:%M:%S"

    date_cn = "%Y年%m月%d日"
    time_cn = "%H时%M分%S秒"
    datetime_cn = "%Y年%m月%d日 %H时%M分%S秒"

    @classmethod
    def default(cls) -> str:
        return cls.datetime.value

    @classmethod
    def default_cn(cls) -> str:
        return cls.datetime_cn.value


class EncodingEnum(BaseEnum):
    """
    Encoding enum.
    """

    utf_8 = "UTF-8"
    gbk = "GBK"
    gb2312 = "GB2312"
    gb18030 = "GB18030"

    @classmethod
    def default(cls):
        return cls.utf_8.value


class LogLevelEnum(BaseEnum):
    """
    Log level Enum.
    """

    trace = "TRACE"
    debug = "DEBUG"
    info = "INFO"
    success = "SUCCESS"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"

    @classmethod
    def default(cls) -> str:
        return cls.info.value

    @classmethod
    def default_debug(cls) -> str:
        return cls.trace.value


class PlatformEnum(BaseEnum):
    """
    Platform enum.
    """

    windows = "Windows"
    linux = "Linux"
    macos = "Darwin"
    darwin = "Darwin"

    @classmethod
    def default(cls) -> str:
        return cls.linux.value
