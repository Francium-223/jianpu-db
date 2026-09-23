#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""判决实验: 用源谱里**显式写的 `|`**当裁判, 看 h 该按 2 拍还是 1/64 拍算。

思路:
  * 先在 `status=midi` 的曲上跑 —— 它们的 h **确定**是 64 分音符(jianpu-ly 的映射表),
    所以这个裁判本身应该给出"h=1/64 更贴合"。裁判不通过 -> 结论不可信, 直接作废。
  * 再用同一个裁判跑 `status=ocr` 的曲(待定), 看哪一侧更贴合。
  * 判据: 相邻两条显式 `|` 之间的**拍数**分布, 正确的那一侧应集中在拍号(如 4.0)及其倍数附近。
"""
import io
import json
import os
import re
import statistics
import sys
import collections

sys.path.insert(0, 'jianpu2/skills/jianpu-melody-lookup')
import jptok


def beats_between_pipes(body, hval):
    """按给定 h 值, 返回相邻 `|` 之间的拍数列表。"""
    out, acc = [], 0.0
    for t in body.split():
        if t == '|':
            out.append(acc)
            acc = 0.0
            continue
        if t == '-' or (t and t.endswith('-') and t[:-1].strip('cqsdh') == ''):
            acc += 1.0
            continue
        p = jptok.parse_token(t)
        if not p:
            continue
        L = jptok.duration_letter(t)
        if L == 'h':
            v = hval
        else:
            v = jptok.BEAT.get(L, 0.0625) if L else 1.0
        acc += v * (1.5 if t.endswith('.') else 1.0)
    return out


def judge(name, songs, bpb_of):
    """songs: [(label, body)] —— 返回两个假设下的贴合度"""
    res = {}
    for hval, key in ((2.0, 'h=2(二分)'), (0.0625, 'h=1/64(官方)')):
        good = tot = 0
        for label, body, bpb in songs:
            gaps = [g for g in beats_between_pipes(body, hval) if g > 0]
            if len(gaps) < 4:
                continue
            for g in gaps:
                tot += 1
                # 与拍号(或它的倍数)相差 <0.26 拍算"贴合"
                k = round(g / bpb)
                if k >= 1 and abs(g - k * bpb) < 0.26:
                    good += 1
        res[key] = (good, tot)
    print('  [%s] 相邻 `|` 之间的拍数贴合拍号的: ' % name)
    for k, (g, t) in res.items():
        print('     %-14s %5d / %5d = %5.1f%%' % (k, g, t, 100 * g / max(1, t)))
    return res


def main():
    # ① MIDI 组(真值 h=64): 从源文件读(带 `|` 的原文, 不展开也行 —— 用 _expand 更准)
    midi = []
    for fn in sorted(os.listdir('jianpu-db/scores')):
        if not fn.endswith('.txt') or fn.endswith('_expand.txt'):
            continue
        raw = io.open('jianpu-db/scores/' + fn, encoding='utf-8').read()
        if not re.search(r'(?m)^status=midi\s*$', raw) or 'h' not in raw:
            continue
        exp = 'jianpu-db/scores/' + fn[:-4] + '_expand.txt'
        body = io.open(exp, encoding='utf-8').read() if os.path.isfile(exp) else raw
        body = body.split('%---', 1)[-1] if '%---' in body else body
        midi.append((fn, body, jptok.beats_per_bar_from(raw)))
    print('MIDI 组(真值 h=64 分)  含 h 且有 body 的曲: %d' % len(midi))
    judge('MIDI 组 —— 裁判自检(应偏向 h=1/64)', midi, None)

    # ② OCR 组(待定): 用 data.jsonl 的 score(里面保留了显式 `|`)
    ocr = []
    for line in open('jianpu-db/data.jsonl', encoding='utf-8'):
        r = json.loads(line)
        if r.get('status') != 'ocr':
            continue
        sc = r.get('score') or ''
        if 'h' not in sc or '|' not in sc:
            continue
        ocr.append((r['file'][0], sc, float(r.get('beats_per_bar') or 4.0)))
    print('\nOCR 组(待定)  含 h 且含显式 `|` 的曲: %d' % len(ocr))
    judge('OCR 组 —— 判决', ocr, None)

    # ③ 顺带: 不含 h 的 OCR 曲做对照(说明裁判本身是否靠谱)
    ctrl = []
    for line in open('jianpu-db/data.jsonl', encoding='utf-8'):
        r = json.loads(line)
        if r.get('status') != 'ocr':
            continue
        sc = r.get('score') or ''
        if 'h' in sc or '|' not in sc:
            continue
        ctrl.append((r['file'][0], sc, float(r.get('beats_per_bar') or 4.0)))
    print('\n对照组: 不含 h 的 OCR 曲 %d 首' % len(ctrl))
    judge('对照组(不含 h, 两个假设结果应相同)', ctrl, None)


if __name__ == '__main__':
    main()
