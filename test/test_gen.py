from unittest import TestCase

import tos.lib as lib


class MyTests(TestCase):

    def test_tounixts(self):

        checks = [
            ('2020-01-01', 1577836800),
            ('2020-01-01', 'America/Denver', 1577862000),  # given a date in phx, get correct nix ts
        ]

        for check in checks:

            r = lib.strtime_to_unixts(*check[:-1])

            self.assertEqual(check[-1], r)

