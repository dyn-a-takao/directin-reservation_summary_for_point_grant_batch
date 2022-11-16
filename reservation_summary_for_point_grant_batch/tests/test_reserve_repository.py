from decimal import Decimal
import pytest
from configparser import ConfigParser
from unittest import mock
from reservation_summary_for_point_grant_batch import dyconfig


def test_get_reserve_summary(mocked_config_get):
    mocked_config_get.return_value = "4"
    mocked_connection = mock.MagicMock()

    # query_result = [
    #     {
    #         "MEMBER_CODE": "member1",
    #         "PLAN_CODE": "plan1",
    #         "RESERVE_NUMBER": "reserve1",
    #         "ACTUAL_PRICE": Decimal("6200"),
    #         "TOTAL_USE_POINT_AMOUNT": Decimal("1000"),
    #     },
    #     {
    #         "MEMBER_CODE": "member2",
    #         "PLAN_CODE": "plan2",
    #         "RESERVE_NUMBER": "reserve2",
    #         "ACTUAL_PRICE": Decimal("12000"),
    #         "TOTAL_USE_POINT_AMOUNT": Decimal("0"),
    #     },
    #     {
    #         "MEMBER_CODE": "member3",
    #         "PLAN_CODE": "plan3",
    #         "RESERVE_NUMBER": "reserve3",
    #         "ACTUAL_PRICE": Decimal("1500"),
    #         "TOTAL_USE_POINT_AMOUNT": Decimal("500"),
    #     }, ]

    # arg_section = "section"
    # arg_key = "key"

    # actual_config = dyconfig.get(arg_section, arg_key)

    # self.assertEqual(actual_config, f"{arg_section}:{arg_key}")
    # mocked_get.assert_called_once_with(arg_section, arg_key)


if __name__ == '__main__':
    pytest.main()
