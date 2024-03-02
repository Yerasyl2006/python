import os

path = os.getcwd()

if os.path.exists("dir7.txt"):
  os.remove("dir7.txt")
else:
  print("The file does not exist")