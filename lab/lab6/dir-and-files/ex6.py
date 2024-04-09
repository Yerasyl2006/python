import os

path = r"C:\Users\Erasyl\Desktop\python_1\lab\lab6\folder"

for i in range(65,91):
    name = os.path.re(path, chr(i) + ".txt")
    f = open(name, "a")
    