import datetime
import pytest
from datetime import date
from decimal import Decimal
from reservation_summary_batch import reserve_repository


CONFIG_DATA = {
    "reserve_repository": {
        "grace_days_after_checkout": 12,
        "acquired_size": 6,
    },
}


def test_get_reserve_list(mocked_config_get, mocked_config_getint, mocked_connection):
    mocked_config_get.side_effect = lambda name, key: CONFIG_DATA[name][key]
    mocked_config_getint.side_effect = lambda name, key: CONFIG_DATA[name][key]

    group_code_1 = "M000000060"
    group_code_2 = "M000000019"

    query_result = [
        {
            "MEMBER_GROUP_CODE": group_code_1,
            "MEMBER_CODE": "member1",
            "PLAN_CODE": "plan1",
            "RESERVE_NUMBER": "reserve1",
            "ACTUAL_PRICE": Decimal("6200"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("1000"),
        },
        {
            "MEMBER_GROUP_CODE": group_code_1,
            "MEMBER_CODE": "member2",
            "PLAN_CODE": "plan2",
            "RESERVE_NUMBER": "reserve2",
            "ACTUAL_PRICE": Decimal("12000"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("0"),
        },
        {
            "MEMBER_GROUP_CODE": group_code_2,
            "MEMBER_CODE": "member3",
            "PLAN_CODE": "plan3",
            "RESERVE_NUMBER": "reserve3",
            "ACTUAL_PRICE": Decimal("1500"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("500"),
        }, ]
    mocked_cursor = mocked_connection.return_value.cursor.return_value
    mocked_cursor.fetchmany.side_effect = [query_result, []]

    expected_reserve_summary = query_result

    arg_member_group_codes = ["hoge", "huga"]
    arg_fromdate = datetime.date(2021, 9, 5)
    arg_todate = datetime.date(2022, 9, 6)

    actual_cursor = reserve_repository.get_reserve_summary_cursor(
        mocked_connection.return_value, arg_member_group_codes, arg_fromdate, arg_todate)
    actual_reserve_summary = reserve_repository.get_reserve_list(
        actual_cursor)

    assert actual_reserve_summary == expected_reserve_summary


if __name__ == '__main__':
    pytest.main()
