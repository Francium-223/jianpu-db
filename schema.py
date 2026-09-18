#schema.py：检测某属性是否合规，不合规则会报错。
import re
#在这里写判断某项属性（如MBID之类的）的函数。必须输入一个字符串、返回一个布尔值。
def check_mbid(a: str) -> bool:
    return re.match('[0123456789abcdef]{8}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{12}', a)
#属性: 判断这个属性的函数
schema = {
    'MBID': check_mbid
}