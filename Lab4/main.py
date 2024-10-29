def ex1(a, b):  # am doua liste, trebuie sa le transform in seturi si sa afisez intersectie, reuniune si dif
    set_a = set(a)
    set_b = set(b)
    intersection = set_a & set_b
    reunion = set_a | set_b
    dif_a_b = set_a - set_b
    dif_b_a = set_b - set_a
    return [intersection, reunion, dif_a_b, dif_b_a]


def ex2(string):  # primesc un string si returnez un dictionar cu frecventele fiecarui caracter
    frec = {}
    for i in string:
        if i in frec:
            frec[i] += 1
        else:
            frec[i] = 1

    return frec


def ex3(dictionar_1, dictionar_2):  # compar doua dictionare fara ==
    if dictionar_1.keys() != dictionar_2.keys():
        return False

    for key in dictionar_1:
        value_1 = dictionar_1[key]
        value_2 = dictionar_2[key]

        if isinstance(value_1, dict) and isinstance(value_2, dict):  # presupunem ca ambele sunt dictionare si apelam recursiv
            if not ex3(value_1, value_2):
                return False

        elif isinstance(value_1, (list, tuple)) and isinstance(value_2, (list, tuple)):  # verificare pentru liste si tupluri
            if len(value_1) != len(value_2):
                return False
            for i in range(len(value_1)):
                if isinstance(value_1[i], (dict, list, tuple, set)) or isinstance(value_2[i], (dict, list, tuple, set)):
                    if not ex3({0: value_1[i]}, {0: value_2[i]}): # daca elementul este un alt tip de date, il transform in dictionar
                        return False
                elif value_1[i] != value_2[i]:
                    return False

        elif isinstance(value_1, set) and isinstance(value_2, set):  # comparere pentru seturi
            if value_1 != value_2:
                return False

        elif value_1 != value_2:  # compararea valorilor efective
            return False

    return True


def ex4(tag, content, **attributes): # realizare sintaxa xml
    attributes_list = ' '.join(f'{key}="{value}"' for key, value in attributes.items())
    return f'<{tag} {attributes_list}>{content}</{tag}>'


def ex5(rules, dictionary):  # validarea unui dictionar dupa niste reguli
    for key in dictionary:
        if not any(rule[0] == key for rule in rules):
            return False

    for (key, prefix, middle, suffix) in rules:
        if key not in dictionary:
            return False

        value = dictionary[key]

        if not value.startswith(prefix):
            return False

        if middle not in value or value.endswith(middle) or value.endswith(middle):
            return False

        if not value.endswith(suffix):
            return False

    return True


def ex6(listt): # returnez un tuplu de numarul de elemente unice in lista si nr de duplicate
    my_set = set(listt)
    set_len = len(my_set)
    dup_len = len(listt) - set_len
    uni_len = set_len - dup_len
    return (uni_len, dup_len)


def ex7(*sets):
    result = {}

    for i, a in enumerate(sets):
        for j, b in enumerate(sets):
            if i < j:
                result[f"{a} | {b}"] = a | b
                result[f"{a} & {b}"] = a & b
                result[f"{a} - {b}"] = a - b
                result[f"{b} - {a}"] = b - a

    return result


def ex8(mapping):  # obtinere lista de la start pana la start
    result = []
    visited = set() # set pentru cheile vizitate
    curr_key = mapping["start"]

    while curr_key not in visited:
        result.append(curr_key)
        visited.add(curr_key)

        if curr_key in mapping:
            curr_key = mapping[curr_key]
        else:
            break

    return result


def ex9(*args, **kwargs):
    kwargs_list = set(kwargs.values())
    count = sum(1 for arg in args if arg in kwargs_list)
    return count


def main():
    # print(ex1([1, 2, 2, 3], [3, 4, 5]))
    # print(ex2("Ana has apples"))
    # print(ex3({"a": 1, "b": [2, 3], "c": {"d": 4}}, {"a": 1, "b": [2, 3], "c": {"d": 4}}))
    # print(ex4("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid "))
    # print(ex5({("key1", "", "inside", ""), ("key2", "start", "middle", "winter")},{"key1": "come inside, it's too cold out", "key2": "start your middle journey this winter", "key3": "this is not valid"}))
    # print(ex6([1, 2, 2, 3, 4, 5, 5, 6]))
    # print(ex7({1, 2}, {2, 3}))
    # print(ex8({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'}))
    print(ex9(1, 2, 3, 4, x=1, y=2, z=3, w=5))


if __name__ == '__main__':
    main()
