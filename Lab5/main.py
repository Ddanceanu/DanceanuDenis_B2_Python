class Stack:
    def __init__(self):
        self.items = []  # folosim o lista

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop()
        return None

    def peek(self):
        if self.items:
            return self.items[-1]
        return None

    def print_stack(self):
        for item in self.items:
            print(item)


class Queue:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.items:
            return self.items.pop(0)  # primul element
        return None

    def peek(self):
        if self.items:
            return self.items[0]  # primul element fara eliminare
        return None

    def print_queue(self):
        for item in self.items:
            print(item)


class Matrix:
    def __init__(self, rows, cols, data = None):
        self.rows = rows
        self.cols = cols
        # punem 0 peste tot in matrice
        self.data = data if data else [[0 for _ in range(cols)] for _ in range(rows)]

    def get(self, row, col):  # elementul de la pozitia [row][col]
        return self.data[row][col]

    def set(self, row, col, value):
        self.data[row][col] = value

    def transpose(self):
        transposed_data = []
        for i in range(self.cols):
            new_row = []
            for j in range(self.rows):
                new_row.append(self.data[j][i])
            transposed_data.append(new_row)

        return Matrix(self.cols, self.rows, data=transposed_data)

    def multiply(self, other):
        if self.cols != other.rows:
            return None  # daca matricile nu se potrivesc

        result = Matrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                result.data[i][j] = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))

        return result

    def apply(self, func):
        for i in range(self.rows):
            for j in range(self.cols):
                self.data[i][j] = func(self.data[i][j])

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])


def main():
    print("Stack:")
    my_stack = Stack()
    my_stack.push(10)
    my_stack.push(20)
    my_stack.push(30)
    my_stack.pop()
    my_stack.print_stack()
    print(my_stack.peek())

    print()
    print("Queue:")

    my_queue = Queue()
    my_queue.push(10)
    my_queue.push(20)
    my_queue.push(30)
    my_queue.print_queue()
    my_queue.pop()
    print()
    my_queue.print_queue()
    print()
    print(my_queue.peek())

    print()
    print("Matrix:")
    matrix = Matrix(3, 3)  # matrice de 3 x 3
    matrix.set(0, 0, 1)
    matrix.set(0, 1, 2)
    matrix.set(0, 2, 3)
    matrix.set(1, 0, 4)
    matrix.set(1, 1, 5)
    matrix.set(1, 2, 6)
    matrix.set(2, 0, 7)
    matrix.set(2, 1, 8)
    matrix.set(2, 2, 9)

    print("Matricea initiala:")
    print(matrix)
    print()
    print(matrix.transpose())

    matrix.apply(lambda x: x * 2)
    print("\nDupa inmultirea fiecarui elemnt cu 2:")
    print(matrix)

if __name__ == '__main__':
    main()
