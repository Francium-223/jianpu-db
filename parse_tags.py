import json
with open('tag_implications.json', 'r', encoding='utf-8') as f1:
	imply = json.load(f1)
with open('tag_equality.json', 'r', encoding='utf-8') as f2:
	equal = json.load(f2)
def findequals(a):
	global equal
	for i in equal:
		for j in i:
			if j == a:
				c = []
				for k in i:
					if not k == j:
						c.append(k)
				return c
	return []
'''
dest = Path(filename)
Path(filename).parent.mkdir(parents=True, exist_ok=True)
dest.unlink(missing_ok=True)
dest.symlink_to(os.path.relpath(self.score, start=filename))
'''
for k, v in imply.items():