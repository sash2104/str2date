import unittest

from str2date.dateutil import *

_doy_common_year = [
    (1, 1, 1), (1, 31, 31),
    (2, 1, 32), (2, 28, 59),
    (3, 1, 60), (3, 31, 90),
    (4, 1, 91), (4, 30, 120),
    (5, 1, 121), (5, 31, 151),
    (6, 1, 152), (6, 30, 181),
    (7, 1, 182), (7, 31, 212),
    (8, 1, 213), (8, 31, 243),
    (9, 1, 244), (9, 30, 273),
    (10, 1, 274), (10, 31, 304),
    (11, 1, 305), (11, 30, 334),
    (12, 1, 335), (12, 31, 365)
]
_doy_leap_year = [
    (1, 1, 1), (1, 31, 31),
    (2, 1, 32), (2, 29, 60),
    (3, 1, 61), (3, 31, 91),
    (4, 1, 92), (4, 30, 121),
    (5, 1, 122), (5, 31, 152),
    (6, 1, 153), (6, 30, 182),
    (7, 1, 183), (7, 31, 213),
    (8, 1, 214), (8, 31, 244),
    (9, 1, 245), (9, 30, 274),
    (10, 1, 275), (10, 31, 305),
    (11, 1, 306), (11, 30, 335),
    (12, 1, 336), (12, 31, 366)
]
class TestDateUtil(unittest.TestCase):
    def test_doy_to_monthday(self):
        # common year
        for m, d, doy in _doy_common_year:
            target = doy_to_monthday(doy, 1999)
            self.assertEqual(target, (m, d))
        # leap year
        for m, d, doy in _doy_leap_year:
            target = doy_to_monthday(doy, 2000)
            self.assertEqual(target, (m, d))

    def test_shift_days(self):
        # common year
        y, m, d = shift_days(2001, 2, 28, 1)
        self.assertEqual((2001, 3, 1), (y, m, d))
        y, m, d = shift_days(2001, 3, 1, -1)
        self.assertEqual((2001, 2, 28), (y, m, d))

        # leap year
        y, m, d = shift_days(2000, 2, 28, 1)
        self.assertEqual((2000, 2, 29), (y, m, d))
        y, m, d = shift_days(2000, 3, 1, -1)
        self.assertEqual((2000, 2, 29), (y, m, d))

        # 月を跨ぐ場合
        y, m, d = shift_days(2019, 1, 1, 100)
        self.assertEqual((2019, 4, 11), (y, m, d))
        y, m, d = shift_days(2019, 12, 31, -100)
        self.assertEqual((2019, 9, 22), (y, m, d))

        # 年を跨ぐ場合
        y, m, d = shift_days(2019, 1, 1, 1000)
        self.assertEqual((2021, 9, 27), (y, m, d))
        y, m, d = shift_days(2019, 12, 31, -1000)
        self.assertEqual((2017, 4, 5), (y, m, d))
