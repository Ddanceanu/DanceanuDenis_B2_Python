import os
import shutil
import time

def list_files(path):  # creeaza o lista cu toate fisierele (cai relative) dintr-un director
    file_paths = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = full_path.replace(path, "").lstrip("\\/")
            file_paths.append(relative_path)
    return file_paths

def copy_file(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {path}")

def initial_sync(folder1, folder2):  # sincronizare initiala intre fisiere
    global global_file_paths1, global_file_paths2  # salvam toate fisierele existente initial
    files1 = list_files(folder1)
    files2 = list_files(folder2)
    for file in files1:
        src = os.path.join(folder1, file)
        dst = os.path.join(folder2, file)
        if file not in files2:
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
        else:
            if os.path.getmtime(src) > os.path.getmtime(dst):
                shutil.copy2(src, dst)
                print(f"Updated {src} -> {dst}")

    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)

def sync_folders(folder1, folder2):
    global global_file_paths1, global_file_paths2

    # verificam daca s-a sters un fisier din folder1
    for file in global_file_paths1:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        if not os.path.exists(file_path1):  # fisier lipsa folder1
            if os.path.exists(file_path2):  # stergem din folder2
                delete_file(file_path2)

    # verificam daca s-a sters un fisier din folder2
    for file in global_file_paths2:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        if not os.path.exists(file_path2):  # fisier lipsa folder2
            if os.path.exists(file_path1):  # stergem din folder1
                delete_file(file_path1)

    # actualizam listele cu fisierele
    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)

    # copiere fisiere lipsa din folder1 in folder2
    for file in global_file_paths1:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        if not os.path.exists(file_path2):
            copy_file(file_path1, file_path2)

    # copiere fisiere lipsa din folder2 in folder1
    for file in global_file_paths2:
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        if not os.path.exists(file_path1):
            copy_file(file_path2, file_path1)

    # actualizeaza fisierele updatate intr-un anumit folder
    for file in set(global_file_paths1).intersection(global_file_paths2):
        file_path1 = os.path.join(folder1, file)
        file_path2 = os.path.join(folder2, file)
        if os.path.exists(file_path1) and os.path.exists(file_path2):
            mtime1 = os.path.getmtime(file_path1)
            mtime2 = os.path.getmtime(file_path2)
            if mtime1 > mtime2:  # Fișierul din folder1 este mai nou
                shutil.copy2(file_path1, file_path2)
                print(f"Updated {file_path1} -> {file_path2}")
            elif mtime2 > mtime1:  # Fișierul din folder2 este mai nou
                shutil.copy2(file_path2, file_path1)
                print(f"Updated {file_path2} -> {file_path1}")

    # actualizare liste globale
    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)

def run_sync(folder1, folder2):
    initial_sync(folder1, folder2)
    print(f"Starting continuous sync between:\n  {folder1}\n  {folder2}")
    while True:
        sync_folders(folder1, folder2)
        time.sleep(1)
