def generate(a):
    for i in range(a,-1,-1):
        yield i


n=int(input())
for i in generate(n):
    print(i)