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
