import sys
import json
import re
with open('tag_imply.json', 'r', encoding='utf-8') as f1:
	imply = json.load(f1)
with open('tag_equal.json', 'r', encoding='utf-8') as f2:
	equal = json.load(f2) 
class NotMBIDError(Exception):
	pass
class NotTitleError(Exception):
	pass
tag = []
usertag = []
origtag = []
nottag = []
orignottag = []
mbid = ''
title = ''
others = {'tag': [], 'usertag': [], }
comments = []
def safe_add(a, b):
	c = a[:]
	for i in b:
		if not i in c:
			c.append(i)
	if c:
		return c
	return b
def safe_minus(a, b):
	c = []
	for i in a:
		if not i in b:
			c.append(i)
	return c
def find_tag(n):
	global tag
	global origtag
	if n.startswith('!'):
		find_nottag(n.lstrip('!'))
		return
	for i in equal:
		if n in i:
			tag = safe_add(tag, i)
			if n in origtag:
				origtag = safe_add(origtag, i)
	tag = safe_add(tag, [n])
	for i in tag:
		where_imply(i, [])
def find_nottag(n):
	global nottag
	global orignottag
	for i in equal:
		if n in i:
			nottag = safe_add(nottag, i)
			if n in orignottag:
				orignottag = safe_add(orignottag, i)
	nottag = safe_add(nottag, [n])
	for i in nottag:
		where_not_imply(i, [])
def goto(p):
	if p == []:
		return imply
	a = imply
	for i in p:
		a = a[i]
	return a
def where_imply(n, p):
	global tag
	for k, v in goto(p).items():
		if k == n and set(origtag) & set(p + [k]):
			tag = safe_add(tag, p)
		where_imply(n, p + [k])
def where_not_imply(n, p):
	global nottag
	for k, v in goto(p).items():
		if k == n and set(orignottag) & set(p):
			nottag = safe_add(nottag, p)
		where_not_imply(n, p + [k])
def get_meta_lines(s):
	d = []
	for i in s:
		d.append(i)
		if i.replace(' ', '').startswith('%--'):
			return d
	return []
def prioritize_title_and_tag(a):
	b = {}
	b['file'] = a['file']
	b['title'] = a['title']
	b['usertag'] = a['usertag']
	b['tag'] = a['tag']
	for i in a.keys():
		if not i in ['file', 'title', 'tag', 'usertag']:
			b[i] = a[i]
	return(b)
score = sys.argv[1]
try:
	with open(score, 'r', encoding='utf-8') as f:
		raw = f.readlines()
	for i in get_meta_lines(raw):
		i = i.rstrip('\n')
		if i.replace(' ', '').startswith('%--'):
			continue
		if i.replace(' ', '').lower().startswith('mbid='):
			mbid = i[i.find('=') + 1:].strip(' ')
			if not re.match('[0123456789abcdef]{8}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{12}', mbid) and False:
				raise NotMBIDError
			continue
		if i.replace(' ', '').startswith('usertag='):
			for j in re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')):
				usertag = safe_add(usertag, [j])
				origtag = safe_add(origtag, [j])
				find_tag(j.strip(' '))
			continue
		'''
		if i.replace(' ', '').startswith('tag='):
			for j in re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')):
				origtag.append(j)
				find_tag(j.strip(' '))
			continue
		'''
		if i.replace(' ', '').startswith('title='):
			title = i[i.find('=') + 1:].strip(' ')
			continue
		if '=' in i:
			t = i[:i.find('=')].strip(' ')
			if t in others.keys():
				others[t] = safe_add(others[t], re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')))
			else:
				others[t] = safe_add([], re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')))
			continue
		if i == '%' + score.split('/')[-1]:
			continue
		if i.startswith('%'):
			comments.append(i.rstrip('\n'))
			continue
		for j in re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')):
			usertag = safe_add(usertag, [j])
			origtag = safe_add(origtag, [j])
			find_tag(j.strip(' '))
	maybetag = safe_minus(tag, nottag)
	others['usertag'] = []
	for i in usertag:
		others['usertag'] = safe_add(others['usertag'], [i])
	for i in maybetag:
		others['tag'] = safe_add(others['tag'], [i])
		for j in equal:
			if i in j:
				others['tag'] = safe_add(others['tag'], j)
	with open(score, 'w', encoding='utf-8') as f:
		print('%' + score.split('/')[-1], file=f)
		for i in comments:
			print(i.rstrip('\n'), file=f)
		print('MBID=' + mbid, file=f)
		print('title=' + title, file=f)
		for i in others.keys():
			print(i + '=' + (',').join(others[i]), file=f)
		others['title'] = title
		others['file'] = score.split('/')[-1]
		d = False
		for i in raw:
			if i.replace(' ', '').startswith('%--'):
				d = True
			if d:
				print(i.rstrip('\n'), file=f)
	with open(('.').join(score.split('.')[:-1]) + '.json', 'w', encoding='utf-8') as f:
		json.dump({mbid : prioritize_title_and_tag(others)}, f, indent=4, ensure_ascii=False)
except NotMBIDError:
	print('Error: no MBID!')
	print(f'Try adding \'MBID=(what you\'ve found in your address bar after \'https://musicbrainz.org/work/\'.)\'.)\' in {score}.')
except NotTitleError:
	print(f'Error: no title!')
	print(f'Try adding \'title=(your preferred title)\' in {score}.')
except FileNotFoundError:
	print(f'Error: file \'{score}\' not found!')
