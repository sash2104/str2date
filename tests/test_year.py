import unittest

from str2date.year import *

class TestYear(unittest.TestCase):
    def test_init(self):
        # 年のみ指定した場合, 全ての日付にフラグが立つ
        y = Year(2018)
        self.assertTrue(y.check(year=2018))
        self.assertTrue(y.check(month=1, day=1))
        self.assertTrue(y.check(month=12, day=31))

        # 月も指定した場合, その月の全ての日付にフラグが立つ
        y = Year(2018, month=1)
        self.assertTrue(y.check(year=2018))
        for day in range(1, 32):
            self.assertTrue(y.check(month=1, day=day))
            self.assertFalse(y.check(month=12, day=day))

        # 日も指定した場合, 全ての月の指定した日付にフラグが立つ
        y = Year(2018, day=1)
        self.assertTrue(y.check(year=2018))
        for month in range(1, 13):
            self.assertTrue(y.check(month=month, day=1))
            self.assertFalse(y.check(month=month, day=2))

        # 月日を指定した場合, 指定した年月日のみにフラグが立つ
        y = Year(2018, month=1, day=1)
        self.assertTrue(y.check(year=2018))
        self.assertTrue(y.check(month=1, day=1))
        self.assertFalse(y.check(month=2, day=1))
        self.assertFalse(y.check(month=1, day=2))
        self.assertFalse(y.check(month=12, day=31))

    def test_filter(self):
        # 一つ指定した場合
        y = Year(2018)
        y.filter(year=2017)
        self.assertTrue(y.check(year=2017))

        # 月を指定した場合, その月以外の全てのフラグがなくなる
        y = Year(2018)
        y.filter(month=1)
        self.assertTrue(y.check(year=2018))
        for day in range(1, 32):
            self.assertTrue(y.check(month=1, day=day))
            self.assertFalse(y.check(month=12, day=day))

        # 日を指定した場合, 各月の指定した日以外の全てのフラグがなくなる
        y = Year(2018)
        y.filter(day=1)
        self.assertTrue(y.check(year=2018))
        for month in range(1, 13):
            self.assertTrue(y.check(month=month, day=1))
            self.assertFalse(y.check(month=month, day=2))

        # 月日を指定した場合, 指定した日付以外の全てのフラグがなくなる
        y = Year(2018)
        y.filter(month=1, day=1)
        self.assertTrue(y.check(year=2018))
        self.assertTrue(y.check(month=1, day=1))
        self.assertFalse(y.check(month=2, day=1))
        self.assertFalse(y.check(month=1, day=2))
        self.assertFalse(y.check(month=12, day=31))

        # 順に指定した場合も複数同時に指定した場合と同じ結果になる
        y = Year(2018)
        y.filter(month=1)
        y.filter(day=1)
        self.assertTrue(y.check(year=2018))
        self.assertTrue(y.check(month=1, day=1))
        self.assertFalse(y.check(month=2, day=1))
        self.assertFalse(y.check(month=1, day=2))
        self.assertFalse(y.check(month=12, day=31))

        # 順に指定した場合, 指定の順番には依存しない
        y = Year(2018)
        y.filter(day=1)
        y.filter(month=1)
        self.assertTrue(y.check(year=2018))
        self.assertTrue(y.check(month=1, day=1))
        self.assertFalse(y.check(month=2, day=1))
        self.assertFalse(y.check(month=1, day=2))
        self.assertFalse(y.check(month=12, day=31))

    def test_remove(self):
        # 月を指定した場合, その月の全ての日付が集合から削除される
        y = Year(2018)
        y.remove(month=1)
        self.assertTrue(y.check(year=2018))
        for day in range(1, 32):
            self.assertFalse(y.check(month=1, day=day))
            self.assertTrue(y.check(month=12, day=day))

        # 日を指定した場合, 全ての月の指定した日付が集合から削除される
        y = Year(2018)
        y.remove(day=1)
        self.assertTrue(y.check(year=2018))
        for month in range(1, 13):
            self.assertFalse(y.check(month=month, day=1))
            self.assertTrue(y.check(month=month, day=2))

        # 月日を指定した場合, 指定した月日の日付が集合から削除される
        y = Year(2018)
        y.remove(month=1, day=1)
        self.assertTrue(y.check(year=2018))
        self.assertFalse(y.check(month=1, day=1))
        self.assertTrue(y.check(month=2, day=1))
        self.assertTrue(y.check(month=1, day=2))
        self.assertTrue(y.check(month=12, day=31))
