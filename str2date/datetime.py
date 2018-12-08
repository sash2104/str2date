#!/usr/bin/env python
# coding: utf-8

""" """
from enum import Enum
from bitset import BitSet


class UnitType:
    DAY, WDAY, WEEK, MONTH, YEAR = range(5)


class Datetime:
    def __init__(self):
        self.units = [None for _ in range(4)]
        self.units[UnitType.DAY.value] = BitSet(31) # 31桁のbit. 桁が日付に対応
        self.units[UnitType.WDAY.value] = BitSet(7) # 7桁のbit. 桁が日付に対応
        """
        54桁のbit. date.isocalendar()のweekに準拠
        https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar
        """
        self.units[UnitType.WEEK.value] = BitSet(54)
        self.units[UnitType.MONTH.value] = BitSet(12) # 12桁のbit. 桁が月に対応
        self.year = 0 # ひとまずは年は範囲を持たないとする

    def set(self, n, unit):
        """
        特定の単位 (year, month, week, wday, day) を特定の値にする

        Arguments
        ---------
        n: int
            指定したい値.
        unit: UnitType
            時間表現の単位. 年, 月, 週, 曜日, 日
        """
        if unit == UnitType.YEAR:
            self.year = n
            return
        self.units[unit.value].set(n)

    def add(self, n, unit):
        """
        特定の単位 (month, week, wday, day) に特定の値を追加する
        現時点ではyearはサポートしない

        Arguments
        ---------
        n: int
            指定したい値.
        unit: UnitType
            時間表現の単位. 年, 月, 週, 曜日, 日
        """
        if unit == UnitType.YEAR:
            raise ValueError("`unit` must not be `UnitType.YEAR`")
        self.units[unit.value].add(n)

    def shift(self, n, unit):
        """
        特定の単位 (month, week, wday, day) を特定の値だけずらす

        Arguments
        ---------
        n: int
            指定したい値.
        unit: UnitType
            時間表現の単位. 年, 月, 週, 曜日, 日
        """
        if unit == UnitType.YEAR:
            self.year += n
            return
        self.units[unit.value].shift(n)

    def check(self, day=None, wday=None, week=None, month=None, year=None):
        """
        Datetimeの日付が指定されたunitsの特定の値に合致していればTrueを返す
        Noneの引数は無視する

        Arguments
        ---------
        day: int or None
        wday: int or None
        week: int or None
        month: int or None
        year: int or None

        Returns
        -------
        ret: bool
        """
        if day is not None:
            if not self.units[UnitType.DAY.value].check(day):
                return False
        if wday is not None:
            if not self.units[UnitType.WDAY.value].check(wday):
                return False
        if week is not None:
            if not self.units[UnitType.WEEK.value].check(week):
                return False
        if month is not None:
            if not self.units[UnitType.MONTH.value].check(month):
                return False
        if year is not None:
            if year != self.year:
                return False
        return True
