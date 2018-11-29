#!/usr/bin/env python
# coding: utf-8

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
        partial = text[pos:]
        token = match(partial, tokens)
        if token is None:
            pos += 1
        else:
            result.append(tokens[token])
            pos += len(token)
    return result


if __name__ == '__main__':
    _tokens = {
        "次": "r_next",
        "最終日": "r_last_day",
        "ゴールデンウィーク": "p_goldenweek",
    }
    text = "次のゴールデンウィークの最終日"
    result = lexer(text, _tokens)
    print(text, result)
    text = "ゴールデンウィーク最終日"
    result = lexer(text, _tokens)
    print(text, result)
