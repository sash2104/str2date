import unittest

from str2date.datetime import Datetime, UnitType

class TestDatetime(unittest.TestCase):
    def test_check(self):
        d = Datetime()
        d.set(1, unit=UnitType.DAY)

    def test_set(self):
        d = Datetime()

        d.set(1, unit=UnitType.DAY)
        days = d.days()
        self.assertEqual(days, [1])

        d.set(2, unit=UnitType.WDAY)
        wdays = d.wdays()
        self.assertEqual(wdays, [2])

        d.set(3, unit=UnitType.WEEK)
        weeks = d.weeks()
        self.assertEqual(weeks, [3])

        d.set(4, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [4])

        d.set(5, unit=UnitType.YEAR)
        years = d.years()
        self.assertEqual(years, [5])

        d.set(6, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [6])

    def test_add(self):
        d = Datetime()

        d.add(1, unit=UnitType.DAY)
        days = d.days()
        self.assertEqual(days, [1])

        d.add(2, unit=UnitType.WDAY)
        wdays = d.wdays()
        self.assertEqual(wdays, [2])

        d.add(3, unit=UnitType.WEEK)
        weeks = d.weeks()
        self.assertEqual(weeks, [3])

        d.add(4, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [4])

        d.add(5, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(len(months), 2)
        self.assertTrue(4 in months)
        self.assertTrue(5 in months)

    def test_shift(self):
        d = Datetime()

        d.set(1, unit=UnitType.DAY)
        d.shift(1, unit=UnitType.DAY)
        days = d.days()
        self.assertEqual(days, [2])

        d.set(1, unit=UnitType.WDAY)
        d.shift(1, unit=UnitType.WDAY)
        wdays = d.wdays()
        self.assertEqual(wdays, [2])

        d.set(1, unit=UnitType.WEEK)
        d.shift(1, unit=UnitType.WEEK)
        weeks = d.weeks()
        self.assertEqual(weeks, [2])

        d.set(1, unit=UnitType.MONTH)
        d.shift(1, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [2])
        d.shift(2, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [4])
        d.shift(-2, unit=UnitType.MONTH)
        months = d.months()
        self.assertEqual(months, [2])

        d.set(1, unit=UnitType.YEAR)
        d.shift(1, unit=UnitType.YEAR)
        years = d.years()
        self.assertEqual(years, [2])
        d.shift(2, unit=UnitType.YEAR)
        years = d.years()
        self.assertEqual(years, [4])
        d.shift(-2, unit=UnitType.YEAR)
        years = d.years()
        self.assertEqual(years, [2])

    def test_check(self):
        d = Datetime()

        d.set(1, unit=UnitType.DAY)
        self.assertTrue(d.check(day=1))

        d.set(2, unit=UnitType.WDAY)
        self.assertTrue(d.check(wday=2))

        d.set(3, unit=UnitType.WEEK)
        self.assertTrue(d.check(week=3))

        d.set(4, unit=UnitType.MONTH)
        self.assertTrue(d.check(month=4))

        d.set(5, unit=UnitType.YEAR)
        self.assertTrue(d.check(year=5))

    def test_set_by_datetime(self):
        import datetime
        # wday = 2 (tuesday), week = 1
        day_20180102 = datetime.datetime(2018, 1, 2)
        d = Datetime()
        d.set_by_datetime(day_20180102)

        self.assertTrue(d.check(day=2))
        self.assertTrue(d.check(wday=2))
        self.assertTrue(d.check(week=1))
        self.assertTrue(d.check(month=1))
        self.assertTrue(d.check(year=2018))
