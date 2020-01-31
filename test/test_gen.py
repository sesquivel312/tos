from unittest import TestCase

import tos

class MyTests(TestCase):

    def test_tounixts(self):

        checks = [
            ('2020-01-01', 1577836800),
            ('2020-01-02', 'Asia/Tokyo', 1577862000),  # given a date in phx, get correct nix ts
        ]

        for check in checks:

            r = tos.strtime_to_unixts(*check[:-1])

            self.assertEqual(check[-1], r)

