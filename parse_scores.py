from score import *
files = os.listdir('scores')
files = ['scores/' + i for i in files if re.match(r'.*\.txt', i)]
a = []
for i in files:
	a.append(Score(i))
	print('Parsing:', i)
	a[len(a) - 1].parse()