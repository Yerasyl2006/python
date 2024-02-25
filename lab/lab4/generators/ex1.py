def generate(a):
    for i in range(1,a+1):
        yield pow(i,2)


n=int(input())
for i in generate(n):
    print(i)