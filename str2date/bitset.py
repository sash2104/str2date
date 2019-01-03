#!/usr/bin/env python
# coding: utf-8

""" """
import math

_trailing_digit_table = [
1,2,60,3,61,41,55,4,62,33,50,42,56,20,36,5,
63,53,31,34,51,13,15,43,57,17,28,21,37,24,45,6,
64,59,40,54,32,49,19,35,52,30,12,14,16,27,23,44,
58,39,48,18,29,11,26,22,38,47,10,25,46,9,8,7
]

_mask = 0xffffffffffffffff # 2^64-1

def _trailing_digit(x):
    """
    1が立っている末尾の桁を返す
    http://d.hatena.ne.jp/siokoshou/20090704#p1
    0b1110 -> 2, 0b1000 -> 4

    Returns
    -------
    digit: int
        1が立っている末尾の桁
    """
    y = x & -x
    i = ((y * 0x03F566ED27179461) & _mask) >> 58
    return _trailing_digit_table[i]


def _get_nonzero_digits(x):
    """
    0でない桁のリストを返す

    Returns
    -------
    digits: list of int
        0でない桁のリスト
    """
    digits = []
    while x != 0:
        digit = _trailing_digit(x)
        digits.append(digit)
        x = x & (x-1)
    return digits


class BitSet:
    MAX_DIGIT = 64
    def __init__(self, digit):
        assert(0 < digit <= BitSet.MAX_DIGIT)
        self.digit = digit
        self.bits = 0
        self.mask = int(math.pow(2, digit))-1

    def add(self, n):
        """
        n桁目に1を追加する
        """
        assert(1 <= n <= self.digit)
        mask = 1 << (n-1)
        self.bits |= mask

    def check(self, n):
        """
        n桁目が1ならTrue
        """
        assert(1 <= n <= self.digit)
        y = (1 << (n-1)) & self.bits
        return y > 0

    def set(self, n):
        """
        n桁目に1を立てる
        """
        assert(1 <= n <= self.digit)
        self.bits = 1 << (n-1)

    def shift(self, n, wrap=True):
        """
        Arguments
        ---------
        n: int
        wrap: bool
            Trueならcircular shift, そうでないなら溢れた桁は消す
        """
        assert(-self.digit <= n <= self.digit)
        if wrap:
            " circular shift "
            if n > 0:
                self.bits = ((self.bits << n)&self.mask) | (self.bits >> (self.digit-n))
            elif n < 0:
                self.bits = (self.bits >> -n) | ((self.bits << (self.digit+n))&self.mask)
        else:
            if n > 0:
                self.bits = ((self.bits << n)&self.mask)
            elif n < 0:
                self.bits = (self.bits >> -n)
        # if n == 0, do nothing

    def set_all(self):
        """
        全ての桁を1にする
        """
        self.bits = self.mask

    def reset(self):
        """
        全ての桁を0にする
        """
        self.bits = 0

    def remove(self, n):
        """
        指定された桁を0にする
        """
        assert(0 < n <= self.digit)
        mask = 1 << (n - 1)
        self.bits &= ~mask

    def get_nonzero_digits(self):
        """
        deprecated. activeを使う.
        0でない桁のリストを返す

        Returns
        -------
        digits: list of int
            0でない桁のリスト
        """
        return _get_nonzero_digits(self.bits)

    def active(self):
        """
        0でない桁のリストを返す

        Returns
        -------
        digits: list of int
            0でない桁のリスト
        """
        return _get_nonzero_digits(self.bits)
