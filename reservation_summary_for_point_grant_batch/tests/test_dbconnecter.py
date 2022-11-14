import unittest
import mysql.connector
from unittest import mock
from reservation_summary_for_point_grant_batch import dbconnecter, dyconfig

CONFIG_DATA = {
    "name1": {
        "host": "192.168.11.21",
        "port": 3306,
        "user": "root",
        "password": "root",
        "database": "reserveServiceDB",
        "ssl_disabled": True,
    },
    "name2": {
        "host": "192.168.1.2",
        "port": 12000,
        "user": "testuser2",
        "password": "testpass2",
        "database": "testDB2",
        "ssl_disabled": False,
    },
}


class Test_dbconnecter(unittest.TestCase):

    @mock.patch.object(mysql.connector, "connect")
    @mock.patch.object(dyconfig, "getboolean")
    @mock.patch.object(dyconfig, "getint")
    @mock.patch.object(dyconfig, "get")
    def test_get_connection(self, mocked_get, mocked_getint, mocked_getboolean, mocked_connect):
        arg_name = "name1"
        expected_host = CONFIG_DATA[arg_name]["host"]
        expected_port = CONFIG_DATA[arg_name]["port"]
        expected_user = CONFIG_DATA[arg_name]["user"]
        expected_password = CONFIG_DATA[arg_name]["password"]
        expected_database = CONFIG_DATA[arg_name]["database"]
        expected_ssl_disabled = CONFIG_DATA[arg_name]["ssl_disabled"]

        mocked_get.side_effect = lambda name, key: CONFIG_DATA[name][key]
        mocked_getint.return_value = expected_port
        mocked_getboolean.return_value = expected_ssl_disabled

        actual_connection = dbconnecter.get_connection(arg_name)

        mocked_connect.assert_called_once_with(
            host=expected_host, port=expected_port, user=expected_user, password=expected_password, database=expected_database, ssl_disabled=expected_ssl_disabled)
        self.assertFalse(actual_connection.autocommit)


if __name__ == '__main__':
    unittest.main()
