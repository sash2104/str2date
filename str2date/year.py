#!/usr/bin/env python
# coding: utf-8

""" """

from abc import ABCMeta, abstractmethod
from datetime import datetime

import str2date.dateutil as dateutil
from str2date.timeset import *

class Year:
    """
    一年分の日付の集合を管理.
    とりあえずはshiftは棚上げ. 閏年も気にしない.

    Properties
    ----------
    year: int
    months: list of BitTimeSet
        一ヶ月分の日付を一つのBitTimeSetで管理.
        十二のBitTimeSetで一年分を表現する.
    """

    def __init__(self, year, month=None, day=None):
        self.months = [None] # None is a placeholder for indexing purposes.
        for m in range(1, 13):
            dim = dateutil.DAYS_IN_MONTH[m]
            # 閏年のために、2月はDAYS_IN_MONTHより1日多くしておく
            # self.months.append(BitTimeSet(dim + (m == 2)))
            # 一旦は, 閏年はなかったことにする
            self.months.append(BitTimeSet(dim))
        self.set(year=year, month=month, day=day)

    def add(self, month=None, day=None):
        """
        特定の月日を追加する

        Arguments
        ---------
        month: int
        day: int
        """
        assert (month is not None) or (day is not None), "month or day must be given"
        if month is None:
            assert 1 <= day <= 31
            for m in range(1, 13):
                self.months[m].add(day)
            return
        if day is None:
            assert 1 <= month <= 12
            self.months[month].set_all()
            return
        self.months[month].add(day)

    def set(self, year=None, month=None, day=None):
        """
        特定の時間集合を引数で与えられた値で初期化する.

        Arguments
        ---------
        year: int, optional
        month: int, optional
        day: int, optional
            year, month, dayのいずれか一つは指定する必要がある


        Notes
        -----
        year = None: 年は元の値のままにする.
        year != None: 年を指定された値にする.

        month = None, day = None: 全ての月の全ての日を集合に加える.
        month != None, day = None: 指定された月の全ての日を集合に加える.
        month = None, day != None: 全ての月の指定された日を集合に加える.
        month != None, day != None: 指定された月の指定された日を集合に加える.
        """
        assert (year is not None) or (month is not None) or (day is not None), "At least an argument must be given"
        if year is not None:
            self.year = year
        for m in range(1, 13):
            if month is None:
                if day is None:
                    self.months[m].set_all()
                else:
                    self.months[m].set(day)
            else:
                if m != month:
                    continue
                if day is None:
                    self.months[m].set_all()
                else:
                    self.months[m].set(day)

    def filter(self, year=None, month=None, day=None):
        """
        特定の時間集合から引数で与えられた値以外を取り除く.

        Arguments
        ---------
        year: int, optional
        month: int, optional
        day: int, optional
            year, month, dayのいずれか一つは指定する必要がある

        Notes
        -----
        year = None: 年は元の値のままにする.
        year != None: 年を指定された値にする.

        month = None, day = None: 元の集合のまま.
        month != None, day = None: 指定された月以外の全ての日を集合から削除する.
        month = None, day != None: 全ての月の指定された日以外を集合から削除する.
        month != None, day != None: 指定された月の指定された日以外を集合から削除する.
        """
        assert (year is not None) or (month is not None) or (day is not None), "At least an argument must be given"
        if year is not None:
            self.year = year
        if month is not None:
            for m in range(1, 13):
                if m == month:
                    continue
                self.months[m].reset()
        if day is not None:
            for m in range(1, 13):
                active_days = self.months[m].active()
                if day in active_days:
                    self.months[m].set(day)
                else:
                    self.months[m].reset()

    def remove(self, month=None, day=None):
        """
        特定の時間集合から引数で与えられた値以外を取り除く.

        Arguments
        ---------
        month: int, optional
        day: int, optional
            month, dayのいずれか一つは指定する必要がある

        Notes
        -----
        month != None, day = None: 指定された月の全ての日を集合から削除する.
        month = None, day != None: 全ての月の指定された日を集合から削除する.
        month != None, day != None: 指定された月の指定された日を集合から削除する.
        指定された条件に該当する要素が集合にない場合は何もしない.
        """
        assert (month is not None) or (day is not None), "At least an argument must be given"
        if month is None and day is not None:
            for m in range(1, 13):
                self.months[m].remove(day)
            return
        if month is not None and day is None:
            self.months[month].reset()
            return
        self.months[month].remove(day)

    def shift(self, year=None, month=None, day=None):
        """
        特定の時間集合の要素を引数で与えられた値だけずらす.
        集合の要素の最大値・最小値が存在し、ずらした結果閾値を超えてしまった場合、
        回り込ませるかは継承先のクラス毎に異なる

        Arguments
        ---------
        year: int
        month: int
        day: int
        """
        assert (year is not None) or (month is not None) or (day is not None), "At least an argument must be given"
        pass

    def active(self):
        """
        日付集合の要素のリストを返す

        Returns
        -------
        s: list of datetime.datetime
            日付のリスト
        """
        if self.year is None:
            return []
        active_dates = []
        for m in range(1, 13):
            days = self.months[m].active()
            for d in days:
                active_dates.append(datetime(self.year, m, d))
        return active_dates

    def first(self):
        """
        日付集合の要素のうち一番早い日を返す

        Returns
        -------
        s: datetime.datetime or None
            一番早い日
        """
        active_dates = self.active()
        if len(active_dates) == 0:
            return None
        else:
            return active_dates[0]

    def last(self):
        """
        日付集合の要素のうち一番遅い日を返す

        Returns
        -------
        s: datetime.datetime or None
            一番早い日
        """
        active_dates = self.active()
        if len(active_dates) == 0:
            return None
        else:
            return active_dates[-1]

    def check(self, year=None, month=None, day=None):
        """
        引数で与えられた値が集合に含まれていればTrue, そうでなければFalse

        Arguments
        ---------
        year: int
        month: int
        day: int

        Returns
        -------
        ret: bool
            dateが集合に含まれていればTrue.
        """
        assert (year is not None) or (month is not None) or (day is not None), "At least an argument must be given"
        if year is not None:
            if self.year != year:
                return False
        if month is not None:
            assert day is not None, "Month and day both must be given"
            return self.months[month].check(day)
        return True
