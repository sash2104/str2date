#!/usr/bin/env python
# coding: utf-8

""" """
from datetime import datetime
from enum import Enum

from str2date.bitset import BitSet


class UnitType:
    DAY, WDAY, WEEK, MONTH, YEAR = range(5)


class Datetime:
    def __init__(self):
        self.units = [None for _ in range(4)]
        self.units[UnitType.DAY] = BitSet(31) # 31桁のbit. 桁が日付に対応
        self.units[UnitType.WDAY] = BitSet(7) # 7桁のbit. 桁が日付に対応
        """
        54桁のbit. date.isocalendar()のweekに準拠
        https://docs.python.org/3/library/datetime.html#datetime.date.isocalendar
        """
        self.units[UnitType.WEEK] = BitSet(54)
        self.units[UnitType.MONTH] = BitSet(12) # 12桁のbit. 桁が月に対応
        self.year = None # ひとまずは年は範囲を持たないとする

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
        self.units[unit].set(n)

    def set_by_datetime(self, d):
        self.units[UnitType.DAY].set(d.day)
        self.units[UnitType.WDAY].set(d.isoweekday())
        self.units[UnitType.WEEK].set(d.isocalendar()[1])
        self.units[UnitType.MONTH].set(d.month)
        self.year = d.year

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
            raiseError("`unit` must not be `UnitType.YEAR`")
        self.units[unit].add(n)

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
        self.units[unit].shift(n)

    def get(self, unit):
        """
        特定の単位 (month, week, wday, day) でセットされている値のリストを返す

        Arguments
        ---------
        unit: UnitType
            時間表現の単位. 年, 月, 週, 曜日, 日

        Returns
        -------
       s: list of int
            指定されたunitでセットされている値のリスト
        """
        if unit == UnitType.YEAR:
            if self.year is None:
                return []
            return [self.year]
        return self.units[unit].get_nonzero_digits()

    def days(self):
        """
        dayでセットされている値のリストを返す

        Returns
        -------
       s: list of int
           dayでセットされている値のリスト
        """
        return self.get(UnitType.DAY)

    def wdays(self):
        """
        wdayでセットされている値のリストを返す

        Returns
        -------
       s: list of int
           wdayでセットされている値のリスト
        """
        return self.get(UnitType.WDAY)

    def weeks(self):
        """
        weekでセットされている値のリストを返す

        Returns
        -------
       s: list of int
           weekでセットされている値のリスト
        """
        return self.get(UnitType.WEEK)

    def months(self):
        """
        monthでセットされている値のリストを返す

        Returns
        -------
       s: list of int
           monthでセットされている値のリスト
        """
        return self.get(UnitType.MONTH)

    def years(self):
        """
        yearでセットされている値のリストを返す

        Returns
        -------
       s: list of int
           yearでセットされている値のリスト
        """
        return self.get(UnitType.YEAR)

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
            if not self.units[UnitType.DAY].check(day):
                return False
        if wday is not None:
            if not self.units[UnitType.WDAY].check(wday):
                return False
        if week is not None:
            if not self.units[UnitType.WEEK].check(week):
                return False
        if month is not None:
            if not self.units[UnitType.MONTH].check(month):
                return False
        if year is not None:
            if year != self.year:
                return False
        return True
