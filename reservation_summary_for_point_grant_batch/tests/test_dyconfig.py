import pytest
from configparser import ConfigParser
from unittest import mock
from reservation_summary_for_point_grant_batch import dyconfig


def test_get(mocked_parser_get):
    mocked_parser_get.side_effect = lambda section, key: f"{section}:{key}"

    arg_section = "section"
    arg_key = "key"

    actual_config = dyconfig.get(arg_section, arg_key)

    assert actual_config == f"{arg_section}:{arg_key}"
    mocked_parser_get.assert_called_once_with(arg_section, arg_key)


def test_getint(mocked_parser_getint):
    mocked_parser_getint.side_effect = lambda section, key: len(
        f"{section}{key}")

    arg_section = "section"
    arg_key = "key"

    actual_config = dyconfig.getint(arg_section, arg_key)

    assert actual_config == len(arg_key) + len(arg_section)
    mocked_parser_getint.assert_called_once_with(arg_section, arg_key)


def test_getboolean(mocked_parser_getboolean):
    mocked_parser_getboolean.side_effect = [True, False]

    arg_section1 = "section1"
    arg_section2 = "section2"
    arg_key1 = "key1"
    arg_key2 = "key2key"

    actual_config1 = dyconfig.getboolean(arg_section1, arg_key1)
    actual_config2 = dyconfig.getboolean(arg_section2, arg_key2)

    assert actual_config1 is True
    assert actual_config2 is False
    assert mocked_parser_getboolean.call_count == 2
    mocked_parser_getboolean.assert_any_call(arg_section1, arg_key1)
    mocked_parser_getboolean.assert_any_call(arg_section2, arg_key2)


if __name__ == '__main__':
    pytest.main()
