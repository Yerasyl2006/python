def isPrime(num):
    if(num == 1):
        return False
    for i in range(2, num):
        if(num % i == 0):
            return False
    return True

class List():
    def __init__(self, a):
        self.a = a
    def filtering(self):
        return list(filter(lambda num : isPrime(num), self.a))

myList = List([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
print(myList.filtering())