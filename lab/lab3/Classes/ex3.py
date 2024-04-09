class Shape():
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Rectangle(Shape):
    def area(self):
        print(self.length * self.width)

x = int(input())
y = int(input())
s = Rectangle(x, y)
s.area()