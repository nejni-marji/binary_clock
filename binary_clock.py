#!/usr/bin/env python3
import datetime
from pprint import pprint

ASCII_ESC = '\x1b'
ANSI_CODE = '%s[%%sm' % ASCII_ESC
ANSI_RGB_FG = ANSI_CODE % '38;2;%i;%i;%i'
ANSI_RGB_BG = ANSI_CODE % '48;2;%i;%i;%i'
ANSI_END = ANSI_CODE % '0'

WIDTH_MOD = 4
HEIGHT_MOD = 2
COL_SEP_MOD = 2

DEBUG = False



def get_table():
	curr = datetime.datetime.now()
	# demo time
	# curr = datetime.datetime.strptime('2023-03-22 13:48:34', '%Y-%m-%d %H:%M:%S')
	curr = datetime.datetime.strptime('2023-03-22 23:59:59', '%Y-%m-%d %H:%M:%S')

	hms = [curr.hour, curr.minute, curr.second]
	hms_bin = [bin(i)[2:].zfill(8) for i in hms]

	# demo hmsb
	# hms_bin = ['h1234567', 'mABCDEFG', 'sabcdefg']

	hms_str = ''.join(hms_bin)

	table = []
	for i in range(3+1):
		row = list(hms_str[i::4])
		row = [int(i) for i in row]
		table.append(row)

	return table
	pprint(table)


def hex_to_rgb(x):
	if x[0] == '#':
		x = x[1:]
	if not len(x) == 6:
		raise ValueError
	arr_x = [x[0:2], x[2:4], x[4:6]]
	rgb = [int(i, 16) for i in arr_x]
	return rgb

def hex_to_ansi(x, is_bg=False):
	rgb = hex_to_rgb(x)
	fmt = [ANSI_RGB_FG, ANSI_RGB_BG][is_bg]
	if DEBUG:
		print([fmt])
	ansi = fmt % tuple(rgb)
	return ansi


def draw_once(table, on, off, grid):
	ansi = []
	for i in [on, off, grid]:
		if DEBUG:
			print(i)
			print(hex_to_rgb(i))
			print(hex_to_ansi(i, is_bg=True) + 'TEST' + ANSI_END)
		ansi.append(hex_to_ansi(i, is_bg=True))

	height = len(table)
	width = len(table[0])

	def row_sep():
		print(ansi[2] + ' ' * (width*(COL_SEP_MOD+WIDTH_MOD)+COL_SEP_MOD))

	def col_sep():
		print(ansi[2] + ' ' * COL_SEP_MOD, end='')

	for row in table:
		# print separator above row
		row_sep()
		# bonus rows account for HEIGHT_MOD
		for bonus_row in range(HEIGHT_MOD):
			for item in row:
				# print separator before item
				col_sep()
				# clever trick to reference index
				print(ansi[not item], end='')
				# debug setting
				if DEBUG:
					print(str(item) * WIDTH_MOD, end='')
				else:
					# account for WIDTH_MOD
					print(' ' * WIDTH_MOD, end='')
			# print final separator at end of row
			col_sep()
			# go to next row
			print()
	# print final separator at end of table
	row_sep()
	# end colors
	print(ANSI_END, end='')



def main():
	table = get_table()
	if DEBUG:
		pprint(table)

	# draw_once(table, '#FF8CDA', '#D7E7ED', '#EFB1E2')
	draw_once(table, '#FF8CDA', '#FFFFFF', '#EFB1E2')


if __name__ == '__main__':
	main()