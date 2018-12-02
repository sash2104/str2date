# 日本語の日時操作表現をdatetimeのような扱いやすい形式に変換する
- 例えば、現在が2018/1/1で日時操作表現が「来月の月末」であれば、`datetime(2018, 2, 28)`のように変換したい
- 構成は下記の二つ
  - 日時操作表現を中間言語に変換するParser
  - 中間言語をdatetime型もしくは類する形式に変換するParser

## 日時操作表現のParser
イメージを下記に示す

- 次のゴールデンウィークの最終日
  - [次] [ゴールデンウィーク] [最終日]
  - x0 = now()
  - x1 = next(x0, ゴールデンウィーク)
  - x2 = last(x1)
- 12月の2回目の火曜日
  - [12月] [2回目] [火曜日]
  - x0 = now()
  - x1 = set(x0, month=12) and unset(x0, week) and unset(x0, day)
  - x2 = set(x1, wday=火)
- 来週の休日
  - [来週] [休日]
  - x0 = now()
  - x1 = add(x0, week=+1) and unset(x0, day)
  - x2 = set_days(x1, day=<休日全て>) := unset(x1, day) and set_day(x1, day=土, override=false) and set_day(x1, ...)

# Python Version
Python 3.4 or later are supported.

# For Developers
```
$ pip install --editable .
$ dominion
```
## tests
```
pyenv virtualenv -p python3.4 3.4.8 py34
pyenv virtualenv -p python3.5 3.5.5 py35
pyenv virtualenv -p python3.6 3.6.5 py36
pyenv shell py34 py35 py36
tox
```

# memo

## token prefix
- `a_`: ambiguous token (ex: `月`= `a_moon`, which is ambiguous between month and monday)
- `d_`: datetime token (ex: `火曜日` = `d_tuesday`, `ゴールデンウィーク` = `d_goldenweek`)
- `o_`: operational token (ex: `次` = `o_next`, `昨日` = `o_yesterday`)
- `p_`: prefix token (ex: `平成` = `p_heisei`, `西暦` = `p_ad`)
- `s_`: suffix token (ex: `年` = `s_year`, `週間` = `s_week`)

## Emoji-prefix
- :memo: when writing docs
- :bug: when fixing a bug
- :+1: when improving features
- :tada: when adding features
- :construction: work in progress
- :recycle: when refactoring code
- :shower: when removing code or files
- :green_heart: when updating tests
- :shirt: when removing linter warnings or fixing style guides
- :rocket: when improving performance
- :arrow_up: when upgrading dependencies
- :arrow_down: when downgrading dependencies
- :lock: when dealing with security
