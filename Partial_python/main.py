import sys
import os

def Words(path_to_file):
    try:
        with open(path_to_file, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print('File not found')
        sys.exit(1)
    except Exception as e:
        print(f"A aparut urmatoarea eroare {e}")
        sys.exit(1)

    words = content.split(" ,.!?")
    my_list = []
    for word in words:
        my_list.append(word)

    my_set = set(my_list)
    freq = {}

    for word in my_set:
        freq[word] = len(word)
    for word in freq:
        print(f"{word} - {freq[word]}")


def main():
    if len(sys.argv) != 2:
        print("Numar gresit de parametri.")
        sys.exit(1)

    file_path = sys.argv[1]
    if not (os.path.isfile(file_path)):
        print("Parametrul furnizat nu reprezinta calea corecta catre un fisier.")
        sys.exit(1)




if __name__ == '__main__':
    main()