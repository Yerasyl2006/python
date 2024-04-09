class Shape():
    def __init__(self, length):
        self.length = length
    def area(self):
        print(0)

class Square(Shape):
    def area(self):
        print(self.length * self.length)

a = int(input())
b = Shape(a)
b.area()
b = Square(a)
b.area()