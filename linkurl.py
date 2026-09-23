# -*- coding: utf-8 -*-
"""收录页 URL 的**唯一**校验/规范化实现(纯函数, 不读任何文件, 所以服务端也能直接 import)。

为什么独立成一个模块: `schema.py` 一 import 就要读 cwd 下的 `tags.json`(标签真源),
而 `jianpu-web/app/server.py`(网页投稿)只想知道"这个 URL 能不能当收录页"。
于是口径落在这里, `schema.parse_link` 只是它的一层皮 —— **不许再写第二份**。

用户口径(2026-09-23): 「我要的不是个自动跳转到搜索页面的按钮, 我要的是跳转到它
**具体收录的那一页**」。所以:
  * 只收 http(s) 的确切页面; 搜索页一律拒收(前端现拼搜索即可, 进语料就等于
    把"待补充"伪装成"已收录")。
  * 返回**列表**: 多值字段写回源文件时是逗号连接成一行, 所以必须按逗号切
    (否则第二次 parse_scores 会把多个 URL 当成一个畸形 URL —— 往返损坏)。
"""
import re
import urllib.parse

# 收录页 URL 里常见的跟踪参数: 去掉, 否则同一个页面会有多种写法 -> 去重失效
_TRACKING = {'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
			 'from', 'spm', 'share_source', 'share_medium', 'refer', 'referer',
			 'fbclid', 'gclid', 'vd_source', 'buvid'}

# "像搜索页"的判据(只看 URL, 不请求网络):
#   * 站内搜索路径: /search、/search/...、/results、/so/ ... 或 search.xxx.com 这种搜索子域
#   * 首页/空路径 + 搜索参数: ?q= ?s= ?w= ?keys= ?keyword= ?query= ?search_query=
_SEARCHY = re.compile(r'(^|[/#?&.])(search|results|sou)([/?#=&.]|$)', re.I)
_SEARCH_PARAM = re.compile(r'[?&](q|s|w|k|keys|keyword|query|search_query|wd)=', re.I)


def looks_like_search(p) -> bool:
	"""p 是 urllib.parse.urlsplit 的结果。"""
	if _SEARCHY.search(p.netloc + p.path + ('#' + p.fragment if p.fragment else '')):
		return True
	# 参数名像搜索 **且** 路径很浅(首页/空) —— 免得把 `?w=1200` 这类正常参数一棒子打死
	return bool(_SEARCH_PARAM.search('?' + p.query)) and p.path.strip('/') == ''


def parse_link(a: str) -> list:
	"""一行(可以是逗号分隔的多个)URL -> 规范化后的列表; 不合规/是搜索页就抛 ValueError。

	规范化: 去首尾空白、host 转小写、去掉跟踪参数。片段(`#`)保留 —— 网易云有 `#/song?id=…`。
	"""
	out = []
	for part in re.split(r'[,\s]+', (a or '').strip()):
		if not part:
			continue
		p = urllib.parse.urlsplit(part)
		if p.scheme not in ('http', 'https') or not p.netloc:
			raise ValueError(f'not a valid http(s) link: {part!r}')
		if looks_like_search(p):
			raise ValueError(f'这是**搜索页**, 不是收录页 —— 请填这首歌在那一站的具体页面: {part!r}')
		q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)
			 if k.lower() not in _TRACKING]
		out.append(urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path,
											urllib.parse.urlencode(q), p.fragment)))
	if not out:
		raise ValueError('link 是空的')
	return out


def add_to_score_file(path, url):
	"""把 `link=<url>` 写进一份曲谱文件的**元数据区**(第一条 `%--` 之前)。

	返回 (added, already) —— 两个都已规范化。同一个 URL 不重复写;
	文件里已有的 `link=` 行就并到那一行(多值字段写回时本来就是逗号连接);
	行尾保持原样(\r\n 还是 \n); 只动这一处, 其余字节不变。

	**唯一实现**: 网页上「＋ 补收录页」(server.py) 与命令行 tools/add_link.py 都调它。
	"""
	added, already = [], []
	urls = parse_link(url)
	with open(path, 'rb') as f:
		raw = f.read()
	nl = '\r\n' if b'\r\n' in raw else '\n'
	text = raw.decode('utf-8')
	lines = text.splitlines()
	idx = next((i for i, ln in enumerate(lines) if ln.replace(' ', '').startswith('%--')), len(lines))
	have = []
	for i in range(idx):
		if lines[i].startswith('link='):
			try:
				have += parse_link(lines[i][5:])
			except ValueError:
				pass
	for u in urls:
		(already if u in have else added).append(u)
	if not added:
		return added, already
	li = next((i for i in range(idx) if lines[i].startswith('link=')), None)
	if li is None:
		lines.insert(idx, 'link=' + ','.join(added))
	else:
		lines[li] = lines[li] + ',' + ','.join(added)
	with open(path, 'wb') as f:
		f.write((nl.join(lines) + nl).encode('utf-8'))
	return added, already


# usertag 里不许出现的字符(会破坏 `key=value` 行格式或列表分隔)
_BAD_TAG = re.compile(r'[,\uFF0C\u3001|=%\t\r\n<>]')


def parse_tag(tag: str) -> str:
	"""标签(usertag)的校验: 非空、<=30 字、不许含逗号/等号/竖线等会破坏格式的字符。"""
	t = (tag or '').strip()
	if not t:
		raise ValueError('标签是空的')
	if len(t) > 30:
		raise ValueError(f'标签太长(<=30 字): {t!r}')
	if _BAD_TAG.search(t):
		raise ValueError(f'标签里不能有逗号/等号/竖线等字符: {t!r}')
	return t


def add_usertag(path, tag, clear_todo=True):
	"""把 usertag 写进曲谱的**元数据区**(第一条 `%--` 之前); 返回 'added' / 'exists'。

	与 `add_to_score_file` 同一个套路(行尾保持、只动一处、大小写不敏感去重),
	所以**这里是"写进曲谱"的唯一实现**:
	  * 网页上「＋ 补标签」(server.py:save_tags)
	  * 命令行 jianpu2/tools/propose_tags.py(add_tag 只是本函数的皮)
	  * jianpu2/tools/harvest_artists.py(抽到的歌手/分类落盘)
	`clear_todo=True` 时顺带删掉 `todo=add tags`(那条 todo 的字面意思就是"该加标签了")。
	"""
	tag = parse_tag(tag)
	with open(path, 'rb') as f:
		raw = f.read()
	nl = '\r\n' if b'\r\n' in raw else '\n'
	lines = raw.decode('utf-8').splitlines()
	end = next((i for i, ln in enumerate(lines) if ln.replace(' ', '').startswith('%--')), None)
	if end is None:                     # 没有 %-- 标记: 插在元数据区末尾, 绝不插到正文/文件尾
		end = 0
		for i, ln in enumerate(lines):
			s = ln.strip()
			if not s or s.startswith('%') or re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', s):
				end = i + 1
			else:
				break
	ui = next((i for i in range(end) if lines[i].startswith('usertag=')), None)
	have = ([x.strip() for x in lines[ui][8:].split(',') if x.strip()] if ui is not None else [])
	if any(t.casefold() == tag.casefold() for t in have):   # 大小写不敏感去重(BEYOND/Beyond)
		return 'exists'
	if ui is None:
		lines.insert(end, 'usertag=' + tag)
	else:
		lines[ui] = 'usertag=' + ','.join(have + [tag])
	if clear_todo:
		lines = [ln for ln in lines if ln.strip() != 'todo=add tags']
	with open(path, 'wb') as f:
		f.write((nl.join(lines) + nl).encode('utf-8'))
	return 'added'
