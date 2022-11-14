import unittest
from configparser import ConfigParser
from unittest import mock
from reservation_summary_for_point_grant_batch import dyconfig


class test_dyconfig(unittest.TestCase):

    @mock.patch.object(ConfigParser, "get")
    def test_get(self, mocked_get):
        mocked_get.side_effect = lambda section, key: f"{section}:{key}"

        arg_section = "section"
        arg_key = "key"

        actual_config = dyconfig.get(arg_section, arg_key)

        self.assertEqual(actual_config, f"{arg_section}:{arg_key}")
        mocked_get.assert_called_once_with(arg_section, arg_key)

    @mock.patch.object(ConfigParser, "getint")
    def test_getint(self,  mocked_getint):
        mocked_getint.side_effect = lambda section, key: len(f"{section}{key}")

        arg_section = "section"
        arg_key = "key"

        actual_config = dyconfig.getint(arg_section, arg_key)

        self.assertEqual(actual_config, len(arg_key) + len(arg_section))
        mocked_getint.assert_called_once_with(arg_section, arg_key)

    @mock.patch.object(ConfigParser, "getboolean")
    def test_getboolean(self,  mocked_getboolean):
        mocked_getboolean.side_effect = [True, False]

        arg_section1 = "section1"
        arg_section2 = "section2"
        arg_key1 = "key1"
        arg_key2 = "key2key"

        actual_config1 = dyconfig.getboolean(arg_section1, arg_key1)
        actual_config2 = dyconfig.getboolean(arg_section2, arg_key2)

        self.assertTrue(actual_config1)
        self.assertFalse(actual_config2)
        self.assertEqual(mocked_getboolean.call_count, 2)
        mocked_getboolean.assert_any_call(arg_section1, arg_key1)
        mocked_getboolean.assert_any_call(arg_section2, arg_key2)


if __name__ == '__main__':
    unittest.main()
