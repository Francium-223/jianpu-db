"""README 顶上的六颗徽章：数字由本次 parse 的产物现算，不再手写。

以前这行是死的 —— 徽章 URL 里编码着数字（`曲谱-11%2C381%20%E9%A6%96`），
只能由生成数据的那一步顺手改，而生成数据的那一步一直没管它。
2026-10-17 作者发现 GitHub 上还挂着 11,381 首，data.jsonl 其实已经 44,089 行，
要求"这个应该 parse 的时候更新一下"。

口径：
  曲谱   = data.jsonl 的行数
  音符   = Σ n_notes（不含时值标记）
  小节线 = Σ len(bars)（只数显式小节线）
  出处站 = 有 ≥SITE_MIN 首的来源数（零星来源不撑门面）
  人工校对 = status=ok
  机器转写 = 其余的（ocr / converted / bare-numbers 都算"还没人工校对"）
"""

import os
import re
import urllib.parse

BADGE_LINE_RE = re.compile(r'^\[!\[曲谱\]\(https://img\.shields\.io/badge/')
SITE_MIN = 10       # 少于这么多首的来源不算"出处站"
MIN_ROWS = 10000    # 小语料（测试、toy 目录）不动 README


def _badge(label, msg, color):
	q = urllib.parse.quote
	# 外面那层是链接, 点徽章回站点首页 —— README 一直是这么写的, 保持原样。
	return '[![%s](https://img.shields.io/badge/%s-%s-%s)](https://jianpu-db.org/)' % (
		label, q(label, safe=''), q(msg, safe=''), color)


def stats(rows):
	"""把 data.jsonl 的行压成六个数字。"""
	n = len(rows)
	notes = bars = 0
	sites = {}
	st = {}
	for r in rows:
		notes += int(r.get('n_notes') or 0)
		b = r.get('bars') or []
		bars += len(b) if isinstance(b, list) else 0
		for s in (r.get('source') or []):
			site = str(s).rsplit('-', 1)[0]
			sites[site] = sites.get(site, 0) + 1
		s_ = r.get('status')
		for x in (s_ if isinstance(s_, list) else [s_]):
			st[x] = st.get(x, 0) + 1
	ok = st.get('ok', 0)
	return {'songs': n, 'notes': notes, 'bars': bars,
	        'sites': sum(1 for v in sites.values() if v >= SITE_MIN),
	        'ok': ok, 'auto': n - ok}


def line(d):
	return ' '.join([
		_badge('曲谱', '%s 首' % format(d['songs'], ','), '0b62c4'),
		_badge('音符', format(d['notes'], ','), '0b62c4'),
		_badge('小节线', format(d['bars'], ','), '0b62c4'),
		_badge('出处站', '%d 个' % d['sites'], '0b62c4'),
		_badge('人工校对', '%s 首' % format(d['ok'], ','), 'c4770b'),
		_badge('机器转写', '%s 首' % format(d['auto'], ','), 'c4770b'),
	])


def refresh(rows, path='README.md', dry_run=False):
	"""把 README 里那行徽章换成现算的。返回 (旧行, 新行, 有没有改动) 或 None。

	找不到徽章行、语料太小、README 不存在时返回 None —— 调用方不必区分这些情况。
	"""
	if len(rows) < MIN_ROWS or not os.path.exists(path):
		return None
	new = line(stats(rows))
	with open(path, encoding='utf-8') as f:
		lines = f.read().split('\n')
	for i, l in enumerate(lines):
		if not BADGE_LINE_RE.match(l):
			continue
		old = l
		if old == new:
			return (old, new, False)
		if not dry_run:
			lines[i] = new
			with open(path, 'w', encoding='utf-8', newline='\n') as f:
				f.write('\n'.join(lines))
		return (old, new, True)
	return None
