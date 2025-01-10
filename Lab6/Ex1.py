import math

class Shape:
    def perimeter(self):
        return None

    def area(self):
        return None


class Rectangle(Shape):
    def __init__(self, lungime, latime):
        self.lungime = lungime
        self.latime = latime

    def perimeter(self):
        return self.lungime * 2 + 2 * self.latime

    def area(self):
        return self.lungime * self.latime


class Square(Shape):
    def __init__(self, lungime):
        self.lungime = lungime

    def perimeter(self):
        return self.lungime * 4

    def area(self):
        return self.lungime * self.lungime


class Circle(Shape):
    def __init__(self, raza):
        self.raza = raza

    def perimeter(self):
        return 2 * self.raza * math.pi

    def area(self):
        return self.raza * self.raza * math.pi


class Triangle(Shape):
    def __init__(self, lat_a, lat_b, lat_c):
        self.lat_a = lat_a
        self.lat_b = lat_b
        self.lat_c = lat_c

    def perimeter(self):
        return self.lat_a + self.lat_b + self.lat_c

    def area(self):
        # semiperimetrul
        s = (self.lat_a + self.lat_b + self.lat_c) / 2
        return math.sqrt(s * (s - self.lat_a) * (s - self.lat_b) * (s - self.lat_c))

def main():
    my_rectangle = Rectangle(10, 20)
    print(f"Perimetrul: {my_rectangle.perimeter()}")
    print(f"Area: {my_rectangle.area()}\n")

    my_square = Square(10)
    print(f"Perimetrul: {my_square.perimeter()}")
    print(f"Area: {my_square.area()}\n")

    my_circle = Circle(5)
    print(f"Perimetrul: {my_circle.perimeter()}")
    print(f"Area: {my_circle.area()}\n")

    my_triangle = Triangle(3, 4, 5)
    print(f"Perimetrul: {my_triangle.perimeter()}")
    print(f"Area: {my_triangle.area()}\n")

if __name__ == '__main__':
    main()