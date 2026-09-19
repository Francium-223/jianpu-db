import sys
import json
import re
import os
import shutil
import warnings
import schema
from pathlib import Path
def load_tag_rules(path='tags.json'):
	"""蕴涵/等同规则: 从 tags.json 派生(单一真源), 不再读 tag_implications.json /
	tag_equality.json —— 那两份本就是这个文件的冗余副本, 三处各写一份必然漂移
	(实测"东方同人曲"被错挂在"东方原曲"下: 同人曲不是原曲)。
	那两份旧文件已归档到 misc/, 仅供查阅, 改了不会生效。

	tags.json 是 **DAG 而非树**: 一个名字可以出现在多处(实测"东方整数作原曲"
	同时挂在"东方旧作原曲"与"东方新作原曲"下)。不过这类中间节点只是**代码推路线时
	生成的**, 人写 usertag 时只会写叶子(如 th10), 所以歧义不会从输入进来 ——
	但仍必须按**路径**递归构造嵌套 dict, 绝不做 名字->父 的映射: 那样后写会覆盖
	先写, 会把 th01-th05 的"旧作"错算成"新作"(实测 309 份里错 97 份)。

	返回 (imply, equal), 与旧的 tag_implications.json / tag_equality.json 逐项等值:
	  imply    = 嵌套 dict, 键取每个节点 name[0]
	  equal[0] = 别名数 >= 2 的节点, 按先序;  equal[1] = [[]] (历史形状, 空)
	"""
	with open(path, 'r', encoding='utf-8') as f:
		raw = f.read()
	tree = json.loads(raw)
	imply = {}
	groups = []

	def walk(nodes, carry):
		for nd in nodes:
			names = nd.get('name') or []
			if not names:
				continue
			if len(names) >= 2:
				groups.append(list(names))
			here = carry.setdefault(names[0], {})
			walk(nd.get('child') or [], here)

	walk(tree, imply)
	return imply, [groups, [[]]]


imply, equal = load_tag_rules()
class NoScoreError(Exception):
	pass
class NotTitleError(Exception):
	pass
class BadBufError(Exception):
	pass
def safe_add(a, b):
	c = a[:]
	for i in b:
		if not i in c:
			c.append(i)
	return c
def safe_minus(a, b):
	c = []
	for i in a:
		if not i in b:
			c.append(i)
	return c
def maybe_add(a, b):
	c = []
	s = True
	for i in range(len(a)):
		if b == a[i]:
			s = False
			c.append(a[i])
			continue
		elif b.startswith(a[i]) and not s:
			s = True
			continue
		c.append(a[i])
	if s:
		c.append(b)
		s = False
	if not c:
		c = [b]
	return c
def _rel(target, link_path):
	"""链接目标: 相对链接所在目录, 统一用正斜杠。

	Windows 的 os.sep 是反斜杠、Linux 是正斜杠 —— 不统一的话, 本地生成一次、
	CI(Linux) 再生一次, 同一批链接的文本内容就不同, 每次提交都在改它们。
	"""
	return os.path.relpath(target, start=os.path.dirname(link_path)).replace(os.sep, '/')


def same_ends(a, b):
	for i in range(1, min(len(b) + 1, len(a) + 1)):
		if not equal_tag(b[-i], a[-i]):
			return False
	return True
def equal_in(a, b):
	for i in a:
		if b == i.split('/')[-1]:
			return True
	return False
def equal_tag(a, b):
	for i in equal[0]:
		if equal_in(i, a) and equal_in(i, b):
			return True
	return False
def get_meta_lines(s):
	d = []
	for i in s:
		d.append(i)
		if i.replace(' ', '').startswith('%--'):
			return d
	return d
def goto_node(p):
	if p == []:
		return imply
	a = imply
	for i in p:
		a = a[i]
	return a
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
	for line in text.splitlines():
		s = line.strip()
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
			# 取时值: 可能前置(q1 / q1' / s,6) 或后置(1q / ,6s / 3c.)
			m_pre = re.match(r'^([cqsdh])(.*)$', tok)
			m_post = re.match(r'^(.*?)([cqsdh])([.]*)$', tok)
			val = ''
			if m_pre and re.match(r"^[,']*[0-9x]", m_pre.group(2)):
				val = m_pre.group(1)
			elif m_post:
				val = m_post.group(2)
			if val:
				cur_val = val
				toks.append(tok)
			else:
				# 无时值: KeepLength 生效时补上当前时值, 否则按四分音(不加前缀)
				if keep and cur_val:
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
	def find_tag(self, n):
		if n.startswith('!'):
			self.find_nottag(n.lstrip('!'))
			return
		for i in equal[0]:
			for j in i:
				if same_ends(j.split('/'), n.split('/')):
					self.tag = safe_add(self.tag, j.split('/'))
					self.origtag = safe_add(self.origtag, i)
					break
		for i in equal[1]:
			for j in i:
				if j == n:
					self.tag = safe_add(self.tag, j.split('/'))
					self.origtag = safe_add(self.origtag, i)
					break
		for i in self.origtag:
			self.where_imply(i, [])
	def find_nottag(self, n):
		for i in equal[0]:
			for j in i:
				if same_ends(j.split('/'), n.split('/')):
					self.nottag = safe_add(self.nottag, j.split('/'))
					self.orignottag = safe_add(self.orignottag, i)
					break
		for i in equal[1]:
			for j in i:
				if j == n:
					self.nottag = safe_add(self.nottag, j.split('/'))
					self.orignottag = safe_add(self.orignottag, i)
					break
		self.nottag = safe_add(self.nottag, [n])
		for i in self.nottag:
			self.where_not_imply(i, [])
	def where_imply(self, n, p):
		o = ''
		if '/' in n:
			o = n.split('/')
			n = o[0]
		for k, v in goto_node(p).items():
			q = p + [k]
			if k == n:
				for l in self.origtag:
					if ('/').join(q).endswith(l):
						self.tag_route = maybe_add(self.tag_route, ('/').join(q))
						for m in range(1, len(q) + 1):
							self.all_tag_route = safe_add(self.all_tag_route, [('/').join(q[:m])])
						#self.all_tag_route = safe_add(self.all_tag_route, [('/').join(q)])
			if o:
				self.where_imply(('/').join(o[1:]), q)
			else:
				self.where_imply(n, q)
	def where_not_imply(self, n, p):
		o = ''
		if '/' in n:
			o = n.split('/')
			n = o[0]
		# 原先这里是**两个独立的循环**, 各自把每个子节点递归一遍:
		#   A: where_not_imply(n, p+[k])            —— 用原标签名继续找
		#   B: where_not_imply(o[1:] or n, p+[k])   —— 路径形态时消耗掉一段
		# 单段标签时(A 和 B 的递归参数完全相同)整棵树被白走两遍(2^深度)。
		# 合并成一个循环; 只有在 n 是路径时(= o 非空)两条递归才确实不同, 都保留。
		for k, v in goto_node(p).items():
			if k == n:
				if set(self.orignottag) & set(p):
					self.nottag = safe_add(self.nottag, p)
				for l in self.orignottag:
					if ('/').join(p + [k]).endswith(l):
						self.nottag_route = maybe_add(self.nottag_route, ('/').join(p + [k]))
			if o:
				self.where_not_imply(('/').join(o[1:]), p + [k])
				self.where_not_imply(n, p + [k])
			else:
				self.where_not_imply(n, p + [k])
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
	def getusertag(self, a):
		for j in re.split(r'[,|，|、]', a[a.find('=') + 1:].strip(' ')):
			self.usertag = safe_add(self.usertag, [j.strip(' ')])
			self.origtag = safe_add(self.origtag, [j.strip(' ')])
			self.find_tag(j.strip(' '))
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
					if re.match(r"^[,']*[qsdh]*[,']*[1-7x0]", t) or t in ('-', '|', '~')]
		if cur:
			sections.append({'subtitle': cur_sub, 'score': ' '.join(cur)})
		full = ' | '.join(x['score'] for x in sections if x['score'])
		n_notes = len([t for t in full.split() if re.match(r"^[,']*[qsdh]*[,']*[1-7x0]", t)])
		# 各字段的形态由 schema 决定(字符串或列表) -> 原样传出去, 不在这里强转
		return {
			'file': [self.score.split('/')[-1]],
			'status': self.others.get('status', ''),
			'title': self.title,                      # ← 单值字符串(schema 里由 return_itself 产出)
			# 字段名统一用**单数**, 与 data.json 完全一致(tag/usertag, 不是 tags/usertags)
			'tag': self.others.get('tag', []),
			'usertag': self.others.get('usertag', []),
			'transcriber': self.others.get('transcriber', []),
			'sections': sections,
			'score': full,
			'n_notes': n_notes,
		}
	def read(self):
		try:
			with open(self.score, 'r', encoding='utf-8') as f:
				self.raw = f.readlines()
				self.raw2 = f.read()
			for i in get_meta_lines(self.raw):
				i = i.rstrip('\n')
				if i.replace(' ', '').startswith('%--') or i.replace(' ', '').startswith('tag=') or i.replace(' ', '').startswith('tagroute='):
					continue
				if i.replace(' ', '').startswith('usertag='):
					self.getusertag(i)
					continue
				if i.replace(' ', '').lower().startswith('file='):
					# file 由文件名派生(write_buf 里写进 JSON), 不是源字段 ——
					# 曲谱文件里若残留这一行(历史误写)要忽略, 否则会被读回来又写回去。
					continue
				if '=' in i:
					k, raw = i.split('=', 1)
					k = k.strip(' ')
					# schema 里有这个字段的解析函数就用它, 没有就用 schema.default_parse(多值列表)。
					# 解析函数返回什么类型, 这个字段就是什么类型(字符串或列表); 不合规会抛异常。
					v = schema.schema.get(k, schema.default_parse)(raw.strip(' '))
					if isinstance(v, list) and isinstance(self.others.get(k), list):
						# 多值字段: 同一个字段可以写多行, 累加去重
						self.others[k] = safe_add(self.others[k], v)
					else:
						self.others[k] = v
					continue
				if i == '%' + self.score.split('/')[-1]:
					continue
				if i.startswith('%'):
					self.comments.append(i.rstrip('\n'))
					continue
				self.getusertag(i)
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
	def process_others(self):
		# 外部标识(MBID / Wikidata / ...)不做特殊处理 —— 它们和 alias/status/transcriber
		# 等一样, 在 read() 里按 `键=值` 统一进 others, 由 make_link() 统一建 by_<键>/ 链接。
		for n in self.all_tag_route:
			self.tag = safe_add(self.tag, n.split('/'))
			for i in equal[0]:
				for j in i:
					if same_ends(j.split('/'), n.split('/')):
						self.tag = safe_add(self.tag, j.split('/'))
						break
			for i in equal[1]:
				for j in i:
					if j == n:
						self.tag = safe_add(self.tag, j.split('/'))
						break
		maybetag = safe_minus(self.tag, self.nottag)
		self.others['usertag'] = []
		for i in self.usertag:
			self.others['usertag'] = safe_add(self.others['usertag'], [i])
		self.others['tag'] = safe_add(self.others['tag'], self.others['usertag'])
		for i in maybetag + self.tag_route:
			self.others['tag'] = safe_add(self.others['tag'], i.split('/'))
			for j in equal[0]:
				if i in j:
					for k in j:
						self.others['tag'] = safe_add(self.others['tag'], k.split('/'))
			for j in equal[1]:
				if i in j:
					for k in j:
						self.others['tag'] = safe_add(self.others['tag'], k.split('/'))
		self.others['tagroute'] = self.tag_route
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
					self.process_others()
					self.write_buf()
					self.expand()
					self.write_expand()
					self.move_buf()
					self.make_link()
				except NoScoreError:
					pass
