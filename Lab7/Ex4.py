import os
import sys

def count_file_extensions(director):
    extensii = {}

    try:
        for item in os.listdir(director):
            filepath = os.path.join(director, item)
            if os.path.isfile(filepath):
                nume, extensie = os.path.splitext(item)

                if extensie:
                    if extensie in extensii:
                        extensii[extensie] += 1
                    else:
                        extensii[extensie] = 1
    except PermissionError:
        print("Permission denied")
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)

    if extensii:
        for extensie, numar in extensii.items():
            print(f"{extensie}: {numar}")
    else:
        print("No file found")


def main():
    if len(sys.argv) != 2:
        print("Format: python Ex3.py <director>")
        sys.exit(1)

    director = sys.argv[1]
    if not os.path.isdir(director):
        print("Director doesn't exist")
        sys.exit(1)
    count_file_extensions(director)

if __name__ == "__main__":
    main()