def generate(a,b):
    for i in range(a,b+1):
        yield pow(i,2)



n=int(input())
m=int(input())
for i in generate(n,m):
    print(i)