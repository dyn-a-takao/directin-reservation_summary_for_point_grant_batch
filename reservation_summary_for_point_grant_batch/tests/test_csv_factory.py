import unittest
import datetime
import csv
from decimal import Decimal
from unittest import mock
from reservation_summary_for_point_grant_batch import csv_factory, dyconfig


class Test_dbconnecter(unittest.TestCase):

    excepted_fieldnames = [
        "MEMBER_CODE",
        "PLAN_CODE",
        "RESERVE_NUMBER",
        "ACTUAL_PRICE",
        "TOTAL_USE_POINT_AMOUNT"]
    mocked_file_open = mock.mock_open(read_data="")

    @mock.patch("builtins.open", new=mocked_file_open)
    @mock.patch.object(csv.DictWriter, "writerows")
    @mock.patch.object(csv.DictWriter, "writeheader")
    @mock.patch.object(csv, "DictWriter")
    @mock.patch.object(dyconfig, "get", return_value="output")
    def test_get_connection(self, mocked_get, mocked_csv_DictWriter, mocked_writeheader, mocked_writerows):
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

        excepted_csv_name = f"{mocked_get.return_value}/summary_reserve_{arg_fromdate:%Y%m%d}_{arg_todate:%Y%m%d}_{arg_member_group_code}.csv"

        mocked_csv_DictWriter.writeheader = mocked_writeheader
        mocked_csv_DictWriter.writerows = mocked_writerows
        csv_factory.generate_summary_csv_file(
            arg_reserve_list, arg_fromdate, arg_todate, arg_member_group_code)

        self.mocked_file_open.assert_called_once_with(
            excepted_csv_name, "w", newline="")
        mocked_csv_DictWriter.assert_called_once_with(
            self.mocked_file_open.return_value, fieldnames=self.excepted_fieldnames, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        # mocked_writeheader.assert_called_once_with()
        # mocked_writerows.assert_called_once_with(arg_reserve_list)


if __name__ == '__main__':
    unittest.main()
