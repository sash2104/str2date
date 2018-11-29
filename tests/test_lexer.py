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
