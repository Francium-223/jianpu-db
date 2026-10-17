import os as _os, sys as _sys
# 2026-09-24: 这个脚本必须在 jianpu-db 里跑(要读 scores/、tags.json, 写 by_* 与 data.jsonl)。
# 以前从别的目录跑会崩在 `FileNotFoundError: 'tags.json'`, 而且 by_* 还会被拆到一半
# (实测: 从工作区根目录跑 -> 崩溃 + by_* 树半重建)。自己 chdir 过来, 从哪儿跑都对。
_os.chdir(_os.path.dirname(_os.path.abspath(__file__)))
from score import *
# 必须排序: os.listdir 的顺序由文件系统决定, 每次可能不同 -> data.json 的顶层键顺序乱跳,
# 于是 CI 每次 git add -A 都提交一个巨大的"无意义重排"(实测踩过)。
files = sorted(os.listdir('scores'))
files = ['scores/' + i for i in files if re.match(r'^(?!.*(?:_expand|_buf)\.txt$).*\.txt$', i)]
a = []
b = {}
rows = []          # data.jsonl 的行(扁平, 一行一首)
c = [i.name for i in Path('.').iterdir() if i.is_dir() and i.name.startswith('by_')]
for i in c:
	shutil.rmtree(i)
for i in files:
	a.append(Score(i))
for i in a:
	print('Parsing:', i.score)
	i.parse()
	b.update({i.score.split('/')[-1] : i.others})
	# 同一批数据再摆一份扁平的。**白名单**: status 含 ok 或 ocr 的算可用数据。
	#   ok   = 人工校对过                -> 进数据集
	#   ocr  = 由图片机器转写(OCR)来的    -> **也进**(2026-09-23 用户决定:
	#          导入的 OCR 谱必须进 data.jsonl, 否则 data.json 有而 data.jsonl 没有 -> 静默丢数据)
	#   midi = 由 MIDI 硬转过来的(自动)   -> 不进(它是硬转, 不是本仓库要的简谱记录)
	#   converted = 由 **ABC 等记谱格式机械转换**来的(自动) -> **进**(2026-10-04 作者定:
	#           ABC 这类转换与 `midi` 区分开 —— 它带完整音高记录, 且转换器已按本仓库首调口径
	#           (大调 Do-based / 小调 La-based, 主音 `,6`)写出来源与调号)
	#   bare-numbers = 本仓库作者**亲自转写**出来的裸数字谱 -> **进**(2026-10-17 作者定:
	#           "加一个 status 可用的值: bare-numbers"。第一批实测 `scores/th*.txt` 4 首,
	#           transcriber=Francium-223。它跟 ok 一样是人的产出, 只是没走人工校对标记)
	# 用白名单而不是"排除 midi": 以后再加等级(比如两条自动线各自再分档)也不会漏进数据集。
	OK_STATUS = ('ok', 'ocr', 'converted', 'bare-numbers')
	_r = i.to_record()
	# status 的形态由 schema 决定(现在是字符串, 也可能是列表) -> 统一成列表再判断
	_s = _r['status'] if isinstance(_r['status'], list) else [_r['status']]
	if any(_x in OK_STATUS for _x in _s) and _r['score']:
		rows.append(_r)
with open('./data.json', 'w', encoding='utf-8') as f:
	json.dump(b, f, indent=4, ensure_ascii=False)
with open('./data.jsonl', 'w', encoding='utf-8') as f:
	for _r in rows:
		f.write(json.dumps(_r, ensure_ascii=False) + '\n')
print(f'data.json  {len(b)} 首  -> ./data.json')
print(f'data.jsonl {len(rows)} 首  -> ./data.jsonl  (待整理已跳过 {len(b) - len(rows)})')
# README 顶上那六颗徽章跟着这次产物刷新(2026-10-17 作者: "这个应该 parse 的时候更新一下")。
# 语料太小(测试、toy 目录)不动, 找不到 README 也不动 —— 都交给 readme_badges 自己判。
try:
	import readme_badges
	_got = readme_badges.refresh(rows)
	if _got:
		print('README 徽章 %s  (旧行 %d 字符)' % ('已刷新' if _got[2] else '已是最新', len(_got[0])))
except Exception as _e:
	print('README 徽章未刷新:', _e)