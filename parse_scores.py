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
	# 用白名单而不是"排除 midi": 以后再加等级(比如两条自动线各自再分档)也不会漏进数据集。
	OK_STATUS = ('ok', 'ocr')
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