def generate(N):
    for i in range(0, N+1, 12):
        yield i

n=int(input())
even = generate(n)
print(*even, sep=",")