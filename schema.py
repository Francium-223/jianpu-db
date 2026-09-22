#schema.py：解析某个属性的值；并声明**属性之间的依赖**与执行顺序。
#
#【契约 A：一阶 / 逐值】deps 为空
#   函数必须**输入一个字符串**（等号后面的原文），并**返回解析后的值**：
#     * 返回 str  -> 单值字符串字段
#     * 返回 list -> 多值列表字段
#     * 不合规就抛异常（如 ValueError），调用方会直接把错误报出来。
#   没在 schema 里登记的属性走 default_parse。
#   同一个字段可以出现多行：调用方按**出现顺序**逐行调用本函数再累加
#   （list 字段去重保序、str 字段后者覆盖前者）—— 累加是**调用方的**职责，
#   不在本文件里，函数本身必须无状态。
#
#【契约 B：整对象 / 衍生】声明了 deps 的属性
#   函数输入是 **Score 对象**（不是字段字符串），**整份谱只跑一次**，
#   且必须等 deps 里的属性全部就绪之后才跑。
#   例：usertag（人写的叶子） --derive--> tag --derive--> tagroute
#
#【执行顺序】order() 用 Kahn 拓扑排序给出顺序，**与本文件的书写顺序无关**；
#   依赖成环就 Warning 并退回声明顺序（strict=True 时直接抛错，给 CI 用）。
#   依赖只能声明**属性名**；tags.json 这种全局真源不是属性，写在下面的 doc 里：
#       tag / tagroute = f(usertag, tags.json)
import json
import re
import warnings
from dataclasses import dataclass

# ---------------- 一阶（逐值）解析函数 ----------------

def default_parse(a: str) -> list:
	"""没写解析函数的字段走这里: 按 , ， 、 | 切成多值列表(空项丢掉)。"""
	return [x.strip() for x in re.split(r'[,，、|]', a) if x.strip()]


def parse_mbid(a: str) -> str:
	"""MBID: 单个 uuid 字符串。不合规直接报错。"""
	a = a.strip()
	if not re.fullmatch(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}'
						r'-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', a):
		raise ValueError(f'not a valid MBID: {a!r}')
	return a


def return_itself(a: str) -> str:
	return a.strip()


# ---------------- 标签图的机械（从 score.py 迁来，逐字保留） ----------------
# 为什么在这里: 它是"usertag -> tag/tagroute"的**唯一实现**。放 schema 里,
# 依赖声明与实现就近可见; score.py 只 import 别名, 不会出现第二份实现。

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


def goto_node(p):
	if p == []:
		return imply
	a = imply
	for i in p:
		a = a[i]
	return a


class TagState():
	"""一份谱的标签推导状态(原来挂在 Score 上的那几个字段 + 方法, 原样搬来)。

	方法体**逐字**保留原实现 —— 推导结果与顺序必须与搬迁前完全一致:
	maybe_add 只对精确重复去重、且结果与插入顺序有关, 所以这里不能"顺手优化"。
	"""

	def __init__(self):
		self.tag_route = []
		self.all_tag_route = []
		self.nottag_route = []
		self.tag = []
		self.usertag = []
		self.origtag = []
		self.nottag = []
		self.orignottag = []

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

	def getusertag(self, a):
		"""人写的一个 usertag 原文(可能逗号分隔多个) -> 状态里登记。"""
		for j in re.split(r'[,|，|、]', a[a.find('=') + 1:].strip(' ')):
			self.usertag = safe_add(self.usertag, [j.strip(' ')])
			self.origtag = safe_add(self.origtag, [j.strip(' ')])
			self.find_tag(j.strip(' '))


def _state_of(score):
	"""整份谱只建一次状态(两个衍生字段共用; 幂等, 重跑 parse 会重建)。"""
	st = getattr(score, '_tagstate', None)
	if st is None:
		st = TagState()
		for v in (score.others.get('usertag') or []):
			st.getusertag(v)
		score._tagstate = st
	return st


def derive_tag(score) -> list:
	"""tag = usertag ∪ (隐含祖先 ∪ 别名的每一段)；实现与搬迁前的 process_others 一致。"""
	st = _state_of(score)
	tag = list(st.tag)
	for n in st.all_tag_route:
		tag = safe_add(tag, n.split('/'))
		for i in equal[0]:
			for j in i:
				if same_ends(j.split('/'), n.split('/')):
					tag = safe_add(tag, j.split('/'))
					break
		for i in equal[1]:
			for j in i:
				if j == n:
					tag = safe_add(tag, j.split('/'))
					break
	maybetag = safe_minus(tag, st.nottag)
	out = []
	for i in (score.others.get('usertag') or []):
		out = safe_add(out, [i])
	for i in maybetag + st.tag_route:
		out = safe_add(out, i.split('/'))
		for j in equal[0]:
			if i in j:
				for k in j:
					out = safe_add(out, k.split('/'))
		for j in equal[1]:
			if i in j:
				for k in j:
					out = safe_add(out, k.split('/'))
	return out


def derive_tagroute(score) -> list:
	"""tagroute = 该标签在 DAG 里的完整路径(可能多条)。"""
	return list(_state_of(score).tag_route)


# ---------------- 依赖表 + 执行顺序 ----------------

@dataclass(frozen=True)
class Attr:
	"""一个属性的生产者。

	fn   : deps 为空 -> fn(原文: str) -> str|list   (一阶, 可被多行多次调用)
	       deps 非空 -> fn(score) -> str|list       (整对象, 只跑一次)
	deps : 依赖的**属性名**(只能写属性, 不能写 tags.json 这类全局真源)
	doc  : 给人看的说明; 全局真源(deps 表达不了的东西)必须写在这里
	"""
	fn: object
	deps: tuple = ()
	doc: str = ''


schema = {
	# 一阶字段(逐值)
	'title': Attr(return_itself, (), '单值字符串; 文件名/NotTitleError 依赖它'),
	'MBID': Attr(parse_mbid, (), '单值 uuid'),
	'status': Attr(return_itself, (), 'ok / midi / ocr ... (parse_scores 用白名单筛)'),
	'usertag': Attr(default_parse, (), '人只写**叶子**; 可多行、可逗号分隔'),
	# 衍生字段(整对象) —— 顺序由这里的 deps 决定, 与书写顺序无关
	'tag': Attr(derive_tag, ('usertag',), '全局真源: tag = f(usertag, tags.json)'),
	'tagroute': Attr(derive_tagroute, ('usertag', 'tag'),
					 '全局真源: tagroute = f(usertag, tags.json); 与 tag 共用同一份推导状态'),
}


def parser(name):
	"""取某个属性的生产者; 没登记的属性走 default_parse(多值列表)。"""
	attr = schema.get(name)
	return attr.fn if attr else default_parse


def order(strict=False):
	"""按 deps 做 Kahn 拓扑排序(同层按声明顺序, 保证可复现)。

	成环 -> Warning 并**退回声明顺序**(strict=True 时抛错, 给 CI 用)。
	依赖了未登记的属性 -> Warning(仍按声明顺序执行, 该依赖被忽略)。
	"""
	names = list(schema.keys())
	indeg = {n: 0 for n in names}
	for n in names:
		for d in schema[n].deps:
			if d not in schema:
				warnings.warn(f'{n} 依赖未登记的属性 {d!r}(已忽略)', RuntimeWarning, stacklevel=2)
				continue
			indeg[n] += 1
	ready = [n for n in names if indeg[n] == 0]
	out = []
	while ready:
		n = ready.pop(0)
		out.append(n)
		for m in names:
			if n in schema[m].deps:
				indeg[m] -= 1
				if indeg[m] == 0:
					ready.append(m)
	if len(out) != len(names):
		cyc = [n for n in names if n not in out]
		msg = ('属性依赖成环, 退回声明顺序: ' + ', '.join(cyc) +
			   '  依赖边: ' + ', '.join(f'{n}->{d}' for n in names for d in schema[n].deps
										if n in cyc or d in cyc))
		if strict:
			raise RuntimeError(msg)
		warnings.warn(msg, RuntimeWarning, stacklevel=2)
		return names
	return out
