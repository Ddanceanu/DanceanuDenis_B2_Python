def gcd(a, b):
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return b


def ex1():
    gcd_result = int(input("Introdu un nr sau 0 pt a opri: \n"))
    if gcd_result == 0:
        print("Stop")
        return

    while True:
        number = int(input("Introdu un nr sau 0 pt a opri: \n"))
        if number == 0:
            break
        gcd_result = gcd(gcd_result, number)

    print(f"Cel mai mare divizor comun al numerelor este: {gcd_result}")


def ex2():
    user_input = input("Introdu un sir de caractere: ")

    vowels = "aeiouAEIOU"
    count = 0
    for i in user_input:
        if i in vowels:
            count += 1

    print(count)


def ex3():
    string1 = input("Introdu sirul mai mic: ")
    string2 = input("Introdu sirul mai mare: ")

    count = string2.count(string1)
    print(count)


def ex4():
    user_input = input("Introdu sirul: ")

    result = ""

    for i in user_input:
        if i.isupper():
            if result:
                result += "_"
            result += i.lower()
        else:
            result += i

    print(result)


def ex5():
    user_input = int(input("Introdu numarul: "))

    copieNumar = user_input
    numarInversat = 0

    while copieNumar > 0:
        c = copieNumar % 10
        numarInversat = numarInversat * 10 + c
        copieNumar = copieNumar // 10

    if user_input == numarInversat:
        print("Palindrom")
    else:
        print("Nu este")


def ex6():
    user_input = input("Introdu un text: ")
    number = ""
    for i in user_input:
        if i.isdigit():
            number += i
        elif number:
            break

    print(number)


def ex7():
    user_input = int(input("Introdu un numar: "))
    nr_binar = bin(user_input)[2:]
    print(nr_binar.count('1'))


def ex8():
    user_input = input("Introdu un text: ")
    if not user_input.strip():
        print("Textul nu conține cuvinte.")
        return

    count = 0
    in_word = False

    for i in user_input:
        if i != ' ' and not in_word:
            count += 1
            in_word = True
        elif i == ' ':
            in_word = False
    print(count)



def main():
    #ex1()
    #ex2()
    #ex3()
    #ex4()
    #ex5()
    ex6()
    #ex7()
    #ex8()


main()
