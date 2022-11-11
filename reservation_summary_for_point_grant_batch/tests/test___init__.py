import unittest
import pytest
import sys
import csv
from decimal import Decimal
from unittest import mock
from reservation_summary_for_point_grant_batch import ResultCode, dbconnecter, dyconfig, main, setup


class test___init__(unittest.TestCase):

    logger = setup.get_logger(__name__)
    CONFIG_DATA = {
        "reserve_repository": {
            "grace_days_after_checkout": 12,
        },
    }

    @mock.patch.object(dbconnecter, "get_connection")
    @mock.patch.object(dyconfig, "get")
    def test_main(self,  mocked_get, mocked_connection):
        mocked_get.side_effect = lambda name, key: self.CONFIG_DATA[name][key]

        arg_fromdate = "2021-09-05"
        arg_todate = "2022-09-06"
        arg_group_code_1 = "M000000060"
        arg_group_code_2 = "M000000019"

        query_result = [
            {
                "MEMBER_GROUP_CODE": arg_group_code_1,
                "MEMBER_CODE": "member1",
                "PLAN_CODE": "plan1",
                "RESERVE_NUMBER": "reserve1",
                "ACTUAL_PRICE": Decimal("6200"),
                "TOTAL_USE_POINT_AMOUNT": Decimal("1000"),
            },
            {
                "MEMBER_GROUP_CODE": arg_group_code_1,
                "MEMBER_CODE": "member2",
                "PLAN_CODE": "plan2",
                "RESERVE_NUMBER": "reserve2",
                "ACTUAL_PRICE": Decimal("12000"),
                "TOTAL_USE_POINT_AMOUNT": Decimal("0"),
            },
            {
                "MEMBER_GROUP_CODE": arg_group_code_2,
                "MEMBER_CODE": "member3",
                "PLAN_CODE": "plan3",
                "RESERVE_NUMBER": "reserve3",
                "ACTUAL_PRICE": Decimal("1500"),
                "TOTAL_USE_POINT_AMOUNT": Decimal("500"),
            }, ]
        mocked_cursor = mocked_connection.return_value.cursor.return_value
        mocked_cursor.__enter__().fetchall.return_value = query_result

        param_fromdate = arg_fromdate.replace("-", "")
        param_todate = arg_todate.replace("-", "")
        expected_file_name_1 = f"output/summary_reserve_{param_fromdate}_{param_todate}_{arg_group_code_1}.csv"
        expected_file_name_2 = f"output/summary_reserve_{param_fromdate}_{param_todate}_{arg_group_code_2}.csv"
        expected_fieldnames = [
            "MEMBER_CODE",
            "PLAN_CODE",
            "RESERVE_NUMBER",
            "ACTUAL_PRICE",
            "TOTAL_USE_POINT_AMOUNT"]
        expected_file_content_1 = [
            expected_fieldnames,
            [
                query_result[0]["MEMBER_CODE"],
                query_result[0]["PLAN_CODE"],
                query_result[0]["RESERVE_NUMBER"],
                str(query_result[0]["ACTUAL_PRICE"]),
                str(query_result[0]["TOTAL_USE_POINT_AMOUNT"]),
            ],
            [
                query_result[1]["MEMBER_CODE"],
                query_result[1]["PLAN_CODE"],
                query_result[1]["RESERVE_NUMBER"],
                str(query_result[1]["ACTUAL_PRICE"]),
                str(query_result[1]["TOTAL_USE_POINT_AMOUNT"]),
            ],
        ]
        expected_file_content_2 = [
            expected_fieldnames,
            [
                query_result[2]["MEMBER_CODE"],
                query_result[2]["PLAN_CODE"],
                query_result[2]["RESERVE_NUMBER"],
                str(query_result[2]["ACTUAL_PRICE"]),
                str(query_result[2]["TOTAL_USE_POINT_AMOUNT"]),
            ],
        ]

        del sys.argv[1:]
        sys.argv.append(arg_fromdate)
        sys.argv.append(arg_todate)
        actual_result = main()
        del sys.argv[1:]

        assert actual_result == ResultCode.SUCCESS

        with open(expected_file_name_1, newline='') as actual_csvfile:
            spamreader = csv.reader(
                actual_csvfile, delimiter=",", quotechar='"')
            actual_csv_data_list_1 = [row for row in spamreader]
        assert actual_csv_data_list_1 == expected_file_content_1

        with open(expected_file_name_2, newline='') as actual_csvfile:
            spamreader = csv.reader(
                actual_csvfile, delimiter=",", quotechar='"')
            actual_csv_data_list_2 = [row for row in spamreader]
        assert actual_csv_data_list_2 == expected_file_content_2


if __name__ == '__main__':
    unittest.main()
