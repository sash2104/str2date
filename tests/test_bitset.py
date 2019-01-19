import unittest

from str2date.bitset import BitSet, _trailing_digit, _get_nonzero_digits, _copy

class TestBitSet(unittest.TestCase):
    def test_set(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.set(2)
        self.assertEqual(b.bits, 0b10)
        b.set(4)
        self.assertEqual(b.bits, 0b1000)

    def test_reset(self):
        b = BitSet(4)
        b.set(1)
        b.reset()
        self.assertEqual(b.bits, 0)

    def test_set_all(self):
        # 全ての桁が立つ
        b = BitSet(4)
        b.set_all()
        self.assertEqual(b.bits, 0b1111)

        # どこかの桁が立っていても全ての桁が立つ
        b = BitSet(4)
        b.set(2)
        b.set_all()
        self.assertEqual(b.bits, 0b1111)

    def test_remove(self):
        b = BitSet(4)
        b.set_all()

        # 指定した桁のみ0になる
        b.remove(2)
        self.assertEqual(b.bits, 0b1101)
        b.remove(4)
        self.assertEqual(b.bits, 0b101)

        # すでに0の桁を指定しても0のまま
        b.remove(2)
        self.assertEqual(b.bits, 0b101)

    def test_add(self):
        b = BitSet(4)
        b.add(1)
        self.assertEqual(b.bits, 0b1)
        b.add(2)
        self.assertEqual(b.bits, 0b11)
        b.add(4)
        self.assertEqual(b.bits, 0b1011)

    def test_check(self):
        b = BitSet(4)
        self.assertFalse(b.check(1))
        b.add(1)
        self.assertTrue(b.check(1))
        b.add(2)
        self.assertTrue(b.check(1))
        self.assertTrue(b.check(2))

    def test_set_bits(self):
        b = BitSet(4)
        b.set(1)
        b.set_bits(0b0110)
        self.assertEqual(b.bits, 0b0111)
        b.set_bits(0b1100)
        self.assertEqual(b.bits, 0b1111)

    def test_filter(self):
        b = BitSet(4)
        b.add(2)
        b.add(4)
        self.assertEqual(b.bits, 0b1010)

        bits = b.filter(0b0110)
        self.assertEqual(bits, 0b0010)

    def test_shift_left(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.shift(1, wrap=False)
        self.assertEqual(b.bits, 0b10)
        b.shift(2, wrap=False)
        self.assertEqual(b.bits, 0b1000)
        b.shift(1, wrap=False)
        self.assertEqual(b.bits, 0)

    def test_shift_right(self):
        b = BitSet(4)
        b.set(4)
        self.assertEqual(b.bits, 0b1000)
        b.shift(-1, wrap=False)
        self.assertEqual(b.bits, 0b0100)
        b.shift(-2, wrap=False)
        self.assertEqual(b.bits, 0b0001)
        b.shift(-1, wrap=False)
        self.assertEqual(b.bits, 0)

    def test_circular_shift_left(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.shift(1)
        self.assertEqual(b.bits, 0b10)
        b.shift(2)
        self.assertEqual(b.bits, 0b1000)
        b.shift(1)
        self.assertEqual(b.bits, 0b0001)

    def test_circular_shift_right(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.shift(-1)
        self.assertEqual(b.bits, 0b1000)
        b.shift(-2)
        self.assertEqual(b.bits, 0b0010)
        b.shift(-1)
        self.assertEqual(b.bits, 0b0001)

    def test_trailing_digit(self):
        digit = _trailing_digit(0b0001)
        self.assertEqual(digit, 1)
        digit = _trailing_digit(0b1111)
        self.assertEqual(digit, 1)
        digit = _trailing_digit(0b1110)
        self.assertEqual(digit, 2)
        digit = _trailing_digit(0b1000)
        self.assertEqual(digit, 4)
        digit = _trailing_digit(0b10000000)
        self.assertEqual(digit, 8)

    def test_get_nonzero_digits(self):
        digits = _get_nonzero_digits(0)
        self.assertEqual(digits, [])

        digits = _get_nonzero_digits(0b0001)
        self.assertEqual(digits, [1])

        digits = _get_nonzero_digits(0b1111)
        self.assertEqual(len(digits), 4)
        self.assertTrue(1 in digits)
        self.assertTrue(2 in digits)
        self.assertTrue(3 in digits)
        self.assertTrue(4 in digits)

        digits = _get_nonzero_digits(0b1010)
        self.assertEqual(len(digits), 2)
        self.assertTrue(2 in digits)
        self.assertTrue(4 in digits)

        digits = _get_nonzero_digits(0b10000000)
        self.assertEqual(digits, [8])

    def test_copy(self):
        b_from = BitSet(3)
        b_from.add(2)
        b_from.add(3)
        self.assertEqual(b_from.bits, 0b110)

        b_to = BitSet(3)
        self.assertEqual(b_to.bits, 0)

        " 指定した範囲のコピーがうまくいく "
        _copy(b_from, b_to, 1, 2, 1)
        self.assertEqual(b_to.bits, 0b010)

        " 値は上書きされる "
        _copy(b_from, b_to, 1, 2, 2)
        self.assertEqual(b_to.bits, 0b100)

        " 桁あふれは無視される "
        _copy(b_from, b_to, 2, 3, 3)
        self.assertEqual(b_to.bits, 0b100)
