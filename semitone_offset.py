import math
import sys
import getopt
notes = ['1', 
         '#1',
         '2',
         '#2',
         '3',
         '4',
         '#4',
         '5',
         '#5',
         '6',
         '#6',
         '7' ]
offset = {'#' : 1,
          'b' : -1,
          '\'' : 12,
          ',' : -12}
def format_note(a, o):
	b = ''
	for i in a:
		if i in ',\'':
			b += i
	d = ''
	for i in a:
		if i in '#b':
			d += i
	e = sum([offset[i] for i in b + d]) + o
	f = ''
	g = ''
	h = ''
	for i in a:
		if i in '1234567':
			if not f:
				f = i
			else:
				print('Warning: note is already ' + f + '. Pass.')
		if i in '\\.':
			h = h + i
		if i in 'sqdh':
			g = g + i
	return offset_note(f, e) + g + h
def offset_note(a, n):
	b = notes.index(a) + n
	c = math.floor(b / 12)
	c = c * '\'' if c > 0 else (-c) * ','
	return c + notes[b % 12]
def is_note(a):
	b = False
	for i in a:
		if not i in 'sqdh\\.#b,\'1234567':
			return False
		if i in '1234567':
			b = True
	return b
def main(argv):
	try:
		infile = ''
		outfile = ''
		offsetv = 0
		d, e = getopt.getopt(argv, 'i:o:', ['input=', 'output=', 'offset='])
		for i, j in d:
			if i in ['-i', '--input']:
				infile = j
			if i in ['-o', '--output']:
				outfile = j
			if i == '--offset':
				offsetv = int(j)
		out = ''
		if not outfile:
			f = infile.split('.')
			outfile = '.'.join(f[:-1]) + '_semitone' + f'{offsetv:+}' + '.' + f[-1]
		with open(infile, 'r', encoding='utf-8') as f:
			raw = f.read().split(' ')
		print((' ').join([(format_note(i, offsetv) if is_note(i) else i) for i in raw]), file=open(outfile, 'w', encoding='utf-8') if outfile else sys.stdout)
	except FileNotFoundError:
		print('Usage:')
		print('python semitone_offset_py -i [input file] -o [output file] --offset=[offset, default 0]')
if  __name__ == '__main__':
	main(sys.argv[1:])
