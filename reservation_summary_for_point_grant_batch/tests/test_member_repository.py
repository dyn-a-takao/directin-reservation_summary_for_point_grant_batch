import unittest
from reservation_summary_for_point_grant_batch import member_repository


class Test_member_repository(unittest.TestCase):

    def test_get_member_group_codes(self):
        actual = member_repository.get_member_group_codes()
        expected = ["hoge", "huga", "M000000060", "M000000019"]
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
