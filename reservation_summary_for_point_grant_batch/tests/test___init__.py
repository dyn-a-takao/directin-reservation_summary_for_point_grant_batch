import pytest
import sys
import json
import glob
from reservation_summary_for_point_grant_batch import ResultCode, main, setup


logger = setup.get_logger(__name__)
CONFIG_DATA = {
    "reserve_repository": {
        "grace_days_after_checkout": 12,
    },
}


def init_testdata_list():
    testdata_path = "reservation_summary_for_point_grant_batch/tests/testdata/case*/"
    case_list = glob.glob(testdata_path)

    testdata_list = []
    for case_dir in case_list:
        with open(f"{case_dir}/query_result.json") as json_file:
            query_result = json.load(json_file)

        csv_file_list = glob.glob(f"{case_dir}/expected_summary_*.csv")
        expected_csv_list = []
        for csv_file_name in csv_file_list:
            with open(csv_file_name, newline="\r\n") as csv_file:
                expected_csv_list.append(csv_file.read())
        testdata_list.append((query_result, expected_csv_list))

    return testdata_list


@pytest.fixture(params=init_testdata_list())
def testdata(request):
    return request.param


def test_main_正常終了(mocked_config_get, mocked_http_get, mocked_connection, testdata):
    mocked_config_get.side_effect = lambda name, key: CONFIG_DATA[name][key]
    (query_result, expected_csv_list) = testdata

    arg_fromdate = "2021-09-05"
    arg_todate = "2022-09-06"
    arg_group_code_list = sorted(
        set([row["MEMBER_GROUP_CODE"] for row in query_result]))

    api_response_body = ["hoge", "huga"] + arg_group_code_list
    mocked_http_get.return_value.json.return_value = api_response_body

    mocked_cursor = mocked_connection.return_value.cursor.return_value
    mocked_cursor.fetchmany.side_effect = [query_result, []]

    param_fromdate = arg_fromdate.replace("-", "")
    param_todate = arg_todate.replace("-", "")
    expected_file_name_list = [
        f"output/summary_reserve_{param_fromdate}_{param_todate}_{group_code}.csv"for group_code in arg_group_code_list]

    del sys.argv[1:]
    sys.argv.append(arg_fromdate)
    sys.argv.append(arg_todate)
    actual_result = main()
    del sys.argv[1:]

    assert actual_result == ResultCode.SUCCESS

    actual_csv_list = []
    for expected_file_name in expected_file_name_list:
        with open(expected_file_name, newline="\r\n") as actual_csvfile:
            actual_csv_list.append(actual_csvfile.read())
    assert actual_csv_list == expected_csv_list


def test_main_異常終了(mocked_config_get, mocked_http_get, mocked_connection):
    mocked_config_get.side_effect = Exception("test_exception")

    arg_fromdate = "2021-09-05"
    arg_todate = "2022-09-06"

    del sys.argv[1:]
    sys.argv.append(arg_fromdate)
    sys.argv.append(arg_todate)
    actual_result = main()
    del sys.argv[1:]

    assert actual_result == ResultCode.OTHER_ERROR


if __name__ == '__main__':
    pytest.main()
