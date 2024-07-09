# coding: utf-8
"""
@software: PyCharm
@author: Lionel Johnson
@contact: https://fairy.host
@organization: https://github.com/FairylandFuture
@since: 2024-06-26 23:16:19 UTC+8
"""

import functools
import pymysql
from pymysql.cursors import DictCursor

from typing import Union, Dict, Tuple, Any, Iterable, Callable

from fairylandfuture.core.abstracts.databases import AbstractMySQLOperation, AbstractMySQLConnector
from fairylandfuture.structures.builder.expression import StructureSQLExecuteParams, StructureSQLInsertManyParams


class CustomMySQLConnect(pymysql.connections.Connection):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__exist = True

    def close(self):
        super().close()
        self.__exist = False

    @property
    def exist(self):
        return self.__exist


class CustomMySQLCursor(DictCursor):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__exist = True

    def close(self):
        super().close()
        self.__exist = False

    @property
    def exist(self):
        return self.__exist


class MySQLConnector(AbstractMySQLConnector):
    """
    This class is used to connect to MySQL database and execute SQL statements.

    It is a subclass of AbstractMySQLConnector and implements the methods of AbstractMySQLOperation.

    :param host: The host name of the MySQL server.
    :type host: str
    :param port: The port number of the MySQL server.
    :type port: int
    :param user: The user name used to connect to the MySQL server.
    :type user: str
    :param password: The password used to connect to the MySQL server.
    :type password: str
    :param database: The name of the database to connect to.
    :type database: str
    :param charset: The character set used to connect to the MySQL server.
    :type charset: str, optional

    Usage:
        >>> from fairylandfuture.modules.databases.mysql import MySQLConnector
        >>> connector = MySQLConnector(host="localhost", port=3306, user="root", password="password", database="test")
        >>> connector.cursor.execute("SELECT * FROM users")
        >>> result = connector.cursor.fetchall()
        >>> print(result)
        [{'id': 1, 'name': 'John', 'age': 25}, {'id': 2, 'name': 'Mary', 'age': 30}]
        >>> connector.close()
    """

    def __init__(self, host: str, port: int, user: str, password: str, database: str, charset: str = "utf8mb4"):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password
        self.__database = database
        self.__charset = charset
        self.connect: CustomMySQLConnect = self.__connect()
        self.cursor: CustomMySQLCursor = self.connect.cursor()

    @property
    def host(self) -> str:
        return self.__host

    @property
    def post(self) -> int:
        return self.__port

    @property
    def user(self) -> str:
        return self.__user

    @property
    def database(self) -> str:
        return self.__database

    @property
    def charset(self) -> str:
        return self.__charset

    def __connect(self) -> CustomMySQLConnect:
        """
        This method is used to connect to the MySQL server.

        :return: Connection object.
        :rtype: CustomMySQLConnect
        """
        connection = CustomMySQLConnect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            database=self.__database,
            charset=self.__charset,
            cursorclass=CustomMySQLCursor,
        )

        return connection

    def reconnect(self) -> None:
        """
        This method is used to reconnect to the MySQL server.

        :return: ...
        :rtype: ...
        """
        if not self.connect or not self.connect.exist:
            self.connect: CustomMySQLConnect = self.__connect()
            self.cursor: CustomMySQLCursor = self.connect.cursor()
        if not self.cursor or not self.cursor.exist:
            self.cursor: CustomMySQLCursor = self.connect.cursor()

    @staticmethod
    def reload(func):
        """
        This method is used to reload the connection and cursor object if they are closed.

        :param func: Decorated function.
        :type func: MethodType
        :return: ...
        :rtype: ...
        """

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.reconnect()
            return func(self, *args, **kwargs)

        return wrapper

    def close(self) -> None:
        """
        This method is used to close the connection and cursor object.

        :return: ...
        :rtype: ...
        """
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


class MySQLDatabase(AbstractMySQLOperation, MySQLConnector):
    """
    This class is used to interact with MySQL database.

    It is a subclass of AbstractMySQLOperation and MySQLConnector and implements the methods of AbstractMySQLOperation.

    :param host: The host name of the MySQL server.
    :type host: str
    :param port: The port number of the MySQL server.
    :type port: int
    :param user: The user name used to connect to the MySQL server.
    :type user: str
    :param password: The password used to connect to the MySQL server.
    :type password: str
    :param database: The name of the database to connect to.
    :type database: str

    Usage:
        >>> from fairylandfuture.modules.databases.mysql import MySQLDatabase
        >>> db = MySQLDatabase(host="localhost", port=3306, user="root", password="password", database="test")
        >>> db.execute(StructureSQLExecuteParams(expression="SELECT * FROM users"))
        True
        >>> result = db.select(StructureSQLExecuteParams(expression="SELECT * FROM users"))
        >>> print(result)
        [{'id': 1, 'name': 'John', 'age': 25}, {'id': 2, 'name': 'Mary', 'age': 30}]
        >>> db.close()
    """

    def __init__(self, host, port, user, password, database):
        super().__init__(host=host, port=port, user=user, password=password, database=database)

    @MySQLConnector.reload
    def execute(self, params: StructureSQLExecuteParams):
        """
        This method is used to execute a SQL statement.

        :param params: MySQL Execute parameters.
        :type params: StructureSQLExecuteParams
        :return: True if the execution is successful, otherwise False.
        :rtype: bool
        """
        try:
            self.cursor.execute(params.expression, params.params)
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            raise err
        finally:
            self.cursor.close()

    @MySQLConnector.reload
    def select(self, params: StructureSQLExecuteParams) -> Union[Dict[str, Any], Tuple[Dict[str, Any]], ...]:
        """
        This method is used to select data from the database.

        :param params: MySQL Execute parameters.
        :type params: StructureSQLExecuteParams
        :return: MySQL Query result.
        :rtype: dict or tuple
        """
        try:
            self.cursor.execute(params.expression, params.params)
            result = self.cursor.fetchall()
            if not result:
                return None
            if len(result) == 1:
                return result[0]
            return result
        except Exception as err:
            ...
            raise err
        finally:
            self.cursor.close()

    @MySQLConnector.reload
    def multiple(self, params: Iterable[StructureSQLExecuteParams]) -> bool:
        """
        This method is used to execute multiple SQL statements.

        :param params: MySQl Execute parameters list.
        :type params: Iterable[StructureSQLExecuteParams]
        :return: Execution status.
        :rtype: bool
        """
        try:
            for param in params:
                self.cursor.execute(param.expression, param.params)
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            raise err
        finally:
            self.cursor.close()

    @MySQLConnector.reload
    def insertmany(self, params: StructureSQLInsertManyParams) -> bool:
        """
        This method is used to insert multiple records into the database.

        :param params: MySQL Insert Many parameters.
        :type params: StructureSQLInsertManyParams
        :return: Execution status.
        :rtype: bool
        """
        try:
            self.cursor.executemany(params.expression, params.params)
            self.connect.commit()
            return True
        except Exception as err:
            self.connect.rollback()
            raise err
        finally:
            self.cursor.close()
