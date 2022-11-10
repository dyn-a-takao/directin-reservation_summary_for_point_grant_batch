import unittest
import mysql.connector
from unittest import mock
from reservation_summary_for_point_grant_batch import dbconnecter, dyconfig

CONFIG_DATA = {
    "name1": {
        "host": "192.168.11.21",
        "user": "root",
        "password": "root",
        "database": "reserveServiceDB",
    },
    "name2": {
        "host": "192.168.1.2",
        "user": "testuser2",
        "password": "testpass2",
        "database": "testDB2",
    },
}


class Test_dbconnecter(unittest.TestCase):

    @mock.patch.object(dyconfig, "getboolean", return_value=True)
    @mock.patch.object(dyconfig, "getint", return_value=3306)
    @mock.patch.object(dyconfig, "get")
    def test_get_connection(self, mocked_get, mocked_getint, mocked_getboolean):
        mocked_get.side_effect = lambda name, key: CONFIG_DATA[name][key]
        expected_name = "name1"
        expected_host = CONFIG_DATA[expected_name]["host"]
        expected_port = mocked_getint.return_value
        expected_user = CONFIG_DATA[expected_name]["user"]
        expected_password = CONFIG_DATA[expected_name]["password"]
        expected_database = CONFIG_DATA[expected_name]["database"]
        expected_ssl_disabled = mocked_getboolean.return_value

        actual = dbconnecter.get_connection(expected_name)

        self.assertEqual(actual._host, expected_host)


if __name__ == '__main__':
    unittest.main()
