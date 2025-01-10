import os


def list_files_and_contents(path):
    entries = os.listdir(path)

    for entry in entries:
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            list_files_and_contents(full_path)
        elif os.path.isfile(full_path):
            print(full_path)

        try:
            with open(full_path, 'r') as file1:
                print(file1.read())

        except FileNotFoundError:
            print('File not found')