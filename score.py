import sys
import json
import re
import shutil
with open('tag_imply.json', 'r', encoding='utf-8') as f1:
	imply = json.load(f1)
with open('tag_equal.json', 'r', encoding='utf-8') as f2:
	equal = json.load(f2) 
class NotMBIDError(Exception):
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
	if c:
		return c
	return b
def safe_minus(a, b):
	c = []
	for i in a:
		if not i in b:
			c.append(i)
	return c
def get_meta_lines(s):
	d = []
	for i in s:
		d.append(i)
		if i.replace(' ', '').startswith('%--'):
			return d
	return []
def goto_node(p):
	if p == []:
		return imply
	a = imply
	for i in p:
		a = a[i]
	return a
class Score():
	def __init__(self, score):
		self.score = score
		self.tag = []
		self.usertag = []
		self.origtag = []
		self.nottag = []
		self.orignottag = []
		self.mbid = ''
		self.title = ''
		self.type = 'work'
		self.others = {'tag': [], 'usertag': []}
		self.comments = []
	def find_tag(self, n):
		if n.startswith('!'):
			find_nottag(n.lstrip('!'))
			return
		for i in equal:
			if n in i:
				self.tag = safe_add(self.tag, i)
				if n in self.origtag:
					self.origtag = safe_add(self.origtag, i)
		self.tag = safe_add(self.tag, [n])
		for i in self.tag:
			self.where_imply(i, [])
	def find_nottag(self, n):
		for i in equal:
			if n in i:
				self.nottag = safe_add(self.nottag, i)
				if n in self.orignottag:
					self.orignottag = safe_add(self.orignottag, i)
		self.nottag = safe_add(self.nottag, [n])
		for i in self.nottag:
			self.where_not_imply(i, [])
	def where_imply(self, n, p):
		for k, v in goto_node(p).items():
			if k == n and set(self.origtag) & set(p + [k]):
				self.tag = safe_add(self.tag, p)
			self.where_imply(n, p + [k])
	def where_not_imply(n, p):
		for k, v in goto_node(p).items():
			if k == n and set(self.orignottag) & set(p):
				self.nottag = safe_add(self.nottag, p)
			self.where_not_imply(n, p + [k])
	def prioritize_title_and_tag(self):
		b = {}
		b['file'] = self.others['file']
		b['type'] = self.others['type']
		b['title'] = self.others['title']
		b['usertag'] = self.others['usertag']
		b['tag'] = self.others['tag']
		for i in self.others.keys():
			if not i in ['file', 'title', 'tag', 'usertag', 'type']:
				b[i] = self.others[i]
		self.others = b
	def makebuf(self):
		try:
			with open(self.score, 'r', encoding='utf-8') as f:
				raw = f.readlines()
			for i in get_meta_lines(raw):
				i = i.rstrip('\n')
				if i.replace(' ', '').startswith('%--'):
					continue
				if i.replace(' ', '').lower().startswith('mbid='):
					self.mbid = i[i.find('=') + 1:].strip(' ')
					if not re.match('[0123456789abcdef]{8}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{4}-[0123456789abcdef]{12}', self.mbid) and False:
						raise NotMBIDError
					continue
				if i.replace(' ', '').startswith('usertag='):
					for j in re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')):
						self.usertag = safe_add(self.usertag, [j])
						self.origtag = safe_add(self.origtag, [j])
						self.find_tag(j.strip(' '))
					continue
				if i.replace(' ', '').startswith('title='):
					self.title = i[i.find('=') + 1:].strip(' ')
					continue
				if i.replace(' ', '').startswith('type='):
					worktypes = ['work', 'recording']
					if i[i.find('=') + 1:].strip(' ').lower() in worktypes:
						self.type = i[i.find('=') + 1:].strip(' ').lower()
					else:
						print(f'Warning: invalid type {i[i.find('=') + 1:].strip(' ')}. Changed to \'work\'.')
						print(f'Valid types are: {', '.join(worktypes)}.')
					continue
				if '=' in i:
					t = i[:i.find('=')].strip(' ')
					if t in self.others.keys():
						self.others[t] = safe_add(self.others[t], re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')))
					else:
						self.others[t] = safe_add([], re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')))
					continue
				if i == '%' + self.score.split('/')[-1]:
					continue
				if i.startswith('%'):
					comments.append(i.rstrip('\n'))
					continue
				for j in re.split(r'[,|，|、]', i[i.find('=') + 1:].strip(' ')):
					self.usertag = safe_add(self.usertag, [j])
					self.origtag = safe_add(self.origtag, [j])
					find_tag(j.strip(' '))
			maybetag = safe_minus(self.tag, self.nottag)
			self.others['usertag'] = []
			for i in self.usertag:
				self.others['usertag'] = safe_add(self.others['usertag'], [i])
			for i in maybetag:
				self.others['tag'] = safe_add(self.others['tag'], [i])
				for j in equal:
					if i in j:
						self.others['tag'] = safe_add(self.others['tag'], j)
			with open(('.').join(self.score.split('.')[:-1]) + '_buf.txt', 'w', encoding='utf-8') as f:
				print('%' + self.score.split('/')[-1], file=f)
				for i in self.comments:
					print(i.rstrip('\n'), file=f)
				print('MBID=' + self.mbid, file=f)
				print('title=' + self.title, file=f)
				print('type=' + self.type, file=f)
				for i in self.others.keys():
					print(i + '=' + (',').join(self.others[i]), file=f)
				self.others['title'] = self.title
				self.others['type'] = self.type
				self.others['file'] = self.score.split('/')[-1]
				d = False
				for i in raw:
					if i.replace(' ', '').startswith('%--'):
						d = True
					if d:
						print(i.rstrip('\n'), file=f)
				if not ('').join(raw).replace('\n', '').replace('\r', '').lower().endswith('%end'):
					print('%END', end='', file=f)
			with open(('.').join(self.score.split('.')[:-1]) + '_buf.json', 'w', encoding='utf-8') as f:
				self.prioritize_title_and_tag()
				json.dump({self.mbid : self.others}, f, indent=4, ensure_ascii=False)
			return 0
		except NotMBIDError:
			print('Error: no MBID!')
			print(f'Try adding \'MBID=(what you\'ve found in your address bar after \'https://musicbrainz.org/work/\'.)\'.)\' in {self.score}.')
			raise
		except NotTitleError:
			print(f'Error: no title!')
			print(f'Try adding \'title=(your preferred title)\' in {self.score}.')
			raise
		except FileNotFoundError:
			print(f'Error: file \'{self.score}\' not found!')
			raise
	def movebuf(self):
		try:
			prefix = ('.').join(self.score.split('.')[:-1])
			with open(prefix + '_buf.txt', 'r', encoding='utf-8') as f:
				raw = f.read()
				if not raw.replace('\n', '').replace('\r', '').lower().endswith('%end'):
					raise BadBufError
			shutil.move(prefix + '_buf.txt', prefix + '.txt')
			shutil.move(prefix + '_buf.json', prefix + '.json')
		except FileNotFoundError:
			print(f'Error: file \'{self.score}\' not found!')
			raise
		except BadBufError:
			print(f'Bad buf: {prefix + '_buf.txt'}!')
	def parse(self):
		self.makebuf()
		self.movebuf()
