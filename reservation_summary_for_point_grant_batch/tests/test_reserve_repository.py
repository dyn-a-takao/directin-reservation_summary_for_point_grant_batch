import datetime
import pytest
from datetime import date
from decimal import Decimal
from reservation_summary_for_point_grant_batch import reserve_repository


CONFIG_DATA = {
    "reserve_repository": {
        "grace_days_after_checkout": 12,
    },
}


def test_get_reserve_summary(mocked_config_get, mocked_connection):
    mocked_config_get.side_effect = lambda name, key: CONFIG_DATA[name][key]

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
    mocked_cursor.__enter__().fetchall.return_value = query_result

    expected_reserve_summary = [(
        group_code_1, [{
            "MEMBER_CODE": query_result[0]["MEMBER_CODE"],
            "PLAN_CODE": query_result[0]["PLAN_CODE"],
            "RESERVE_NUMBER": query_result[0]["RESERVE_NUMBER"],
            "ACTUAL_PRICE": query_result[0]["ACTUAL_PRICE"],
            "TOTAL_USE_POINT_AMOUNT": query_result[0]["TOTAL_USE_POINT_AMOUNT"],
        }, {
            "MEMBER_CODE": query_result[1]["MEMBER_CODE"],
            "PLAN_CODE": query_result[1]["PLAN_CODE"],
            "RESERVE_NUMBER": query_result[1]["RESERVE_NUMBER"],
            "ACTUAL_PRICE": query_result[1]["ACTUAL_PRICE"],
            "TOTAL_USE_POINT_AMOUNT": query_result[1]["TOTAL_USE_POINT_AMOUNT"],
        }, ]
    ), (
        group_code_2, [{
            "MEMBER_CODE": query_result[2]["MEMBER_CODE"],
            "PLAN_CODE": query_result[2]["PLAN_CODE"],
            "RESERVE_NUMBER": query_result[2]["RESERVE_NUMBER"],
            "ACTUAL_PRICE": query_result[2]["ACTUAL_PRICE"],
            "TOTAL_USE_POINT_AMOUNT": query_result[2]["TOTAL_USE_POINT_AMOUNT"],
        }, ]
    ), ]

    arg_member_group_codes = ["hoge", "huga"]
    arg_fromdate = datetime.date(2021, 9, 5)
    arg_todate = datetime.date(2022, 9, 6)

    actual_reserve_summary_iterator = reserve_repository.get_reserve_summary(
        mocked_connection.return_value, arg_member_group_codes, arg_fromdate, arg_todate)
    actual_reserve_summary = [(group_code, list(summary))
                              for group_code, summary in actual_reserve_summary_iterator]

    assert actual_reserve_summary == expected_reserve_summary


if __name__ == '__main__':
    pytest.main()
