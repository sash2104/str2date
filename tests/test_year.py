import unittest

from datetime import datetime
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

    def test_first(self):
        # 年のみ指定した場合
        y = Year(2018)
        d = y.first()
        self.assertEqual(str(d.date()), "2018-01-01")

        # 月を指定した場合
        y = Year(2018, 2)
        d = y.first()
        self.assertEqual(str(d.date()), "2018-02-01")

        # 月日を指定した場合
        y = Year(2018, 2, 2)
        d = y.first()
        self.assertEqual(str(d.date()), "2018-02-02")

        # 複数の日 (1/1, 2/2, 3/3) がある場合は一番早い日が返ってくる
        y.add(month=1, day=1)
        y.add(month=3, day=3)
        d = y.first()
        self.assertEqual(str(d.date()), "2018-01-01")

    def test_last(self):
        # 年のみ指定した場合
        y = Year(2018)
        d = y.last()
        self.assertEqual(str(d.date()), "2018-12-31")

        # 月を指定した場合
        y = Year(2018, 2)
        d = y.last()
        self.assertEqual(str(d.date()), "2018-02-28")

        # 月日を指定した場合
        y = Year(2018, 2, 2)
        d = y.last()
        self.assertEqual(str(d.date()), "2018-02-02")

        # 複数の日 (1/1, 2/2, 3/3) がある場合は一番早い日が返ってくる
        y.add(month=1, day=1)
        y.add(month=3, day=3)
        d = y.last()
        self.assertEqual(str(d.date()), "2018-03-03")

    def test_next(self):
        # 2018/1/1と2018/2/2の二日間を集合に加える
        y = Year(2018, 1, 1)
        y.set(2018, 2, 2)

        # 2018/1/1の方が早いのでそちらが返る
        d = y.next(datetime(2017, 1, 1))
        self.assertEqual(str(d.date()), "2018-01-01")

        # 日付が同じ場合はnextの対象から外れる
        d = y.next(datetime(2018, 1, 1))
        self.assertEqual(str(d.date()), "2018-02-02")

        # nextの対象がないときはNoneが返る
        d = y.next(datetime(2018, 2, 2))
        self.assertIsNone(d)

    def test_before(self):
        # 2018/1/1と2018/2/2の二日間を集合に加える
        y = Year(2018, 1, 1)
        y.set(2018, 2, 2)

        # 2018/2/2の方が遅いのでそちらが返る
        d = y.before(datetime(2019, 1, 1))
        self.assertEqual(str(d.date()), "2018-02-02")

        # 日付が同じ場合はbeforeの対象から外れる
        d = y.before(datetime(2018, 2, 2))
        self.assertEqual(str(d.date()), "2018-01-01")

        # beforeの対象がないときはNoneが返る
        d = y.before(datetime(2018, 1, 1))
        self.assertIsNone(d)

    def test_active(self):
        " common day "
        y = Year(2020, 2, 28)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2020, 2, 28))

        " leap day "
        y = Year(2020, 2, 29)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2020, 2, 29))

        " multiple days "
        y = Year(2020, 1, 1)
        y.add(month=12, day=31)
        dates = y.active()
        self.assertEqual(len(dates), 2)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2020, 1, 1))
        self.assertEqual((dates[1].year, dates[1].month, dates[1].day), (2020, 12, 31))

    def test_shift(self):
        y = Year(2018, 1, 1)
        y.shift(day=1)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2018, 1, 2))

        y = Year(2018, 1, 1)
        y.shift(day=30)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2018, 1, 31))

        " common year "
        y = Year(2018, 2, 28)
        y.shift(day=1)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2018, 3, 1))

        " leap year "
        y = Year(2020, 2, 28)
        y.shift(day=1)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2020, 2, 29))

        " 月を跨ぐ場合 "
        y = Year(2018, 1, 1)
        y.shift(day=364)
        dates = y.active()
        self.assertEqual(len(dates), 1)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2018, 12, 31))

        " 境界値. あふれた分はなくなる "
        y = Year(2018, 12, 31)
        y.shift(day=1)
        dates = y.active()
        self.assertEqual(len(dates), 0)

        " multiple shifts."
        y = Year(2018, 1, 1)
        y.add(month=3, day=31)
        y.shift(day=1)
        dates = y.active()
        self.assertEqual(len(dates), 2)
        self.assertEqual((dates[0].year, dates[0].month, dates[0].day), (2018, 1, 2))
        self.assertEqual((dates[1].year, dates[1].month, dates[1].day), (2018, 4, 1))
