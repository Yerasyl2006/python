import os

list = ["alma", "almurt", "orik", "zhuzim"]

with open("dir.txt", "w") as file:
    for i in list:
        file.write(i + "\n")