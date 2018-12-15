#!/usr/bin/env python
# coding: utf-8

""" """

from abc import ABCMeta, abstractmethod

from str2date.bitset import BitSet


class TimeSet(metaclass=ABCMeta):
    """
    特定の時間表現の単位での集合
    """
    @abstractmethod
    def add(self, n):
        """
        集合に引数で与えられた値を追加する

        Arguments
        ---------
        n: int
            集合に追加したい値.
        """
        raise NotImplementedError()

    @abstractmethod
    def set(self, n):
        """
        集合を引数で与えられた値のみにする

        Arguments
        ---------
        n: int
            集合の要素として指定したい値.
        """
        raise NotImplementedError()

    @abstractmethod
    def shift(self, n, **kwargs):
        """
        集合の要素を引数で与えられた値だけずらす.
        集合の要素の最大値・最小値が存在し、ずらした結果閾値を超えてしまった場合、
        回り込ませるかは継承先のクラス毎に異なる

        Arguments
        ---------
        n: int
            集合の要素をいくつずらすかの値.
        """
        raise NotImplementedError()

    @abstractmethod
    def active(self):
        """
        集合の要素のリストを返す

        Returns
        -------
        s: list of int
            集合に含まれている要素のリスト
        """
        raise NotImplementedError()

    @abstractmethod
    def check(self, n):
        """
        引数で与えられた値が集合に含まれていればTrue, そうでなければFalse

        Arguments
        ---------
        n: int
            確認したい値.

        Returns
        -------
        ret: bool
            nが集合に含まれていればTrue.
        """
        raise NotImplementedError()


class BitTimeSet(TimeSet):
    """ BitSetで時間表現の集合を管理 """
    def __init__(self, n):
        self.timeset = BitSet(n)

    def add(self, n):
        self.timeset.add(n)

    def set(self, n):
        self.timeset.set(n)

    def shift(self, n, max_threshold=None):
        """
        ずらした結果集合の要素の最大値・最小値を超えてしまった場合は回り込ませる.
        timesetの最大値が5, shift前のtimesetの要素が3, nが4なら
        shift後のtimesetの要素は(3+4)%5=2となる

        Arguments
        ---------
        max_threshold: None or int
            回り込ませる場合の最大値. Noneの場合は元の最大値を使用.
            日数のように、最大31日あるが2月や9月のように28日や30日しかない月で、
            最大値の31よりも小さい値で回り込ませたい場合に使用する.
            NOTE: 現時点では未実装のためこの値は使用できない
        """
        self.timeset.shift(n)

    def active(self):
        return self.timeset.get_nonzero_digits()

    def check(self, n):
        return self.timeset.check(n)


class DayTimeSet(BitTimeSet):
    """ 日付の集合 """
    def __init__(self):
        super().__init__(31)


class WdayTimeSet(BitTimeSet):
    """ 曜日の集合 """
    def __init__(self):
        super().__init__(7)


class WeekTimeSet(BitTimeSet):
    """ 週の集合 """
    def __init__(self):
        super().__init__(53)


class MonthTimeSet(BitTimeSet):
    """ 月の集合 """
    def __init__(self):
        super().__init__(12)


class IntTimeSet(TimeSet):
    """ intのlistで時間表現の集合を管理 """
    def __init__(self):
        self.timeset = []

    def add(self, n):
        self.timeset.append(n)

    def set(self, n):
        self.timeset = [n]

    def shift(self, n):
        """
        IntTimeSetは最大値、最小値を持たないため回り込みも発生しない
        """
        for i in range(len(self.timeset)):
            self.timeset[i] += n

    def active(self):
        return self.timeset

    def check(self, n):
        return n in self.timeset


class YearSet(IntTimeSet):
    def __init__(self):
        super().__init__()


