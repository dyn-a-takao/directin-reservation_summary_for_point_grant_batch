import mysql.connector
from . import dyconfig


def get_connection(name: str):
    connection = mysql.connector.connect(
        host=dyconfig.get(name, "host"),
        port=dyconfig.getint(name, "port"),
        user=dyconfig.get(name, "user"),
        password=dyconfig.get(name, "password"),
        database=dyconfig.get(name, "database"),
        ssl_disabled=dyconfig.getboolean(name, "ssl_disabled"))
    connection.autocommit = False
    return connection
