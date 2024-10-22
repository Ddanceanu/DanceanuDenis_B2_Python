from itertools import zip_longest
from collections import defaultdict

def ex1(n):
    fibonacci = []
    a = 1
    b = 1
    fibonacci.append(a)
    fibonacci.append(b)
    for i in range(n - 2):
        c = a + b
        b = a
        a = c
        fibonacci.append(c)

    return fibonacci


def ex2(numbers):
    prime_numbers = []
    for number in numbers:
        if number >= 2:
            prime = True
            for i in range(2, number - 1):
                if number % i == 0:
                    prime = False
            if prime is True:
                prime_numbers.append(number)

    return prime_numbers


def ex3(a, b):
    intersection = [item for item in a if item in b]

    reunion = a.copy()
    for i in b:
        if i not in intersection:
            reunion.append(i)

    a_minus_b = a.copy()
    for i in intersection:
        a_minus_b.remove(i)

    b_minus_a = b.copy()
    for i in intersection:
        b_minus_a.remove(i)

    return intersection, reunion, a_minus_b, b_minus_a


def ex4(notes, moves, start_position):
    song = [notes[start_position]]
    position = start_position
    for move in moves:
        position = (position + move) % len(notes)
        song.append(notes[position])

    return song


def ex5(matrix=[
    [2, 5, 9],
    [12, 32, 594],
    [12, 65, 3]
]):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i > j:
                matrix[i][j] = 0

    return matrix


def ex6(x, *lists):
    new_list = []
    for list in lists:
        new_list.extend(list)

    frequency = {} # facem un dictionar pentru a retine fiecare aparitie

    for number in new_list:
        if number in frequency:
            frequency[number] += 1
        else:
            frequency[number] = 1

    result = []
    for number in new_list:
        if frequency[number] == x:
            if (number not in result): # ca sa nu imi apara de mai multe ori numerele (ele au frecventa mai mare de 1)
                result.append(number)

    return result


def is_palindrom(number):
    copy_number = number
    new_number = 0
    while copy_number != 0:
        c = copy_number % 10
        copy_number = copy_number // 10
        new_number = new_number * 10 + c

    if new_number == number:
        return True
    return False


def ex7(numbers):
    result = ()
    count = 0
    greatest = numbers[0]
    for number in numbers:
        if is_palindrom(number) == True:
            count += 1
    if (count == 0):
        result = (0, "none")
    else:
        for number in numbers:
            if is_palindrom(number) == True and number > greatest:
                greatest = number
    result = (count, greatest)
    return result


def ex8(x=1, str_list=[], flag=True):
    result = []

    # parcurg fiecare sir
    for string in str_list:
        filtered_chars = []  # aici voi pune caracterele filtrate

        for char in string:
            ascii_value = ord(char)  # codul ascii

            if flag:
                if ascii_value % x == 0:
                    filtered_chars.append(char)
            else:
                if ascii_value % x != 0:
                    filtered_chars.append(char)

        result.append(filtered_chars)

    return result


def ex9(matrix = [[1, 2, 3, 2, 1, 1], [2, 4, 4, 3, 7, 2], [5, 5, 2, 5, 6, 4], [6, 6, 7, 6, 7, 5]]):
    result = []

    for row in range(1, len(matrix)):
        for col in range(len(matrix[row])):
            # verific daca exista un spectator in randurile anterioare mai inalt
            can_see = True
            for prev_row in range(row):
                if matrix[prev_row][col] >= matrix[row][col]:
                    can_see = False
                    break

            if not can_see:
                result.append((row, col))

    return result


def ex10(*lists):
    # zip_longest combina elementele de pe aceleasi pozitii dar inlocuieste cu None pe cele lipsa
    return list(zip_longest(*lists, fillvalue=None))


def ex11(tuples_list):
    return sorted(tuples_list, key=lambda x: x[1][2])


def ex12(words):
    rhyme_groups = defaultdict(list)  # dictionar care contine listele

    for word in words:
        if len(word) >= 2:
            rhyme_key = word[-2:]
        else:
            rhyme_key = word

        rhyme_groups[rhyme_key].append(word)

    return list(rhyme_groups.values())


def main():
    # print(ex1(10))
    # print(ex2([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
    # print(ex3([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [1, 3, 5, 7, 9]))
    # print(ex4(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))
    # print(ex5())
    # print(ex6(2, [1, 2, 3], [2, 3, 4], [4, 5, 6], [4, 1, "test"]))
    # print(ex7([121, 456, 789, 10, 23, 11, 5, 10, 54]))
    # print(ex8(2, ["test", "hello", "lab002"], False))
    # print(ex9())
    # print(ex10([1, 2, 3], [5, 6, 7], ["a", "b", "c", "d"]))
    # print(ex11([('abc', 'bcd'), ('abc', 'zza')]))
    # print(ex12(['ana', 'banana', 'carte', 'arme', 'parte']))

main()
