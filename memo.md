# links
- https://ja.wikipedia.org/wiki/%E6%93%8D%E8%BB%8A%E5%A0%B4%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0

# token列の例
- どのtoken列でも、はじめにd:nowが入るイメージ
- 来週の土日 = 来週の土か日
  - [来, 週, 土, !か, 日]
  - "!か" は補完したもの
  - [o:next, s:week, d:saturday, o:or, d:sunday]

- 12月の最終日
 - [12, 月, 最終, 日]
 - [12, s:month, o:last, s:day]

- 次のゴールデンウィークの次の連休
 - [次, ゴールデンウィーク, 次, 連休]
 - [o:next, d:goldenweek, o:next, o:holidays]

- 2020年の13日の金曜日
 - [2020, 年, 13, 日, 金曜日]
 - [2020, s:year, 13, s:day, d:friday]

# tokenの結合
- num + s -> d
  - 2020, 年
  - 2020, s:year -> d:(year=2000)
- o + s -> o
  - 来, 週
  - o:next, s:week -> o:next:week
- o + d -> d
  - 次, 火曜日
  - o:next, d:tuesday
  - d1 = set(d0, wday = tuesday)
  - d2 = next(d0, d1, week) := d1 if d0 < d1 else add(d1, week=1)
- d + d -> d
  - 明日
  - d:tomorrow
  - d1 = add(d0, day=1)
