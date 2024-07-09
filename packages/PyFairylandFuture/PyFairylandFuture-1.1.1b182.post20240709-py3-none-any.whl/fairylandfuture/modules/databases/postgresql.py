# coding: utf-8
""" 
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-07-05 12:12:07 UTC+8
"""

import re
import psycopg2

from psycopg2.extras import NamedTupleCursor


class CustomPostgreSQLConnect(psycopg2.extensions.connection):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exist = True

    def close(self):
        super().close()
        self._exist = False

    @property
    def exist(self) -> bool:
        return self._exist


class CustomPostgreSQLCursor(NamedTupleCursor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._exist = True

    def close(self):
        super().close()
        self._exist = False

    @property
    def exist(self) -> bool:
        return self._exist


class PostgreSQLConnector:

    def __init__(self, host: str, port: int, user: str, password: str, database: str, schema: str = None):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._schema = schema
        self._dsn = f"host={self._host} port={self._port} user={self._user} password={self._password} dbname={self._database}"

        if self._schema:
            self._dsn += f" options='-c search_path={self._schema}'"

        self.connect: CustomPostgreSQLConnect = self.__connect()
        self.cursor: CustomPostgreSQLCursor = self.connect.cursor()

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def user(self) -> str:
        return self._user

    @property
    def database(self) -> str:
        return self._database

    def __dsn_mark_password(self, dsn):
        return re.sub(r"(password=)\S+", r"\1******", dsn)

    @property
    def dsn(self) -> str:
        return self.__dsn_mark_password(self._dsn)

    def __connect(self):
        connect = psycopg2.connect(dsn=self._dsn, connection_factory=CustomPostgreSQLConnect, cursor_factory=CustomPostgreSQLCursor)

        return connect

    def reconnect(self) -> None:
        if not self.connect or not self.connect.exist:
            self.connect: CustomPostgreSQLConnect = self.__connect()
            self.cursor: CustomPostgreSQLCursor = self.connect.cursor()
        if not self.cursor or not self.cursor.exist:
            self.cursor: CustomPostgreSQLCursor = self.connect.cursor()

    def close(self) -> None:
        try:
            self.cursor.close()
        except Exception:
            ...
        finally:
            self.cursor = None

        try:
            self.connect.close()
        except Exception:
            ...
        finally:
            self.connect = None

    def __del__(self):
        self.close()
