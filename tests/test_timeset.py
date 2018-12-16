import unittest

from str2date.timeset import *

class TestTimeSet(unittest.TestCase):
    def test_bittimeset(self):
        bts = BitTimeSet(n=3)
        # はじめは集合に何も含まれない
        self.assertEqual(bts.active(), [])
        for i in range(1, 4):
            self.assertFalse(bts.check(i))

        # 1をsetすると1のみが集合に含まれる
        bts.set(1)
        self.assertEqual(bts.active(), [1])

        # 2をaddすると1と2が集合に含まれる
        bts.add(2)
        target = bts.active()
        self.assertEqual(len(target), 2)
        self.assertTrue(bts.check(1))
        self.assertTrue(bts.check(2))

        # 3をsetすると3のみが集合に含まれる
        bts.set(3)
        self.assertEqual(bts.active(), [3])

        # 1をshiftすると回り込みが発生し(3+1)%3=1のみが集合に含まれる
        bts.shift(1)
        self.assertEqual(bts.active(), [1])

        # -1をshiftすると回り込みが発生し[1, 2]が[3, 1]になる
        bts.add(2)
        bts.shift(-1)
        target = bts.active()
        self.assertEqual(len(target), 2)
        self.assertTrue(bts.check(1))
        self.assertTrue(bts.check(3))

    def test_inttimeset(self):
        its = IntTimeSet()
        # はじめは集合に何も含まれない
        self.assertEqual(its.active(), [])
        self.assertFalse(its.check(1))

        # 1をsetすると1のみが集合に含まれる
        its.set(1)
        self.assertEqual(its.active(), [1])

        # 2をaddすると1と2が集合に含まれる
        its.add(2)
        target = its.active()
        self.assertEqual(len(target), 2)
        self.assertTrue(its.check(1))
        self.assertTrue(its.check(2))

        # 3をsetすると3のみが集合に含まれる
        its.set(3)
        self.assertEqual(its.active(), [3])

        # 1をshiftすると3+1=4が集合に含まれる
        its.shift(1)
        self.assertEqual(its.active(), [4])

        # -1をshiftすると[4, 2]が[3, 1]になる
        its.add(2)
        its.shift(-1)
        target = its.active()
        self.assertEqual(len(target), 2)
        self.assertTrue(its.check(1))
        self.assertTrue(its.check(3))

    def test_inttimeset_threshold(self):
        its = IntTimeSet(min_threshold=1, max_threshold=3)
        # 閾値以上の値をshiftさせると回り込む
        its.set(1)
        its.shift(3)
        self.assertEqual(its.active(), [1])

        # shiftの引数にmax_thresholdがあればそちらを優先して回り込む
        its.shift(2, max_threshold=2)
        self.assertEqual(its.active(), [1])
        its.shift(3, max_threshold=2)
        self.assertEqual(its.active(), [2])
        its.shift(8, max_threshold=4)
        self.assertEqual(its.active(), [2])
        its.shift(-6, max_threshold=3)
        self.assertEqual(its.active(), [2])
        its.shift(-4, max_threshold=3)
        self.assertEqual(its.active(), [1])
