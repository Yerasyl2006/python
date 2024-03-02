def multiply(numbers):
    total = 1
    for x in numbers:
        total *= x
    return total

numbers = list(map(int, input().split()))
result = multiply(numbers)
print(result)