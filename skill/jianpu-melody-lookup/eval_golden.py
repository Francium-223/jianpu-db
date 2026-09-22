# -*- coding: utf-8 -*-
"""在"华流金曲清单"上量检索指标 —— 这才是"×首金曲 TopK 准确率"的口径。

做法:
  * 拿 train-work/mandopop_list.txt 的曲名清单(317 首), 在库里找同名歌。
  * 对每首歌: 取它的一份谱截一段片段做查询, **索引里保留全部谱**(含同名歌的其它版本)
    —— 因为我们想知道的是"用户哼一句, 能不能在库里定位到这首歌", 而不是"没有它能不能猜出来"。
  * 报命中率: 片段召回原歌(按其**曲名**判定, 不要求正好是同一份谱)进 Top-1 / Top-3 / Top-5。
  * 同时报"多版本留一"子集(更严: 查询源谱排除, 只能靠别的版本命中)。

用法: py -3.13 eval_golden.py [--list 路径] [--lens 11,15] [--errs 0,1]
"""
import argparse
import json
import os
import random
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lookup import group_of, pitch_and_oct  # noqa: E402

ZW = dict.fromkeys(map(ord, "\u200b-\u200f\u202a-\u202e\u2060\ufeff"), None)


def norm(s):
    s = (s or "").translate(ZW)
    s = re.sub(r"[（(【\[《][^）)】\]》]*[）)】\]》]", "", s)
    s = re.sub(r"(简谱|歌谱|五线谱|正谱|完整版|弹唱|吉他谱|钢琴谱|歌曲类)", "", s)
    return re.sub(r"[\s\-_·、,，。.]+", "", s).casefold()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(HERE, "data.jsonl"))
    ap.add_argument("--list", default=r"D:\Documents_D\jianpu2\train-work\mandopop_list.txt")
    ap.add_argument("--lens", default="11,15")
    ap.add_argument("--errs", default="0")
    ap.add_argument("--per-song", type=int, default=1)
    ap.add_argument("--seed", type=int, default=20260923)
    a = ap.parse_args()
    rnd = random.Random(a.seed)

    rows = [json.loads(l) for l in open(a.data, encoding="utf-8") if l.strip()]
    idx = []
    for r in rows:
        p, _ = pitch_and_oct(r.get("score"))
        if len(p) >= 11:
            idx.append((r, p, np.frombuffer(p.encode(), dtype=np.uint8)))

    want = []
    for ln in open(a.list, encoding="utf-8"):
        s = ln.strip()
        if s and not s.startswith("#"):
            want.append(s)
    wn = {norm(w) for w in want}
    print(f"金曲清单 {len(want)} 首; 库 {len(rows)} 份谱, 其中 >=11 音 {len(idx)} 份")

    # 清单里的每首歌 -> 库里属于它的所有谱。
    # **匹配要双向**: 清单条目常带歌手名(`2002年的第一场雪刀郎`), 库里的曲名没有
    # (`2002年的第一场雪`) -> 单看 "清单 in 库名" 会漏, 必须两边都试。
    # 判定命中时也按**规范化后的字符串互相包含**比, 不要求完全相等。
    def same(a, b):
        return bool(a) and bool(b) and (a == b or (len(a) >= 4 and len(b) >= 4 and (a in b or b in a)))

    hits = {}
    for r, p, ar in idx:
        gn = norm(group_of(r.get("title")))
        for w in wn:
            if same(gn, w):
                hits.setdefault(w, []).append((r, p, ar))
                break
    covered = sorted(hits)
    print(f"清单里能在库中定位到的: {len(covered)}/{len(want)} = {len(covered)/len(want)*100:.1f}%")
    multi = {w: v for w, v in hits.items() if len(v) >= 2}
    print(f"其中在库里有 >=2 个版本的: {len(multi)} 首 (留一口径的分母)")

    for L in [int(x) for x in a.lens.split(",")]:
        for k in [int(x) for x in a.errs.split(",")]:
            t1 = t3 = t5 = n = 0
            lt1 = lt3 = lt5 = ln_ = 0
            for w in covered:
                vers = [v for v in hits[w] if len(v[1]) >= L]
                if not vers:
                    continue
                for _ in range(a.per_song):
                    r0, p0, _a0 = rnd.choice(vers)
                    i0 = rnd.randrange(0, len(p0) - L + 1)
                    frag = list(p0[i0:i0 + L])
                    for _x in range(k):
                        j = rnd.randrange(L)
                        d = int(frag[j])
                        cs = [x for x in (d - 1, d + 1) if 1 <= x <= 7]
                        if cs:
                            frag[j] = str(rnd.choice(cs))
                    qa = np.frombuffer("".join(frag).encode(), dtype=np.uint8)
                    sc = []
                    for r2, p2, ar2 in idx:
                        if len(ar2) < L:
                            continue
                        wnd = np.lib.stride_tricks.sliding_window_view(ar2, L)
                        sc.append((int((wnd != qa).sum(axis=1).min()), norm(group_of(r2.get("title"))), r2 is r0))
                    sc.sort(key=lambda x: x[0])
                    n += 1
                    top1 = sc[0][1]
                    top3 = [x[1] for x in sc[:3]]
                    top5 = [x[1] for x in sc[:5]]
                    if same(top1, w):
                        t1 += 1
                    if any(same(x, w) for x in top3):
                        t3 += 1
                    if any(same(x, w) for x in top5):
                        t5 += 1
                    if len(vers) >= 2:                      # 留一: 排除查询源谱
                        sc2 = [x for x in sc if not x[2]]
                        sc2.sort(key=lambda x: x[0])
                        ln_ += 1
                        if sc2 and same(sc2[0][1], w):
                            lt1 += 1
                        if any(same(x[1], w) for x in sc2[:3]):
                            lt3 += 1
                        if any(same(x[1], w) for x in sc2[:5]):
                            lt5 += 1
            if not n:
                continue
            print(f"L={L:<3} 错音={k}  查询 {n:>4d}  |  **金曲定位**: "
                  f"Top1 {t1/n*100:>5.1f}%  Top3 {t3/n*100:>5.1f}%  Top5 {t5/n*100:>5.1f}%"
                  + (f"  |  多版本留一({ln_} 查询): Top1 {lt1/ln_*100:>5.1f}%  "
                     f"Top3 {lt3/ln_*100:>5.1f}%  Top5 {lt5/ln_*100:>5.1f}%" if ln_ else ""))


if __name__ == "__main__":
    main()
