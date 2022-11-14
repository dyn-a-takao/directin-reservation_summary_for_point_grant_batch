import unittest
import requests
from unittest import mock
from reservation_summary_for_point_grant_batch import member_repository


class Test_member_repository(unittest.TestCase):

    @mock.patch.object(requests, "get")
    def test_get_member_group_codes(self,mocked_http_get):

        api_response_body = ["hoge", "huga", "M000000060", "M000000019"]
        mocked_http_get.return_value.json.return_value = api_response_body

        actual = member_repository.get_member_group_codes()
        expected = api_response_body
        
        assert actual == expected


if __name__ == '__main__':
    unittest.main()
