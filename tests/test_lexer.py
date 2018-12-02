import unittest

import str2date.lexer as lx

class TestLexer(unittest.TestCase):
    def test_match(self):
        tokens = {"次": "1", "ゴールデンウィーク": "2"}
        token = lx.match("ゴールデンウィークの最終日", tokens)
        self.assertEqual(token, "ゴールデンウィーク")

    def test_match_none(self):
        tokens = {"次": "1", "ゴールデンウィーク": "2"}
        token = lx.match("ゴールデンウィーの最終日", tokens)
        self.assertEqual(token, None)

    def test_match_longest(self):
        tokens = {"a": "1", "aa": "2", "aaa": "3"}
        token = lx.match("aaa", tokens)
        self.assertEqual(token, "aaa")

    def test_lexer(self):
        tokens = {"a": "1", "aa": "2", "aaa": "3"}
        result = lx.lexer("aaaaa", tokens)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "3")
        self.assertEqual(result[1], "2")

    def test_lexer_numeric(self):
        tokens = {"a": "1", "aa": "2", "aaa": "3"}
        result = lx.lexer("12aa345aaa6789", tokens)
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], 12)
        self.assertEqual(result[2], 345)
        self.assertEqual(result[4], 6789)

    def test_lexer_or(self):
        tokens = {"日": "d_sunday", "月": "d_monday",
                  "火": "d_tuesday", "水": "d_wednesday",
                  "木": "d_thirsday", "金": "d_friday",
                  "土": "d_saturday"}
        result = lx.lexer("日月火水木金土", tokens)
        self.assertEqual(len(result), 7 + 6) # o_or tokenが間に6つ追加される
        self.assertEqual(result[0], "d_sunday")
        self.assertEqual(result[2], "d_monday")
        self.assertEqual(result[4], "d_tuesday")
        self.assertEqual(result[6], "d_wednesday")
        self.assertEqual(result[8], "d_thirsday")
        self.assertEqual(result[10], "d_friday")
        self.assertEqual(result[12], "d_saturday")
        for i in range(6):
            self.assertEqual(result[1+i*2], "o_or")

    def test_lexer_ambiguous(self):
        tokens = {"月": "a_moon", "火": "d_tuesday"}
        disambiguate_map = {"d_": {"a_moon": "d_monday"}, "s_": {"a_moon": "s_month"}}
        result = lx.lexer("12月", tokens, disambiguate_map)
        self.assertEqual(result[1], "s_month")
        result = lx.lexer("月火", tokens, disambiguate_map)
        self.assertEqual(result[0], "d_monday")
        result = lx.lexer("火月", tokens, disambiguate_map)
        self.assertEqual(result[-1], "d_monday")
