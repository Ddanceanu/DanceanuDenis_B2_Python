import sys
import os

# afiseaza continutul fisierelor cu o anumita extensie dintr-un director

def main():
    if len(sys.argv) != 3:
        print("Format: python Ex1.py <director> <extensie>")
        sys.exit(1)

    director = sys.argv[1]
    extensie = sys.argv[2]

    # verificare existenta director
    if not os.path.isdir(director):
        print("Director " + director + " is not a directory")
        sys.exit(1)

    # verificare extensie
    if not extensie.startswith("."):
        print("Extensie " + extensie + " nu este extensie")
        sys.exit(1)

    try:
        files_fount = False
        for filename in os.listdir(director):
            if filename.endswith(extensie):
                files_found = True
                file_path = os.path.join(director, filename)

                try:
                    with open(file_path, "r") as file:
                        print(filename)
                        print(file.read())
                        print()
                except Exception as e:
                    print(f"Eroare la citirea fisierului {filename}")
        if not files_found:
            print("Nu s-au gasit fisiere.")
    except Exception as e:
        print(f"Eroare {e}")


if __name__ == '__main__':
    main()