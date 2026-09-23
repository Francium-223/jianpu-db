# scores-suspect —— 被隔离的曲谱(只移不删)

`2026-09-24 02:02` 由 `jianpu2/tools/quarantine_short_scores.py` 移入: **旋律音 < 5 个**,
而检索下限就是 5 个音 —— 这些曲永远不可能被查到, 且实测几乎都是
转写失败的产物(整份谱只剩休止/念白/延长, 真音 1~3 个)。

要恢复: 把文件移回 `../scores/` 再跑 `python3 parse_scores.py`。
