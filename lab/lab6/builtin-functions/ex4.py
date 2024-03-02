from time import sleep
from math import sqrt

n = int(input("Sample input:\n"))
t = int(input())
a=sleep(t/1000)
result = sqrt(n)
print(f"Square root of {n} after {t} milliseconds is {result}")