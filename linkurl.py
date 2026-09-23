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
