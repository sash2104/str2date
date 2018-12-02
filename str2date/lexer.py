#!/usr/bin/env python
# coding: utf-8

import unicodedata

""" 日時操作表現をtoken列に変換する
例: 次のゴールデンウィークの最終日
    -> [次, ゴールデンウィーク, 最終, 日]
    -> [o_next, d_goldenweek, o_last, s_day]
"""

_wdays = set(["日", "月", "火", "水", "木", "金", "土"])

def match(text, tokens):
    """
    textの文頭に一致するtokenを最長一致で探す

    Arguments
    ---------
    text: str
    tokens: map of {str: str}
        tokenの文字列をkey, 正規化された表現をvalueにもつdict

    Returns
    -------
    token: str or None
        一致するtokenがあればそのtoken、なければNoneを返す
    """
    MAX_LEN = 15
    target_len = min(MAX_LEN, len(text))
    while target_len > 0:
        target = text[:target_len]
        if target in tokens:
            return target
        target_len -= 1
    return None


def lexer(text, tokens, disambiguation_map=None):
    """
    textを先頭から読み込み、tokens中で該当したtokenのlistを返す

    Arguments
    ---------
    text: str
    tokens: dict of {str: str}
        tokenの文字列をkey, 正規化された表現をvalueにもつdict
    disambiguation_map: dict of {str: dict of {str: str}
        あいまい性のあるtokenの変換辞書
        変換先のtokenのprefixをkey, {変換元のtoken: 変換先のtoken} をvalueにもつ
        例: {"d_": {"a_moon": "d_monday"}, "s_": {"a_moon": "s_month"}}

    Returns
    -------
    result: list of str
        tokenのlistを返す
    """
    pos = 0
    result = []
    while pos < len(text):
        c = text[pos]

        # 数値表現を取得する
        is_numeric = c.isnumeric()
        token_number = 0
        while c.isnumeric():
            d = unicodedata.numeric(c)
            token_number *= 10
            token_number += d
            pos += 1
            if pos >= len(text):
                break
            c = text[pos]
        if is_numeric:
            result.append(int(token_number))
            continue

        # 数値以外の表現を取得する
        partial = text[pos:]
        token = match(partial, tokens)
        if token is None:
            pos += 1
        else:
            token_id = tokens[token]
            if token_id.startswith("a_"):
                assert disambiguation_map is not None
                # あいまい性のあるトークンのあいまい性の解消
                # あいまい性のあるトークンは "日" (day or sunday), "月" (month or monday) の二種類
                prev_c = text[pos-1] if pos > 0 else None
                next_c = text[pos+1] if pos < len(text) - 1 else None
                if prev_c in _wdays or next_c in _wdays:
                    # 日月, 土日, 月水金, のように複数曜日の表現の場合のみd_とみなす
                    token_id = disambiguation_map["d_"][token_id]
                else:
                    token_id = disambiguation_map["s_"][token_id]
            if token in _wdays and token_id.startswith("d_"):
                # "土日"のように複数曜日の指定を行う表現は"土 or 日"と解釈し, orを追加する
                prev_c = text[pos-1] if pos > 0 else None
                if prev_c in _wdays:
                    result.append("o_or")
            result.append(token_id)
            pos += len(token)
    return result


def load_tokens(fp):
    tokens = {}
    for line in fp:
        token, normalized = line.rstrip().split('\t')
        tokens[token] = normalized
    return tokens


if __name__ == '__main__':
    _tokens = {
        "次": "o_next",
        "月": "a_moon",
        "日": "a_sun",
        "ゴールデンウィーク": "d_goldenweek",
        "火曜日": "d_tuesday",
        "火曜": "d_tuesday",
        "火": "d_tuesday",
    }
    _disambiguation_map = {
        "d_": {"a_moon": "d_monday", "a_sun": "d_sunday"},
        "s_": {"a_moon": "s_month", "a_sun": "s_day"}
    }

    text = "次のゴールデンウィークの最終日"
    result = lexer(text, _tokens, _disambiguation_map)
    print(text, result)

    text = "12月の火曜日"
    result = lexer(text, _tokens, _disambiguation_map)
    print(text, result)

    text = "5月の日月火"
    result = lexer(text, _tokens, _disambiguation_map)
    print(text, result)
