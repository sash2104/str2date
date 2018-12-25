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

    def set_all(self):
        self.timeset.set_all()

    def shift(self, n, wrap=True, max_threshold=None):
        """
        ずらした結果集合の要素の最大値・最小値を超えてしまった場合は回り込ませる.
        timesetの最大値が5, shift前のtimesetの要素が3, nが4なら
        shift後のtimesetの要素は(3+4)%5=2となる

        Arguments
        ---------
        n: int
        max_threshold: None or int, optional
            集合の最大値. Noneの場合は元の最大値を使用.
            日数のように、最大31日あるが2月や9月のように28日や30日しかない月で、
            最大値の31よりも小さい値を閾値としたい場合に使用する.
            NOTE: 現時点では未実装のためこの値は使用できない
        wrap: bool, optional
            Trueなら、ずらした結果集合の要素の最大値・最小値を超えてしまった場合に回り込ませる.
            timesetの最大値が5, shift前のtimesetの要素が3, nが4なら
            shift後のtimesetの要素は(3+4)%5=2となる
            Falseなら、ずらした結果集合の要素の最大値・最小値を超えてしまった場合は超えた分は無視する.
            timesetの最大値が5, shift前のtimesetの要素が3, nが4なら
            shift後のtimesetの要素は(3+4)=7となり最大値を超えるのでtimesetの要素はなくなる
        """
        self.timeset.shift(n, wrap=wrap)

    def active(self):
        return self.timeset.get_nonzero_digits()

    def check(self, n):
        return self.timeset.check(n)

    def reset(self):
        self.timeset.reset()

    def remove(self, n):
        self.timeset.remove(n)


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
    """ intのlistで時間表現の集合を管理

    Arguments
    ---------
    min_threshold: int or None
        集合の要素の最小値. Noneの場合は最小値なし
    max_threshold: int or None
        集合の要素の最大値. Noneの場合は最大値なし
    """
    def __init__(self, min_threshold=None, max_threshold=None):
        self.timeset = []
        self.min_threshold = min_threshold
        self.max_threshold = max_threshold

    def add(self, n):
        self.timeset.append(n)

    def set(self, n):
        self.timeset = [n]

    def shift(self, n, max_threshold=None):
        """
        max_thoresholdは, shiftの引数 -> IntTimeSetのメンバ変数の優先順位で参照する
        どちらもNoneの場合は回り込みは発生しない.
        そうでない場合、ずらした結果集合の要素の最大値・最小値を超えてしまった場合は回り込ませる.
        timesetの最大値が5, shift前のtimesetの要素が3, nが4なら
        shift後のtimesetの要素は(3+4)%5=2となる
        min_thoresholdは, 現状shiftのみで挙動を変更させたい場合が思いつかないので引数に含めていない

        Arguments
        ---------
        max_threshold: None or int
            回り込ませる場合の最大値. Noneの場合は元の最大値を使用.
            日数のように、最大31日あるが2月や9月のように28日や30日しかない月で、
            最大値の31よりも小さい値で回り込ませたい場合に使用する.
        """
        min_t = self.min_threshold
        max_t = self.max_threshold if max_threshold is None else max_threshold
        if max_t is None:
            diff = min_t
        else:
            if min_t is None:
                diff = max_t
            else:
                diff = max_t - min_t + 1
        for i in range(len(self.timeset)):
            if diff is None:
                self.timeset[i] += n
            elif n >= 0:
                self.timeset[i] += (n % diff)
            else:
                self.timeset[i] -= abs(n) % diff

    def active(self):
        return self.timeset

    def check(self, n):
        return n in self.timeset


class YearSet(IntTimeSet):
    def __init__(self):
        super().__init__()


