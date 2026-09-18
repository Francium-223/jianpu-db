import re
def check_mbid(a):
	return re.match('[0123456789abcdef]{8}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{12}', a)
schema = {
	'mbid': check_mbid
	}