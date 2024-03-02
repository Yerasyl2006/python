import os

path = r'C:\Users\Erasyl\Desktop\python_1\lab\lab6\dir-and-files\text.txt'

with open(path, 'r') as f:
	lines = len(f.readlines())
	print(lines)