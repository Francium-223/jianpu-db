import sys
import json
import re
import os
import shutil
import warnings
import schema
from pathlib import Path
# 简谱 token / 时值 / 小节线恢复的**唯一实现**(jptok.py)。它住在 skill 目录里,
# 于是这里显式加路径; 加不到**默认直接报错**(见下面), 不再静默换口径。
_JTOK_DIR = os.environ.get("JIANPU_JTOK") or os.path.join(
	os.path.dirname(os.path.abspath(__file__)), "..", "jianpu2", "skills", "jianpu-melody-lookup")
if os.path.isdir(_JTOK_DIR) and _JTOK_DIR not in sys.path:
	sys.path.insert(0, _JTOK_DIR)
try:
	import jptok
except ImportError:                            # pragma: no cover - 只在独立 clone 时走
	# ⚠ 2026-09-24: 这里**不再静默兜底**。兜底是"第二份口径", 两份一起漂过一次(36 首受损),
	#   而静默降级 = 整个 data.jsonl 可能按另一套 token 规则重建还没人发现。
	#   jptok.py 是硬依赖(与 export_hf.py 一个态度); 确实要在没有 jianpu2 的环境跑,
	#   显式设 JIANPU_ALLOW_FALLBACK_JTOK=1 才用内置兜底, 并在报告里写明。
	if os.environ.get("JIANPU_ALLOW_FALLBACK_JTOK") != "1":
		raise SystemExit(
			f"找不到 jptok.py(唯一实现): {_JTOK_DIR}\n"
			f"  它是硬依赖 —— 少了它 data.jsonl 会换一套 token 口径重建(丢音/小节漂)。\n"
			f"  修法: 设 JIANPU_JTOK=<jianpu2/skills/jianpu-melody-lookup 绝对路径>;\n"
			f"  或者(不推荐)设 JIANPU_ALLOW_FALLBACK_JTOK=1 用 score.py 里的内置兜底。")
	class _FallbackJptok:
		"""jptok 找不到时的最小兜底: 保证 data.jsonl 仍产出 bars。与 jptok 同口径。

		⚠ 这是**第二份**口径(唯一一份在 skill 目录的 jptok.py)。2026-09-23 它俩一起漂了:
		  正则只认前缀时值, 后缀形(`6c.`/`5s`/`3q`)被静默丢掉, 36 首受损。
		  改 jptok.py 时**必须同步这里**(或干脆删掉这段、让 jptok 成为硬依赖)。
		"""
		BEAT = {"h": 0.0625, "c": 1.0, "": 1.0, "q": 0.5, "s": 0.25, "d": 0.125}  # h=64分音符, 见 jptok.py 里的定案说明
		_TOK = re.compile(
			r"^(?P<pre>[cqsdh]*)(?P<oct1>[,']*)(?P<acc>[#b♯♭]?)(?P<dig>[1-7x0])"
			r"(?P<oct2>[,']*)(?P<acc2>[#b♯♭]?)(?P<post>[cqsdh]*)(?P<dot>[.]*)(?P<mark>[\[\]]?)$")

		@classmethod
		def parse_token(cls, t):
			m = cls._TOK.match(t or "")
			if not m:
				return None
			g = m.groupdict()
			acc, acc2 = g["acc"], g["acc2"]
			a = 1 if (acc in ("#", "♯") or acc2 in ("#", "♯")) else (-1 if (acc in ("b", "♭") or acc2 in ("b", "♭")) else 0)
			off = (g["oct1"] + g["oct2"]).count(",") - (g["oct1"] + g["oct2"]).count("'")
			return (None, a, off) if g["dig"] in "0x" else (int(g["dig"]), a, off)

		@classmethod
		def is_note(cls, t):
			return cls.parse_token(t) is not None

		@classmethod
		def seq(cls, score):
			"""整份谱 -> [解析结果], 只保留**有音高**的 token(与 jptok.seq 同口径)。

			2026-09-24 补: 兜底类原来缺这个方法, 于是 CI(GitHub runner 只 checkout 了本仓库,
			没有兄弟目录 jianpu2/)走到 export_hf.py 的 `jptok.seq(...)` 就
			`AttributeError: type object '_FallbackJptok' has no attribute 'seq'` ✗。
			它是直接建在 parse_token 上的一行逻辑, 不是第二套正则。
			`check_jptok_parity.py` 现在也逐首比 seq, 专门盯这类"缺方法/口径漂"。
			"""
			out = []
			for t in (score or "").split():
				q = cls.parse_token(t)
				if q and q[0] is not None:
					out.append(q)
			return out

		@classmethod
		def duration_letter(cls, tok):
			t = tok or ""
			m = re.match(r"^([cqsdh]+)", t)
			if m:
				return m.group(1)
			m = re.search(r"([cqsdh]+)[.]*[\[\]]?$", t)
			return m.group(1) if m else ""

		@classmethod
		def beat(cls, tok):
			v = cls.BEAT.get(cls.duration_letter(tok), 0.0625)
			return v * 1.5 if (tok or "").endswith(".") else v

		@staticmethod
		def beats_per_bar_from(text, default=4.0):
			m = re.search(r"(?m)^\s*(\d+)\s*/\s*(\d+)\s*$", text or "")
			if not m:
				return default
			try:
				return int(m.group(1)) * 4.0 / int(m.group(2))
			except ZeroDivisionError:
				return default

		@classmethod
		def recover_bars(cls, sections, beats_per_bar, keep_explicit=True):
			# 与 jptok.recover_bars 同口径: **休止/念白也占拍**(不记时会让小节线整体前漂)
			bars, n, acc = [], 0, 0.0
			for sec in sections or []:
				for t in (sec.get("score") or "").split():
					if t == "|":
						if keep_explicit:
							bars.append(n)
						acc = 0.0
						continue
					if t == "-" or re.match(r"^[cqsdh]+-$", t or ""):
						acc += 1.0
						continue
					p = cls.parse_token(t)
					if not p:
						continue
					if p[0] is not None:
						n += 1
					acc += cls.beat(t)
					if acc >= beats_per_bar - 1e-9:
						bars.append(n)
						acc = 0.0
			return bars

	jptok = _FallbackJptok
	warnings.warn("jptok 未找到(用内置兜底): " + _JTOK_DIR, RuntimeWarning)
# 标签图的机械(safe_add/maybe_add/别名比较/goto_node/load_tag_rules)与
# "usertag -> tag/tagroute"的推导**已迁到 schema.py**(单一实现)。
# 这里只取别名, 免得出现第二份会漂移的实现。
imply, equal = schema.imply, schema.equal
safe_add = schema.safe_add
safe_minus = schema.safe_minus
maybe_add = schema.maybe_add
class NoScoreError(Exception):
	pass
class NotTitleError(Exception):
	pass
class BadBufError(Exception):
	pass
def _rel(target, link_path):
	"""链接目标: 相对链接所在目录, 统一用正斜杠。

	Windows 的 os.sep 是反斜杠、Linux 是正斜杠 —— 不统一的话, 本地生成一次、
	CI(Linux) 再生一次, 同一批链接的文本内容就不同, 每次提交都在改它们。
	"""
	return os.path.relpath(target, start=os.path.dirname(link_path)).replace(os.sep, '/')


def get_meta_lines(s):
	d = []
	for i in s:
		d.append(i)
		if i.replace(' ', '').startswith('%--'):
			return d
	return d
def expand_keep_length(text):
	"""把 KeepLength 的"省略时值"补全成显式时值(供计算机直接读取)。

	jianpu-ly 规则(见 jianpu-ly.py 的 addNote: if nBeams==None: nBeams = self.lastNBeams):
	  出现 KeepLength 后, 凡是"没写时值"的音符沿用上一个音符的时值, 直到出现新的时值标记。
	时值字母: c=四分 q=八分 s=十六分 d=三十二分 h=二分 (可前可后, 这里统一补到前面)

	例: KeepLength s1 1 1 1 c1  ->  s1 s1 s1 s1 c1
	"""
	VAL = 'cqsdh'
	out_lines = []
	cur_val = ''          # 当前生效的时值
	keep = False          # KeepLength 是否生效
	# ⚠ 只处理**曲谱正文**(第一条 `%--` 之后)。输入是 `_buf.txt` 的内容 = 元数据 + 正文,
	#   元数据行里也可能有"以时值字母结尾"的词(todo=add tags / title=Twins …),
	#   一旦被当成时值搬前面就会写成 `dtodo=ad stag`(实测: 1678 个 _expand.txt 被写坏)。
	#   没有 `%--` 时(独立的正文片段)按全文处理。
	has_marker = any(l.replace(' ', '').startswith('%--') for l in text.splitlines())
	in_body = not has_marker
	for line in text.splitlines():
		s = line.strip()
		if s.replace(' ', '').startswith('%--'):
			in_body = True
			out_lines.append(line)
			continue
		if not in_body:
			out_lines.append(line)           # 元数据区原样保留
			continue
		if s == 'KeepLength':
			keep = True
			out_lines.append(line)
			continue
		# 作用域: KeepLength 到换 subtitle(或 NextScore)即失效 —— 必须重置状态
		if s.startswith('subtitle=') or s.lower() == 'nextscore':
			keep = False
			cur_val = ''
			out_lines.append(line)
			continue
		if not s or s.startswith('%'):
			out_lines.append(line)
			continue
		toks = []
		for tok in s.split():
			# 第二道防护: **只对音符/记号做时值处理**。不是音符的 token(`todo=add`、垃圾)
			# 原样放回去 —— 光看"结尾字母像不像 cqsdh"会误伤普通单词。
			if not (jptok.is_note(tok) or tok in ('-', '|', '~')):
				toks.append(tok)
				continue
			# 取时值: 可能前置(q1 / q1' / s,6) 或后置(1q / ,6s / 3c.)
			m_pre = re.match(r'^([cqsdh])(.*)$', tok)
			m_post = re.match(r'^(.*?)([cqsdh])([.]*)$', tok)
			if m_pre and re.match(r"^[,']*[0-9x]", m_pre.group(2)):
				cur_val = m_pre.group(1)
				toks.append(tok)                 # 已经是"时值在前", 原样
			elif m_post:
				cur_val = m_post.group(2)
				# **后缀 -> 前缀**(兑现本函数 docstring 的"统一补到前面"):
				#   `6c.` -> `c6.`    `,6q` -> `q,6`    `'1q` -> `q'1`
				# 以前这里是 `toks.append(tok)` 原样保留 —— 后缀 token 于是流进 data.jsonl /
				# _expand.txt, 而只认前缀的解析器把它们整段丢掉: 36 首手工录入谱索引里
				# 少了 40% 的音(最多一首丢 91%), th10_06 第 1 小节的旋律因此被读错。
				toks.append(cur_val + m_post.group(1) + m_post.group(3))
			elif keep and cur_val:
				# 无时值: KeepLength 生效时补上当前时值, 否则按四分音(不加前缀)
				toks.append(cur_val + tok)
			else:
				toks.append(tok)
		out_lines.append(' '.join(toks))
	return '\n'.join(out_lines)


def replacer(match):
	n_str = match.group(1)
	xxx = match.group(2).strip()
	a_content = match.group(3)
	if a_content is not None:
		items = [item.strip() for item in a_content.split("|")]
		if len(items) >= 2:
			if n_str and int(n_str) != len(items):
				return match.group(0)
			return "\n".join(f"{xxx} {item}" for item in items)
		return match.group(0)
	else:
		repeat_count = int(n_str) if n_str else 2
		return "\n".join([xxx] * repeat_count)
class Score():
	def __init__(self, score):
		self.score = score
		self.prefix = ('.').join(self.score.split('.')[:-1])
		self.tag_route = []
		self.all_tag_route = []
		self.nottag_route = []
		self.tag = []
		self.usertag = []
		self.origtag = []
		self.nottag = []
		self.orignottag = []
		self.title = ''
		self.raw = ''
		self.raw2 = ''
		self.raw_expanded = ''
		self.others = {'tag': [], 'usertag': [], 'tagroute': []}
		self.comments = []
	def prioritize_title_and_tag(self):
		b = {}
		b['file'] = self.others['file']
		b['title'] = self.others['title']
		b['usertag'] = self.others['usertag']
		b['tagroute'] = self.others['tagroute']
		b['tag'] = self.others['tag']
		for i in self.others.keys():
			if not i in ['file', 'title', 'tag', 'usertag', 'tagroute']:
				b[i] = self.others[i]
		self.others = b
	def to_record(self):
		"""扁平记录: 一行一首, 给 data.jsonl 用(便于 datasets.load_dataset 直接读)。

		与 data.json 是同一批数据的两种摆法 —— 由 parse_scores.py 一次跑出来, 不需要另开脚本。
		字段形态与 data.json 一致: 除 title 是字符串外, 其余都是列表。
		"""
		sections, cur, cur_sub = [], [], ''
		for line in self.raw_expanded.splitlines():
			s = line.strip()
			if s.lower().startswith('nextscore'):
				if cur:
					sections.append({'subtitle': cur_sub, 'score': ' '.join(cur)})
				cur, cur_sub = [], ''
				continue
			if s.replace(' ', '').lower().startswith('%end'):
				break
			if s.lower().startswith('subtitle='):
				cur_sub = s.split('=', 1)[1].strip()
				continue
			# 拍号行(如 4/4)不是音符 —— 不排除的话 "4/4" 会被当成音符混进 score
			if re.match(r'^\d+\s*/\s*\d+$', s):
				continue
			if s.startswith('%') or not s:
				continue
			cur += [t for t in s.split()
					# **口径只有一份**: 判音符一律走 jptok.is_note(整体匹配, 时值前后都认)。
					# 这里以前自带一份"前缀部分匹配"的正则 `^[,']*[qsdh]*[,']*[#b]?[1-7x0]|[#b][1-7]`:
					# 它靠部分匹配把 `6c.` 当音收下(所以 n_notes=383), 而真正的 token 解析器
					# 只认前缀 —— 同一份数据两个口径, 正是"带 # 的音整段消失"那次的老坑。
					if jptok.is_note(t) or t in ('-', '|', '~')
					or re.match(r"^[cqsdh]+[-~]$", t)      # `c-`/`q-`: KeepLength 补时值的延长记号
					# 调号(`1=C`/`1=Bb`)不是音符, 但它**是** score 里唯一残留的调性信息 -> 原样保留
					or re.match(r"^[1-7]\s*=\s*[A-Ga-g][#b♯♭]?$", t)]
		if cur:
			sections.append({'subtitle': cur_sub, 'score': ' '.join(cur)})
		full = ' | '.join(x['score'] for x in sections if x['score'])
		# ---------------- 小节线恢复 ----------------
		# 用户口径(2026-09-23): 「进 data.jsonl 的所有小节线必须是显式的。」
		# 现实: 全库只有 2.5%(197/7884)的谱真写了 `|`, 而且 expand 还会把 R{..} 里的吃掉
		# —— 所以不能靠"保留", 必须按**拍号 + 时值**把小节算出来。
		# **实现只有一份**: jptok.beat / beats_per_bar_from / recover_bars
		# (拍值表一度在这里又写了一份, 成了第五个"复制口径"; 已并回去)。
		_beat_n = jptok.beats_per_bar_from(
			self.raw2 or "\n".join(x.rstrip("\n") for x in (self.raw or [])))
		bars = jptok.recover_bars(sections, _beat_n)
		n_notes = sum(1 for t in full.split() if jptok.is_note(t))
		# 各字段的形态由 schema 决定(字符串或列表) -> 原样传出去, 不在这里强转
		return {
			'file': [self.score.split('/')[-1]],
			'status': self.others.get('status', ''),
			'title': self.title,                      # ← 单值字符串(schema 里由 return_itself 产出)
			# 字段名统一用**单数**, 与 data.json 完全一致(tag/usertag, 不是 tags/usertags)
			'tag': self.others.get('tag', []),
			'usertag': self.others.get('usertag', []),
			# source= 是**逐首溯源**(站点-站内id), 之前只有曲谱文件里有、扁平记录里没带出来,
			# 于是 data.jsonl 里这一列是空的 —— 数据集没法回答"这首哪来的" ✗
			'source': self.others.get('source', []),
			# MBID 是**曲目的实体级身份**(MusicBrainz)。库里已有 1034 份写了它,
			# 但这里同样曾经漏带 -> data.jsonl 里 0 条能看见, 下游无法用"同 MBID = 同一首"
			# 替代脆弱的曲名分组。字段名按仓库既有写法保持大写 MBID。
			'MBID': self.others.get('MBID', ''),
			# **收录页**(用户口径 2026-09-23): 每首歌在自己那一页的确切 URL(可多个)。
			# 搜索页不算收录页 —— 前端可以现拼搜索, 但那个不进语料。
			# ⚠ 这个字段是"人工补"的: 页面上的"粘贴链接→保存"与 tools/add_link.py 都写它。
			'link': self.others.get('link', []),
			'alias': self.others.get('alias', []),
			# 歌手(独立字段, 2026-09-24): 以前只混在 usertag 里, 下游没法直接问"这首谁唱的"。
			'artist': self.others.get('artist', []),
			'transcriber': self.others.get('transcriber', []),
			'sections': sections,
			'score': full,
			# **显式小节线**(用户口径: 进 data.jsonl 的所有小节线必须是显式的)。
			# 语义: 一串 0-based 音符下标, 表示"第 i 个音符之前有一条小节线"。
			# 由拍号 + 时值确定性算出(见上面算法); 源文件里已有的 `|` 当强小节线。
			'bars': bars,
			'beats_per_bar': _beat_n,
			'n_notes': n_notes,
		}
	def read(self):
		try:
			with open(self.score, 'r', encoding='utf-8') as f:
				self.raw = f.readlines()
				self.raw2 = f.read()
			# 阶段 1: 只收集**原文**(字段名 -> 按出现顺序的原文列表), 不在这里解析。
			#   为什么分两阶段: 属性的生成有依赖(tag/tagroute 要吃 usertag 的**聚合结果**),
			#   边读边算会让"多行 usertag"在中途被重算; 谁先谁后交给 schema.order()。
			raws = {}
			for i in get_meta_lines(self.raw):
				i = i.rstrip('\n')
				if i.replace(' ', '').startswith('%--') or i.replace(' ', '').startswith('tag=') or i.replace(' ', '').startswith('tagroute='):
					continue
				if i.replace(' ', '').lower().startswith('file='):
					# file 由文件名派生(write_buf 里写进 JSON), 不是源字段 ——
					# 曲谱文件里若残留这一行(历史误写)要忽略, 否则会被读回来又写回去。
					continue
				if '=' in i:
					k, raw = i.split('=', 1)
					raws.setdefault(k.strip(' '), []).append(raw.strip(' '))
					continue
				if i == '%' + self.score.split('/')[-1]:
					continue
				if i.startswith('%'):
					self.comments.append(i.rstrip('\n'))
					continue
				# 裸行 = 旧格式的 usertag(没有 `=`); 实测 0 命中, 保留兼容。
				raws.setdefault('usertag', []).append(i.strip())
			# 阶段 2a: 一阶字段(deps 为空)按**文件出现顺序**逐条原文解析后累加
			#   —— list 字段去重保序、str 字段后者覆盖前者(与搬迁前一致)。
			#   叶子之间没有依赖, 文件顺序本身就是一个合法的拓扑序; 保持它还让
			#   data.json 的键顺序与搬迁前逐字节一致。
			for i in raws:
				_attr = schema.schema.get(i)
				if _attr is not None and _attr.deps:
					continue                      # 衍生字段留到 2b
				_fn = _attr.fn if _attr is not None else schema.default_parse
				for raw in raws[i]:
					v = _fn(raw)
					if isinstance(v, list) and isinstance(self.others.get(i), list):
						# 多值字段: 同一个字段可以写多行, 累加去重
						self.others[i] = safe_add(self.others[i], v)
					else:
						self.others[i] = v
			# 阶段 2b: 衍生字段按**依赖拓扑序**执行(每个吃 Score 对象, 整份谱只跑一次)
			for i in schema.order():
				_attr = schema.schema[i]
				if _attr.deps:
					self.others[i] = _attr.fn(self)
			# title 现在也由 schema 解析进 others(字符串) -> 同步到 self.title(文件命名要用)
			if isinstance(self.others.get('title'), str):
				self.title = self.others['title']
		except NotTitleError:
			print(f'Error: no title!')
			print(f'Try adding \'title=(your preferred title)\' to {self.score}.')
			raise
		except FileNotFoundError:
			print(f'Error: file \'{self.score}\' not found!')
			raise NoScoreError
	def derive_others(self):
		"""衍生字段(tag/tagroute)已在 read() 里按 schema.order() 生成完毕。

		这里保留一个显式收尾点: 只做**依赖表自检** —— 成环会让 schema.order() 自己 Warning
		(CI 里可以用 schema.order(strict=True) 把它升级成错误)。
		"""
		schema.order()
	def write_buf(self):
		with open(('.').join(self.score.split('.')[:-1]) + '_buf.txt', 'w', encoding='utf-8') as f:
			print('%' + self.score.split('/')[-1], file=f)
			for i in self.comments:
				print(i.rstrip('\n'), file=f)
			# title 由 schema 解析成字符串、已进 others; 这里先写它(保持原来的字段位置),
			# 循环里跳过它, 免得写两遍。值的形态由 schema 决定: 字符串(title/MBID)或列表(其余)。
			print('title=' + self.title, file=f)
			for i in self.others.keys():
				if i == 'title':
					continue
				_v = self.others[i]
				# 字符串字段直接写; 列表字段用逗号连接(与读入时的切分规则对称)
				print(i + '=' + ((',').join(str(x) for x in _v)
								 if isinstance(_v, list) else str(_v)), file=f)
			# file 只给 JSON 用(prioritize_title_and_tag), **不写回曲谱文件** ——
			# 否则每份曲谱会多出一行 file=xxx.txt(实测踩过)。
			self.others['title'] = self.title
			self.others['file'] = [self.score.split('/')[-1]]
			d = False
			for i in self.raw:
				if i.replace(' ', '').startswith('%--'):
					d = True
				if d:
					print(i.rstrip('\n'), file=f)
			if not ('').join(self.raw).replace('\n', '').replace('\r', '').lower().endswith('%end'):
				print('%---', file=f)
				print('%END', end='', file=f)
		with open(('.').join(self.score.split('.')[:-1]) + '_buf.txt', 'r', encoding='utf-8') as f:
			self.raw2 = f.read()
		with open(('.').join(self.score.split('.')[:-1]) + '_buf.json', 'w', encoding='utf-8') as f:
			self.prioritize_title_and_tag()
			# key 必须是**文件名**: make_link() 用 file.get(self.score.split('/')[-1]) 取,
			# 之前写成 {self.mbid: ...} 与读取端对不上, by_* 链接实际拿不到数据。
			json.dump({self.score.split('/')[-1]: self.others}, f, indent=4, ensure_ascii=False)
		return 0
	def move_buf(self):
		try:
			with open(self.prefix + '_buf.txt', 'r', encoding='utf-8') as f:
				self.raw2 = f.read()
				if not self.raw2.replace('\n', '').replace('\r', '').lower().endswith('%end'):
					raise BadBufError
			shutil.move(self.prefix + '_buf.txt', self.prefix + '.txt')
			shutil.move(self.prefix + '_buf.json', self.prefix + '.json')
		except FileNotFoundError:
			print(f'Error: file \'{self.score}\' not found!')
			raise
		except BadBufError:
			print(f'Bad buf: {self.prefix + '_buf.txt'}!')
	def make_link(self):
		# ⚠ 2026-09-24: 只给**语料自己的 `scores/`** 里的曲谱建 by_* 链接树。
		#   by_* 树是相对**当前目录**生成的, 而任何一次 parse() 都会调到这里 ——
		#   实测: 在 jianpu-db 里解析一份 /tmp 副本, `by_status/ok/th10_06.txt` 就被改指到
		#   `../../../../../../tmp/injtest5/th10_06.txt`, 整棵已提交的 by_* 树被污染。
		#   草稿/副本/沙箱解析(尖 tests、validate_repo 的沙箱等)不该动仓库;
		#   沙箱自己在沙箱目录里跑 `scores/x.txt`, 仍然照常建树。
		if os.path.dirname(self.score.replace('\\', '/')) not in ('scores', './scores'):
			return
		try:
			with open(self.prefix + '.json', 'r', encoding='utf-8') as f:
				file = json.load(f)
			# data.json 以"文件名"为 key(不再依赖任何单一主键; 标识可多可无)
			attrib = file.get(self.score.split('/')[-1], {})
			for i in attrib.keys():
				if not attrib[i]:
					continue
				filename = ''
				if i in ['usertag', 'file']:
					continue
				elif i == 'title':
					# title 现在是列表(与其它字段形态一致) -> 取首值; 同时兼容旧的字符串形态
					_tv = attrib.get('title')
					_t = (_tv[0] if isinstance(_tv, list) and _tv else (_tv or ''))
					_ts = _t.replace(' ', '') if _t else ''
					if len(_ts) >= 2 and _ts[0] in 'qwertyuioppasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890':
						if _ts[1] in 'qwertyuioppasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890':
							filename = 'by_title/' + _ts[0].upper() + '/' + _ts[1].upper() + '/' + _t + '/' + self.score.split('/')[-1]
						else:
							filename = 'by_title/' + _ts[0].upper() + '/others/' + _t + '/' + self.score.split('/')[-1]
					else:
						filename = 'by_title/others/' + _t + '/' + self.score.split('/')[-1]
				else:
					# 字段值可能是列表(多值), 也可能是字符串(schema 里定义为单值的, 如 MBID):
					# 字符串直接 for 会逐字符拆开(by_M/mbid/…/0/…), 必须先包成列表。
					_vals = attrib[i] if isinstance(attrib[i], list) else [attrib[i]]
					for j in _vals:
						filename = f'by_{i}/' + j + '/' + self.score.split('/')[-1]
						filename = ('').join(filename.split('.')[:-1]) + '.' + filename.split('.')[-1]
						filename = filename.replace('?', '')
						dest = Path(filename)
						Path(filename).parent.mkdir(parents=True, exist_ok=True)
						dest.unlink(missing_ok=True)
						# start 必须是**链接所在目录**: 传 filename(链接自身)会当成目录,
						# 相对路径多出一层 .., 链接全部指向仓库外 -> 显示为死链
						# (实测 by_tag/th01/th01_01.txt 指向 ../../../scores/..., 应为 ../../)。
						# 统一用正斜杠: Windows 生成的反斜杠与 Linux(CI) 不同, 会来回改。
						dest.symlink_to(_rel(self.score, filename))
				filename = ('').join(filename.split('.')[:-1]) + '.' + filename.split('.')[-1]
				filename = filename.replace('?', '')
				dest = Path(filename)
				Path(filename).parent.mkdir(parents=True, exist_ok=True)
				dest.unlink(missing_ok=True)
				dest.symlink_to(_rel(self.score, filename))
		except FileNotFoundError:
			print(f'Error: file \'{self.score}\' not found!')
			raise
	def expand(self):
		pattern = r"R(\d*)\s*\{\s*(.*?)\s*\}(?:\s*A\s*\{\s*(.*?)\s*\})?"
		self.raw_expanded = re.sub(pattern, replacer, self.raw2, flags=re.DOTALL)
		# 再补全 KeepLength 的"省略时值"(jianpu-ly 的 sticky duration) -> 计算机可直接读
		self.raw_expanded = expand_keep_length(self.raw_expanded)
		return self.raw_expanded
	def write_expand(self):
		with open(('.').join(self.score.split('.')[:-1]) + '_expand.txt', 'w', encoding='utf-8') as f:
			print(self.raw_expanded, end='', file=f)
	def parse(self):
		if len(self.score.split('.')) > 1:
			if self.score.split('.')[-2].endswith('_expand') or self.score.split('.')[-2].endswith('_buf'):
				pass
			else:
				try:
					self.read()
					self.derive_others()
					self.write_buf()
					self.expand()
					# ⚠ 2026-09-24: 这里原来无条件 `self.write_expand()`, 于是**每次解析**
					#   (parse_scores.py 每次 refresh 都会跑)都给每首歌写一份 `*_expand.txt`
					#   调试副本 —— 7820 份 / 32MB, 曾经全被提交进仓库, 而且
					#   melody_oct.py / famous2.py / probe_h_*.py 这些只 glob scores/*.txt
					#   不过滤的工具一直在把副本当曲谱统计。
					#   现在改成默认不写(需要时显式调 write_expand(), 或设 JIANPU_WRITE_EXPAND=1)。
					if os.environ.get("JIANPU_WRITE_EXPAND") == "1":
						self.write_expand()
					self.move_buf()
					self.make_link()
				except NoScoreError:
					pass
