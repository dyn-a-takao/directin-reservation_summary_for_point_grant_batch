import pytest
import csv
import mysql.connector
import requests
from unittest import mock
from configparser import ConfigParser
from reservation_summary_for_point_grant_batch import dbconnecter, dyconfig


@pytest.fixture
def mocked_config_get() -> mock.Mock:
    with mock.patch.object(dyconfig, "get") as mocked:
        yield mocked


@pytest.fixture
def mocked_config_getint() -> mock.Mock:
    with mock.patch.object(dyconfig, "getint") as mocked:
        yield mocked


@pytest.fixture
def mocked_config_getboolean() -> mock.Mock:
    with mock.patch.object(dyconfig, "getboolean") as mocked:
        yield mocked


@pytest.fixture
def mocked_parser_get() -> mock.Mock:
    with mock.patch.object(ConfigParser, "get") as mocked:
        yield mocked


@pytest.fixture
def mocked_parser_getint() -> mock.Mock:
    with mock.patch.object(ConfigParser, "getint") as mocked:
        yield mocked


@pytest.fixture
def mocked_parser_getboolean() -> mock.Mock:
    with mock.patch.object(ConfigParser, "getboolean") as mocked:
        yield mocked


@pytest.fixture
def mocked_http_get() -> mock.Mock:
    with mock.patch.object(requests, "get") as mocked:
        yield mocked


@pytest.fixture
def mocked_connection() -> mock.Mock:
    with mock.patch.object(dbconnecter, "get_connection") as mocked:
        yield mocked


@pytest.fixture
def mocked_csv_DictWriter() -> mock.Mock:
    with mock.patch.object(csv, "DictWriter") as mocked:
        yield mocked


@pytest.fixture
def mocked_connect() -> mock.Mock:
    with mock.patch.object(mysql.connector, "connect") as mocked:
        yield mocked


@pytest.fixture
def mocked_file_open() -> mock.Mock:
    with mock.patch("builtins.open") as mocked:
        mocked.read_data = ""
        yield mocked
