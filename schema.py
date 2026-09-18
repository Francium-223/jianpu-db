#schema.py：解析某个属性的值。
#在这里写解析某项属性（如 MBID 之类的）的函数。
#契约: 函数必须**输入一个字符串**（等号后面的原文），并**返回解析后的值**。
#   * 返回 str  -> 该字段是单值字符串字段
#   * 返回 list -> 该字段是多值列表字段
#   * 不合规就抛异常（如 ValueError），调用方会直接把错误报出来。
#没在 schema 里写函数的属性走 default_parse（下面那个函数），也是列表字段。
import re


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


#属性: 解析这个属性的函数
schema = {
	'MBID': parse_mbid,
	'title': return_itself,
	'status': return_itself
}
