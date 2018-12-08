import unittest

from str2date.bitset import BitSet, _trailing_digit, _get_nonzero_digits

class TestBitSet(unittest.TestCase):
    def test_set(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.set(2)
        self.assertEqual(b.bits, 0b10)
        b.set(4)
        self.assertEqual(b.bits, 0b1000)

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

    def test_shift_left(self):
        b = BitSet(4)
        b.set(1)
        self.assertEqual(b.bits, 0b1)
        b.shift(1)
        self.assertEqual(b.bits, 0b10)
        b.shift(2)
        self.assertEqual(b.bits, 0b1000)
        b.shift(1)
        self.assertEqual(b.bits, 0b0001)

    def test_shift_right(self):
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
