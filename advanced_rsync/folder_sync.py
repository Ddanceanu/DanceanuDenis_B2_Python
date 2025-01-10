import os
import shutil

def list_files(path):
    file_paths = []

    for root, dirs, files in os.walk(path):
        for filename in files:
            full_path = os.path.join(root, filename)
            # facem full_path sa fie cale relativa
            relative_path = full_path.replace(path, "").lstrip("\\/")
            file_paths.append(relative_path)

    return file_paths


def initial_sync(folder1, folder2):
    files1 = list_files(folder1)
    files2 = list_files(folder2)

    for file in files1:
        src = os.path.join(folder1, file)
        dst = os.path.join(folder2, file)

        if file not in files2: # daca un fisier nu exista in locatia 2
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied {src} -> {dst}")

    for file in files2:
        src = os.path.join(folder2, file)
        dst = os.path.join(folder1, file)

        if file not in files1:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"Copied {src} -> {dst}")
        else: # daca fisierul exista in ambele locatii, verificam timpul
            if os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy2(src, dst)
                print(f"Updated {src} -> {dst}")