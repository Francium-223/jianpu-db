#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定案实验: 本语料里的时值字母 `h` 到底是**二分音符(2 拍)**还是**六十四分音符(1/64 拍)**?

背景(两条互相矛盾的证据):
  * `score.py:expand_keep_length` 的 docstring 写 "c=四分 q=八分 s=十六分 d=三十二分 h=二分" -> h=2 拍
  * 内置 jianpu-ly(jianpulocal/mxml2jp-main/jianpu-ly_patched.py:1106)写
    `types={"64th":"h","32nd":"d","16th":"s","eighth":"q","quarter":"","half":" -","whole":" - - -"}`
    -> **h = 六十四分音符**, 二分音符写作 `1 -`(数字 + 破折号)

关键旁证: 语料里 `status=midi` 的东方曲是**用那个 jianpu-ly 转出来的**(tools/tlm2jp 那条链路),
它们的 `h` 语义是**确定的 = 64 分音符**。所以只要比较"midi 曲"与"OCR 曲"里 `h` 的用法
(邻居时值、是否跟破折号、单位 token 的拍数), 就能判断 OCR 曲的 `h` 是不是同一个意思
—— OCR 模型正是拿这套语料微调出来的。

判据:
  ① h 的邻居: 若 h=64分, 它该出现在**快速走句**里(邻居多为 d/s/q 或另一个 h);
     若 h=二分, 它更可能**后面跟 `-`**(简谱的二分写法 `1 -`)或周围是 q/纯数字。
  ② 同一首里 h 与 d(32分)的搭配密度。
  ③ 按 h=2 与 h=1/64 分别算"每 token 平均拍数", 看哪个落在合理区间(简谱旋律一般 0.3~1.2 拍/token)。
"""
import json
import sys
import collections

sys.path.insert(0, 'jianpu2/skills/jianpu-melody-lookup')
import jptok


def dur_letter(tok):
    return jptok.duration_letter(tok)


rows = []
for line in open('jianpu-db/data.jsonl', encoding='utf-8'):
    r = json.loads(line)
    rows.append(r)

# midi 组的曲不在 data.jsonl 里(白名单只收 ok/ocr) -> 直接读源文件的**展开版**
import io
import os
import re
midi_added = 0
for fn in os.listdir('jianpu-db/scores'):
    if not fn.endswith('.txt') or fn.endswith('_expand.txt'):
        continue
    raw = io.open('jianpu-db/scores/' + fn, encoding='utf-8').read()
    if not re.search(r'(?m)^status=midi\s*$', raw):
        continue
    exp = 'jianpu-db/scores/' + fn[:-4] + '_expand.txt'
    if not os.path.isfile(exp):
        continue
    body = io.open(exp, encoding='utf-8').read()
    body = body.split('%---', 1)[-1] if '%---' in body else body
    rows.append({'file': [fn], 'status': 'midi', 'score': ' '.join(body.split())})
    midi_added += 1
print('(补入 status=midi 的曲 %d 首, 取自 *_expand.txt)' % midi_added)

groups = collections.defaultdict(lambda: {'songs': 0, 'h': 0, 'nbr': collections.Counter(),
                                          'next_dash': 0, 'beats_h2': 0.0, 'beats_h64': 0.0,
                                          'tokens': 0})
for r in rows:
    sc = r.get('score') or ''
    toks = sc.split()
    if 'h' not in sc:
        continue
    st = r.get('status') or '?'
    g = groups[st]
    g['songs'] += 1
    for i, t in enumerate(toks):
        p = jptok.parse_token(t)
        if not p or p[0] is None:
            continue
        g['tokens'] += 1
        g['beats_h2'] += jptok.beat(t) if dur_letter(t) != 'h' else 2.0
        g['beats_h64'] += jptok.beat(t) if dur_letter(t) != 'h' else 0.0625
        if dur_letter(t) == 'h':
            g['h'] += 1
            prev = next((toks[j] for j in range(i - 1, -1, -1)
                         if jptok.parse_token(toks[j]) and jptok.parse_token(toks[j])[0] is not None), '')
            nxt = next((toks[j] for j in range(i + 1, len(toks))
                        if jptok.parse_token(toks[j]) and jptok.parse_token(toks[j])[0] is not None), '')
            g['nbr'][(dur_letter(prev) or '纯', dur_letter(nxt) or '纯')] += 1
            if toks[i + 1] == '-' if i + 1 < len(toks) else False:
                g['next_dash'] += 1

print('=== 含 h 的曲目, 按 status 分组 ===')
for st, g in sorted(groups.items(), key=lambda x: -x[1]['songs']):
    print('\n[%s] 曲数 %d, h token %d 个, 有音高 token %d' % (st, g['songs'], g['h'], g['tokens']))
    print('   紧跟 `-`(简谱二分写法)的 h: %d (%.1f%%)' % (g['next_dash'], 100 * g['next_dash'] / max(1, g['h'])))
    print('   h 的邻居时值(前,后) 前 8 种:', g['nbr'].most_common(8))
    fast = sum(c for (a, b), c in g['nbr'].items() if a in ('d', 's') or b in ('d', 's'))
    print('   邻居里有 d/s(32/16分) 的 h: %d (%.1f%%)' % (fast, 100 * fast / max(1, g['h'])))
    print('   平均拍数/token: h=2 -> %.3f   h=1/64 -> %.3f' % (g['beats_h2'] / max(1, g['tokens']),
                                                              g['beats_h64'] / max(1, g['tokens'])))

print('\n=== 结论提示 ===')
midi = groups.get('midi')
ocr = groups.get('ocr')
if midi and ocr:
    f = lambda g: sum(c for (a, b), c in g['nbr'].items() if a in ('d', 's') or b in ('d', 's')) / max(1, g['h'])
    print('  midi 曲(真值 h=64分)邻居含 d/s 的比例: %.1f%%' % (100 * f(midi)))
    print('  OCR  曲(待定)     邻居含 d/s 的比例: %.1f%%' % (100 * f(ocr)))
    print('  两者接近 -> OCR 的 h 与 midi 同义(=64分音符)')
