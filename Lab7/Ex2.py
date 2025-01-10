import sys
import os

# modifica denumirea fisierelor intr-o ordine

def main():
    if len(sys.argv) != 2:
        print("Format: python Ex2.py <director>")
        sys.exit(1)

    director = sys.argv[1]
    try:
        if not os.path.isdir(director):
            print("Directorul nu exista.")
            sys.exit(1)
    except PermissionError:
        print("Nu ai permisiuni.")
        sys.exit(1)
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

    try:
        files = [f for f in os.listdir(director) if os.path.isfile(os.path.join(director, f))]

        for index, filename in enumerate(files, start=1):
            new_filename = f"{index}_{filename}"
            old_filepath = os.path.join(director, filename)
            new_filepath = os.path.join(director, new_filename)

            try:
                os.rename(old_filepath, new_filepath)
                print(f"Renamed {old_filepath} to {new_filepath}")
            except Exception as e:
                print(f"Eroare la redenumirea fisierului {filename}")

    except Exception as e:
        print(f"Eroare {e}")


if __name__ == "__main__":
    main()