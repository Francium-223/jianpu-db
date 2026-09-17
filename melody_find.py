#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旋律反查 —— 只输数字，就能在 jianpu-db 里找到是哪首歌。

用法（在本目录下执行）:
    python3 melody_find.py 33565653253
    python3 melody_find.py "3 3 5 6 | 5 6 5 3 2 5 3"     # 空格/竖线/汉字都会自动忽略
    python3 melody_find.py 33575653253 --fuzzy 2          # 容忍 2 处不同
    python3 melody_find.py 33565653253 --ok-only          # 只看已校对(status=ok)的
    python3 melody_find.py 33565653253 --top 20

设计要点
--------
1. **只输数字**：用户不需要懂 jianpu-ly（不用写 q/时值/八度/附点）。
   简谱是首调记法（1 永远是该调的 do），所以数字串天然与调无关 —— 换调唱数字不变。
2. **模糊匹配**：记谱/转写都会有错，整串精确相等会全丢。容忍 k 处不同并按错音扣分。
3. **段落加权**：subtitle= 的段落名带权重 —— 副歌(chorus)是"记得住的那句"，
   匹配到副歌比匹配到前奏更该靠前。
4. **校对状态加权**：status=ok（已校对）比 status=draft（未校对）更可信。
5. **记谱规则**（会被规范化掉，不干扰匹配）：
   * `3[ ... ]` 三连音标记 —— 那个 3 不是音符
   * `1 ~ 1` 同数字用 ~ 连接 = 一个音（连音线）
   * `( 1 2 )` 不同数字用括号 = 圆滑线（两个音都在）
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- token 规范化
STRUCT_CHARS = "[](){}~|"
_TUPLET = re.compile(r"^([0-9])\s*\[$")
# 时值字母: q=八分 s=十六分 d=三十二 h=六十四 **c=四分**(jianpu-ly 的 KeepLength 写法,
# 如 `6c.`) —— 漏了 c 会把 `6c.` 整块丢掉, 数字串错位(实测 `3 3 5 6c. 5s 6 5q ...`
# 被解析成 `335565...`, 少了个 6, 检索直接失配)。
_DUR = "qsdhc"
_NOTE = re.compile(r"^[,']*[" + _DUR + r"#b]*[,']*[1-7x0-][.,'" + _DUR + r"#b-]*$")


def is_marker(tok):
    return bool(tok) and all(c in STRUCT_CHARS for c in tok)


def is_tuplet_marker(tok):
    """`3[` 是三连音标记, 数字不是音符。"""
    return bool(_TUPLET.match(tok.replace(" ", "")))


def normalize_tokens(toks, merge_ties=True):
    """去掉结构符号；merge_ties 时把 `X ~ X`(同音高被连音线连接)合并成一个音。"""
    out, pending = [], False
    for t in toks:
        if is_tuplet_marker(t):
            continue
        if is_marker(t):
            if "~" in t:
                pending = True
            continue
        out.append(t)
        if pending and merge_ties and len(out) >= 2 and _pitch(out[-1]) == _pitch(out[-2]):
            out.pop()
        pending = False
    return out


def _pitch(tok):
    """音高(数字+八度) —— 判连音线两端是否同音用。"""
    t = re.sub(r"^[" + _DUR + r"]+", "", tok)        # 去掉前置时值
    t = re.sub(r"[" + _DUR + r"]+$", "", t)          # 去掉后置时值(如 6c)
    m = re.match(r"^([,']*)([1-7])", t)
    return (m.group(2), m.group(1)) if m else (tok, "")


# ---------------------------------------------------------------- 段落 / 状态
SECTION_W = {
    "chorus": 1.60, "refrain": 1.60,          # 副歌: 最可能是用户哼的那句
    "verse": 1.25,
    "pre-chorus": 1.10, "prechorus": 1.10, "bridge": 1.10, "interlude": 1.10,
    "score": 1.00,
    "intro": 0.80, "outro": 0.80, "layer": 0.80, "crazy-piano": 0.80,
}
SECTION_CN = {"chorus": "副歌", "verse": "主歌", "intro": "前奏", "outro": "尾奏",
              "pre-chorus": "预副歌", "bridge": "桥段", "interlude": "间奏",
              "layer": "叠加层", "crazy-piano": "钢琴华彩", "score": "整曲"}
STATUS_W = {"ok": 1.30, "draft": 0.75}
STATUS_CN = {"ok": "已校对", "draft": "未校对"}


def section_weight(name):
    if not name:
        return 1.0
    parts = [p.strip().lower() for p in re.split(r"[,/|+]", name) if p.strip()]
    return max(SECTION_W.get(p, 1.0) for p in parts) if parts else 1.0


def section_label(name):
    return SECTION_CN.get((name or "").strip().lower(), name or "整曲")


def meta_of(path):
    """读 title / alias / status。"""
    title = alias = status = ""
    try:
        for l in io.open(path, encoding="utf-8", errors="replace"):
            s = l.strip()
            if not title:
                m = re.match(r"^title\s*=\s*(.+)$", s, re.I)
                if m:
                    title = m.group(1).strip()
            if not alias:
                m = re.match(r"^alias\s*=\s*(.+)$", s, re.I)
                if m:
                    alias = m.group(1).strip()
            if not status:
                m = re.match(r"^status\s*=\s*(\S+)", s, re.I)
                if m:
                    status = m.group(1).strip().lower()
            if title and alias and status:
                break
    except Exception:
        pass
    return title, alias, status


def sections_of(path):
    """返回 [(段落名, 数字串)]，已经过规范化（三连音标记剔除、连音线合并）。"""
    try:
        txt = io.open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return []
    lines = [l.strip() for l in txt.splitlines()]
    start = 0
    for i, l in enumerate(lines):
        if l.lower().startswith("%--") or l.startswith("%---"):
            start = i + 1
            break
    secs, buf, cur = [], [], "score"

    def flush():
        if not buf:
            return
        norm = normalize_tokens(buf, merge_ties=True)
        digs = []
        for t in norm:
            m = re.match(r"^[,']*[" + _DUR + r"]*[,']*([1-7])", t)
            if m:
                digs.append(m.group(1))
        secs.append((cur, "".join(digs)))

    for l in lines[start:]:
        if not l:
            continue
        m = re.match(r"^subtitle\s*=\s*(.*)$", l, re.I)
        if m:
            flush()
            buf, cur = [], (m.group(1).strip() or "score")
            continue
        if l.startswith("%"):
            continue
        for t in l.split():
            if _NOTE.match(t) or t == "-" or is_marker(t) or is_tuplet_marker(t):
                buf.append(t)
    flush()
    return secs


def best_match(q, text, fuzzy):
    """在 text 里找与 q 最接近的等长窗口。返回 (不同数, 起点, 匹配段) 或 None。"""
    n, m = len(q), len(text)
    if m < n:
        return None
    pos = text.find(q)
    if pos >= 0:
        return (0, pos, q)
    if fuzzy <= 0:
        return None
    best = None
    for i in range(m - n + 1):
        diff = 0
        for a, b in zip(q, text[i:i + n]):
            if a != b:
                diff += 1
                if diff > fuzzy:
                    break
        if diff <= fuzzy and (best is None or diff < best[0]):
            best = (diff, i, text[i:i + n])
            if diff == 0:
                break
    return best


def parse_args(argv):
    """位置参数(查询)与 --flag value 分开 —— 不能简单滤掉 -- 开头, 否则 --top 12 的 12 会被当查询。"""
    VALUE_FLAGS = {"--fuzzy", "--top", "--min"}
    pos, opts, i = [], {}, 0
    while i < len(argv):
        a = argv[i]
        if a in VALUE_FLAGS:
            opts[a] = argv[i + 1] if i + 1 < len(argv) else ""
            i += 2
        elif a.startswith("--"):
            opts[a] = True
            i += 1
        else:
            pos.append(a)
            i += 1
    return pos, opts


def main():
    pos, opts = parse_args(sys.argv[1:])
    if not pos:
        print(__doc__)
        return
    q = re.sub(r"[^1-7]", "", " ".join(pos))
    if len(q) < 3:
        print("查询太短(至少 3 个音), 容易匹配到一大堆")
        return
    fuzzy = int(opts.get("--fuzzy", 1))
    top = int(opts.get("--top", 15))
    ok_only = "--ok-only" in opts
    src = os.path.join(HERE, "scores")
    if not os.path.isdir(src):
        print(f"找不到 {src} —— 请在 jianpu-db 目录下运行")
        return

    print(f"查询: {q}  ({len(q)} 音)   模糊容差 {fuzzy} 处"
          + ("   只看已校对" if ok_only else ""))
    files = [f for f in glob.glob(os.path.join(src, "*.txt"))
             if not f.endswith("_expand.txt")]
    rows = []
    for f in files:
        title, alias, status = meta_of(f)
        if ok_only and status != "ok":
            continue
        disp = title or os.path.basename(f)[:-4]
        if alias and alias not in disp:
            disp = f"{disp}（{alias}）"
        for sec, digits in sections_of(f):
            mt = best_match(q, digits, fuzzy)
            if not mt:
                continue
            diff, p, _seg = mt
            sw = section_weight(sec)
            stw = STATUS_W.get(status, 1.0)
            cover = len(q) / max(len(digits), 1)
            score = len(q) * sw * stw * (0.5 + 0.5 * min(cover * 20, 1)) - diff * len(q) * 0.25
            rows.append((score, disp, sec, diff, p, digits, sw, stw, status))
    # 同一首歌(同名同段落同错数)去重, 留分高的
    seen = {}
    for r in rows:
        key = (r[1], r[2], r[3])
        if key not in seen or r[0] > seen[key][0]:
            seen[key] = r
    rows = sorted(seen.values(), key=lambda x: -x[0])

    print(f"\n命中 {len(rows)} 处" + (f" (显示前 {top})" if len(rows) > top else ""))
    print(f"{'得分':>6}  {'段落':<8}{'权':>4} {'状态':<7}{'错':>3}  {'曲名'}")
    print("-" * 92)
    for score, disp, sec, diff, p, digits, sw, stw, status in rows[:top]:
        st = STATUS_CN.get(status, status or "无")
        print(f"{score:6.1f}  {section_label(sec):<8}{sw:4.1f} {st:<7}{diff:3d}  {disp[:44]}")
        lo, hi = max(0, p - 5), min(len(digits), p + len(q) + 5)
        ctx = digits[lo:p] + "【" + digits[p:p + len(q)] + "】" + digits[p + len(q):hi]
        print(f"{'':6}  └ 第{p}音起  …{ctx}…")
    if not rows:
        print("   (无 —— 加大 --fuzzy, 或去掉 --ok-only)")


if __name__ == "__main__":
    main()
