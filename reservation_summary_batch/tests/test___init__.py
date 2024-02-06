import pytest
import sys
import json
import glob
from reservation_summary_batch import ResultCode, main, setup


logger = setup.get_logger(__name__)
CONFIG_DATA = {
    "reserve_repository": {
        "grace_days_after_checkout": 12,
    },
}


def init_testdata_list() -> dict:
    """
    外部ファイルからテストデータ読み込んで初期化
    """

    testdata_path = "reservation_summary_batch/tests/testdata/"
    case_pathlist = glob.glob(f"{testdata_path}*/")

    testdata_map = {}
    for case_path in case_pathlist:
        case_name = case_path.replace(testdata_path, "")
        with open(f"{case_path}/query_result.json") as json_file:
            query_result = json.load(json_file)

        with open(f"{case_path}/api_result.json") as json_file:
            api_result = json.load(json_file)

        csv_file_list = glob.glob(f"{case_path}/expected_summary_*.csv")
        expected_csv_list = []
        for csv_file_name in csv_file_list:
            with open(csv_file_name, newline="\r\n") as csv_file:
                expected_csv_list.append(csv_file.read())
        testdata_map[case_name] = (query_result, api_result, expected_csv_list)

    return testdata_map


@pytest.fixture(params=list(init_testdata_list().values()), ids=list(init_testdata_list().keys()))
def testdata(request):
    return request.param


def test_main_正常終了(mocked_config_get, mocked_http_get, mocked_connection, testdata):
    mocked_config_get.side_effect = lambda name, key: CONFIG_DATA[name][key]
    (query_result, api_result, expected_csv_list) = testdata

    arg_fromdate = "2021-09-05"
    arg_todate = "2022-09-06"
    arg_group_code_list = sorted(
        set([row["MEMBER_GROUP_CODE"] for row in query_result]))

    api_response_body = api_result
    mocked_http_get.return_value.json.return_value = api_response_body

    mocked_cursor = mocked_connection.return_value.cursor.return_value
    mocked_cursor.fetchmany.side_effect = [query_result, []]

    param_fromdate = arg_fromdate.replace("-", "")
    param_todate = arg_todate.replace("-", "")
    expected_file_name_list = [
        f"output/{group_code}/transaction-{param_fromdate}.csv"for group_code in arg_group_code_list]

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
