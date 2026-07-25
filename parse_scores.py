from score import *
files = os.listdir('scores')
files = ['scores/' + i for i in files if re.match(r'.*\.txt', i)]
a = []
b = {}
c = [i.name for i in Path('.').iterdir() if i.is_dir() and i.name.startswith('by_')]
for i in c:
	shutil.rmtree(i)
for i in files:
	a.append(Score(i))
for i in a:
	print('Parsing:', i.score)
	i.parse()
	b.update({i.mbid : i.others})
with open('./data.json', 'w', encoding='utf-8') as f:
	json.dump(b, f, indent=4, ensure_ascii=False)