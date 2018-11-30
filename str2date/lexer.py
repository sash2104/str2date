#!/usr/bin/env python
# coding: utf-8

import unicodedata

""" 日時操作表現をtoken列に変換する
例: 次のゴールデンウィークの最終日 -> [次, ゴールデンウィーク, 最終日]
"""

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


def lexer(text, tokens):
    """
    textを先頭から読み込み、tokens中で該当したtokenのlistを返す

    Arguments
    ---------
    text: str
    tokens: map of {str: str}
        tokenの文字列をkey, 正規化された表現をvalueにもつdict

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
            result.append(tokens[token])
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
        "次": "r_next",
        "最終": "r_last",
        "月": "a_moon",
        "日": "a_sun",
        "ゴールデンウィーク": "p_goldenweek",
        "火曜日": "p_tuesday",
        "火曜": "p_tuesday",
    }
    text = "次のゴールデンウィークの最終日"
    result = lexer(text, _tokens)
    print(text, result)
    text = "12月の火曜日"
    result = lexer(text, _tokens)
    print(text, result)
