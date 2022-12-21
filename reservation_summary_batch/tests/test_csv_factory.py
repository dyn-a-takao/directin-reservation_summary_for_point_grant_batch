import pytest
import datetime
import csv
from decimal import Decimal
from reservation_summary_batch import csv_factory


excepted_fieldnames = [
    "MEMBER_CODE",
    "PLAN_CODE",
    "RESERVE_NUMBER",
    "ACTUAL_PRICE",
    "TOTAL_USE_POINT_AMOUNT"]


def test_get_connection(mocked_config_get, mocked_csv_DictWriter,   mocked_file_open):
    mocked_config_get.return_value = "output"

    arg_reserve_list = [
        {
            "MEMBER_CODE": "member1",
            "PLAN_CODE": "plan1",
            "RESERVE_NUMBER": "reserve1",
            "ACTUAL_PRICE": Decimal("6200"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("1000"),
        },
        {
            "MEMBER_CODE": "member2",
            "PLAN_CODE": "plan2",
            "RESERVE_NUMBER": "reserve2",
            "ACTUAL_PRICE": Decimal("12000"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("0"),
        },
        {
            "MEMBER_CODE": "member3",
            "PLAN_CODE": "plan3",
            "RESERVE_NUMBER": "reserve3",
            "ACTUAL_PRICE": Decimal("1500"),
            "TOTAL_USE_POINT_AMOUNT": Decimal("500"),
        }, ]
    arg_fromdate = datetime.date(2022, 10, 22)
    arg_todate = datetime.date(2022, 11, 5)
    arg_member_group_code = "membergroup1"

    excepted_csv_name = f"{mocked_config_get.return_value}/summary_reserve_{arg_fromdate:%Y%m%d}_{arg_todate:%Y%m%d}_{arg_member_group_code}.csv"

    actual_csv_name = csv_factory.generate_summary_csv_file(
        arg_reserve_list, arg_fromdate, arg_todate, arg_member_group_code)

    assert actual_csv_name == excepted_csv_name

    mocked_file_open.assert_called_once_with(
        excepted_csv_name, "w", newline="")
    mocked_csv_DictWriter.assert_called_once_with(
        mocked_file_open.return_value.__enter__(), fieldnames=excepted_fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
    mocked_csv_DictWriter.return_value.writeheader.assert_called_once_with()
    mocked_csv_DictWriter.return_value.writerows.assert_called_once_with(
        arg_reserve_list)


if __name__ == '__main__':
    pytest.main()
