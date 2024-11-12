import sys
import os

#dimensiunea fisierelor

def Ex3(director):
    total_size = 0

    try:
        for dirpath, dirnames, filenames in os.walk(director):
            for f in filenames:
                fp = os.path.join(dirpath, f)

                try:
                    total_size += os.path.getsize(fp)
                except FileNotFoundError:
                    print("Fisierul nu a fost gasit.")
                except PermissionError:
                    print("Nu ai permisiuni pentru acest foisier")
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)
        sys.exit(1)
    return total_size

def main():
    if len(sys.argv) != 2:
        print("Format: python Ex3.py <director>")
        sys.exit(1)

    director = sys.argv[1]
    if not os.path.isdir(director):
        print("Director doesn't exist")
        sys.exit(1)

    print(f"Total size of the directory: {Ex3(director)} bytes")


if __name__ == "__main__":
    main()