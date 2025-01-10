import os
import shutil
import time

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
            copy_file(src, dst)
        else:
            if os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy2(src, dst)
                print(f"Updated {src} -> {dst}")

    for file in files2:
        src = os.path.join(folder2, file)
        dst = os.path.join(folder1, file)

        if file not in files1:
            copy_file(src, dst)
        else: # daca fisierul exista in ambele locatii, verificam timpul
            if os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy2(src, dst)
                print(f"Updated {src} -> {dst}")



def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {path}")


def sync_folders(folder1, folder2):
    files1 = list_files(folder1)
    files2 = list_files(folder2)

    # stergerea fisierelor care nu mai exista
    for file in files1:
        if file not in files2:
            dst = os.path.join(folder1, file)
            delete_file(dst)

    for file in files2:
        if file not in files1:
            dst = os.path.join(folder2, file)
            delete_file(dst)

    files1 = list_files(folder1)
    files2 = list_files(folder2)

    # sincronizare din folder1 in 2
    for file in files1:
        src = os.path.join(folder1, file)
        dst = os.path.join(folder2, file)

        if file not in files2:
            copy_file(src, dst)
        elif os.path.exists(dst) and os.path.exists(src):
            if os.path.getmtime(src) > os.path.getmtime(dst):
                copy_file(src, dst)

    # sincronizare din folder2 in 1
    for file in files2:
        src = os.path.join(folder2, file)
        dst = os.path.join(folder1, file)

        if file not in files1:
            copy_file(src, dst)
        elif os.path.exists(dst) and os.path.exists(src):
            if os.path.getmtime(src) > os.path.getmtime(dst):
                copy_file(src, dst)

def run_sync(folder1, folder2):
    print(f"Starting continuous sync between:\n  {folder1}\n  {folder2}")
    while 1:
        sync_folders(folder1, folder2)
        time.sleep(1)