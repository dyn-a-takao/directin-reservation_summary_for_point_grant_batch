import pytest
from reservation_summary_batch import hotel_group_repository


def test_get_member_group_codes(mocked_http_get):

    api_response_body = ["hoge", "huga", "M000000060", "M000000019"]
    mocked_http_get.return_value.json.return_value = api_response_body

    actual = hotel_group_repository.get_member_group_codes()
    expected = api_response_body

    assert actual == expected


if __name__ == '__main__':
    pytest.main()
