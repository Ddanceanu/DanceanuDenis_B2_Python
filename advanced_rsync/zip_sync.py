import os
import shutil
import time
import zipfile

global_file_paths1 = []
global_file_paths2 = []


def list_files(path):
    """
    Creeaza o lista cu toate caile relative.
    Dacă 'path' este calea către fișierul zip (folder1), citește conținutul zip-ului.
    Daca 'path' este calea catre folder1 (zip), citim continutul.
    Dacă 'path' este folderul (folder2), citim continutul.

    Argumente:
        path (str): Calea catre zip/fodler.

    Returnează:
        list: lista xu toate caile relative.
    """
    # verificare zip/folder
    if os.path.isfile(path) and zipfile.is_zipfile(path):
        file_paths = []
        with zipfile.ZipFile(path, 'r') as zf:
            file_paths = [f for f in zf.namelist() if not f.endswith('/')]  # excludem folderele
        return file_paths
    else:
        file_paths = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                full_path = os.path.join(root, filename)
                relative_path = full_path.replace(path, "").lstrip("\\/")
                file_paths.append(relative_path)
        return file_paths


def copy_file(src, dst):
    """
    Copiaza un fisier intre locatii.
    Daca sursa este un zip, extrage fisierul si il copiaza in folder.
    Daca destinatia este un fisier zip, adauga fisierul in arhiva.

    Argumente:
        src (str): calea catre src
        dst (str): calea catre dst

    Actiuni:
        - ia fisierele din zip si le da copy in folder
        - adauga fisiere din folder in zip
        - copiaza fisierele intre doua foldere daca este cazul
    """

    # Sursa e zip -> dest e folder
    if os.path.isfile(get_zip_path()) and src.startswith(get_zip_path()):
        rel_path = src.replace(get_zip_path(), "").lstrip("\\/")
        with zipfile.ZipFile(get_zip_path(), 'r') as zf:
            try:
                zinfo = zf.getinfo(rel_path)
            except KeyError:
                print(f"[WARN] {rel_path} nu exista in zip!")
                return

            # cream un folder temporar si il extragem aici
            temp_extract = os.path.join(get_temp_dir(), rel_path)
            os.makedirs(os.path.dirname(temp_extract), exist_ok=True)
            zf.extract(rel_path, os.path.dirname(temp_extract))

            # copiem din folder temporar in dst
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(temp_extract, dst)

            # setam mtime la fel ca pe disc
            import datetime, time
            z_dt = datetime.datetime(*zinfo.date_time)
            zip_mtime = time.mktime(z_dt.timetuple())
            os.utime(dst, (zip_mtime, zip_mtime))


    # din zip in folder
    elif os.path.isfile(get_zip_path()) and dst.startswith(get_zip_path()):
        rel_path = dst.replace(get_zip_path(), "").lstrip("\\/")
        with zipfile.ZipFile(get_zip_path(), 'r') as old_zip:
            old_files = old_zip.namelist()
            temp_zip_path = get_temp_zip_path()

            with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                # copiem fisierele existente
                for item in old_files:
                    if item != rel_path:  # nu suprascriem fisierul
                        old_info = old_zip.getinfo(item)
                        data = old_zip.read(item)
                        zinfo_old = zipfile.ZipInfo(item)
                        zinfo_old.date_time = old_info.date_time
                        new_zip.writestr(zinfo_old, data)

                # adaugam fisierul, actualizand mtime
                import datetime, time
                mtime = os.path.getmtime(src)
                dt = datetime.datetime.fromtimestamp(mtime)
                zinfo_new = zipfile.ZipInfo(rel_path)
                zinfo_new.date_time = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

                with open(src, 'rb') as f:
                    data = f.read()
                new_zip.writestr(zinfo_new, data)

        shutil.move(temp_zip_path, get_zip_path())

    else:
        # sursa si dst pe disc ambele
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)


def delete_file(path):
    """
    Sterge un fisier specificat prin path.
    Daca fisierul este zip, reconstruieste toata arhiva exceptand acel fisier.
    Daca fisierul este pe disc, il stergem.

    Argumente:
        path (str): calea catre fisierul de sters.

    Acțiuni:
        - sterge fisierul din zip/disc
    """
    # Verificăm dacă ținta este în zip
    if os.path.isfile(get_zip_path()) and path.startswith(get_zip_path()):
        rel_path = path.replace(get_zip_path(), "").lstrip("\\/")
        with zipfile.ZipFile(get_zip_path(), 'r') as old_zip:
            old_files = old_zip.namelist()
            if rel_path not in old_files:
                # daca fisierul nu exista
                return
            temp_zip_path = get_temp_zip_path()
            with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                for item in old_files:
                    if item != rel_path:  # copy la tot mai putin acel fisier
                        data = old_zip.read(item)
                        new_zip.writestr(item, data)
        shutil.move(temp_zip_path, get_zip_path())
        print(f"Deleted (from ZIP) {path}")
    else:
        # este pe disc, stergem cu os.remove
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")


def initial_sync(folder1, folder2):
    """
     Sincronizeaza initial continutul dintre o arhiva ZIP si un folder.
    Copiaza fisierele lipsa si actualizeaza fisierele mai vechi cu versiuni mai noi.

    Argumente:
        folder1 (str): Calea catre fisierul ZIP.
        folder2 (str): Calea catre folderul sincronizat.

    Actiuni:
        - Copiaza fisierele lipsa din ZIP in folder si invers.
        - Actualizeaza fisierele existente, pastrand cea mai noua versiune.
        - Actualizeaza listele globale cu fisierele sincronizate.
    """
    global global_file_paths1, global_file_paths2
    # actualizam caile globale
    set_paths(folder1, folder2)

    files1 = list_files(folder1)  # continut zip
    files2 = list_files(folder2)  # continut folder

    # copiere de pe zip -> folder si actualizare daca este necesar
    for file in files1:
        src = os.path.join(folder1, file)
        dst = os.path.join(folder2, file)

        if file not in files2:
            copy_file(src, dst)
        else:
            # Comparam mtimes
            mtime_zip = get_zip_mtime(folder1, file)
            mtime_folder = os.path.getmtime(dst)
            if mtime_zip > mtime_folder:
                # Zip e mai nou, il copiem peste folder
                copy_file(src, dst)
                print(f"Updated {src} -> {dst}")

    # Copiere fisiere lipsa folder -> zip si act
    for file in files2:
        src = os.path.join(folder2, file)
        dst = os.path.join(folder1, file)

        if file not in files1:
            copy_file(src, dst)
        else:
            mtime_zip = get_zip_mtime(folder1, file)
            mtime_folder = os.path.getmtime(src)
            if mtime_folder > mtime_zip:
                # Folder e mai nou, îl copiem peste zip
                copy_file(src, dst)
                print(f"Updated {src} -> {dst}")

    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)


def sync_folders(folder1, folder2):
    """
    Mentine sincronizarea intre o arhiva ZIP si un folder.
    Detecteaza modificari, adauga fisiere lipsa si actualizeaza cele mai noi versiuni.

    Argumente:
        folder1 (str): Calea catre fisierul ZIP.
        folder2 (str): Calea catre folderul sincronizat.

    Actiuni:
        - Sterge fisierele care nu mai exista intr-o locatie.
        - Copiaza fisierele lipsa intre ZIP si folder.
        - Actualizeaza fisierele mai noi.
        - Actualizeaza listele globale ale fisierelor.
    """
    global global_file_paths1, global_file_paths2

    # stergerea fisierelor ramase
    for file in global_file_paths1:
        file_path1 = os.path.join(folder1, file)  # zip
        file_path2 = os.path.join(folder2, file)  # folder
        # daca a fost sters din zip, stergem si din folder
        if file not in list_files(folder1):  # nu mai exista în zip
            if os.path.exists(file_path2):
                delete_file(file_path2)

    for file in global_file_paths2:
        file_path1 = os.path.join(folder1, file)  # zip
        file_path2 = os.path.join(folder2, file)  # folder
        if file not in list_files(folder2):  # nu mai exista în folder
            # verificam dacă fisierul încă exista în zip
            current_zip_files = list_files(folder1)
            if file in current_zip_files:
                delete_file(file_path1)

    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)

    # Copiere fisiere lipsa din zip -> folder
    for file in global_file_paths1:
        file_path1 = os.path.join(folder1, file)  # zip
        file_path2 = os.path.join(folder2, file)  # folder
        if file not in global_file_paths2:
            copy_file(file_path1, file_path2)

    # Copiere fisiere lipss din folder -> zip
    for file in global_file_paths2:
        file_path1 = os.path.join(folder1, file)  # zip
        file_path2 = os.path.join(folder2, file)  # folder
        if file not in global_file_paths1:
            copy_file(file_path2, file_path1)

    # Actualizare fisiere mai noi
    intersectie = set(global_file_paths1).intersection(global_file_paths2)
    for file in intersectie:
        file_path1 = os.path.join(folder1, file)  # zip
        file_path2 = os.path.join(folder2, file)  # folder
        if os.path.isfile(get_zip_path()) and file in list_files(get_zip_path()) and os.path.exists(file_path2):
            mtime_zip = get_zip_mtime(folder1, file)
            mtime_folder = os.path.getmtime(file_path2)
            if mtime_zip > mtime_folder:
                copy_file(file_path1, file_path2)
            elif mtime_folder > mtime_zip:
                copy_file(file_path2, file_path1)

    global_file_paths1 = list_files(folder1)
    global_file_paths2 = list_files(folder2)


def run_sync(folder1, folder2):
    """
    Initiaza sincronizarea initiala si mentine sincronizarea continua intre o arhiva ZIP si un folder.

    Argumente:
        folder1 (str): Calea catre fisierul ZIP.
        folder2 (str): Calea catre folderul sincronizat.

    Actiuni:
        - Realizeaza sincronizarea initiala folosind functia `initial_sync`.
        - Mentine sincronizarea continua folosind functia `sync_folders`, la interval de o secunda.
    """
    initial_sync(folder1, folder2)
    print(f"Starting continuous sync between:\n  ZIP: {folder1}\n  FOLDER: {folder2}")
    while True:
        sync_folders(folder1, folder2)
        time.sleep(1)

#path-rui catre zip si folder
_zip_path = None
_folder_path = None


def set_paths(zip_path, folder_path):
    """
        Seteaza caile globale pentru fisierul ZIP si folder.

        Argumente:
            zip_path (str): Calea catre fisierul ZIP.
            folder_path (str): Calea catre folder.
        """
    global _zip_path, _folder_path
    _zip_path = os.path.abspath(zip_path)
    _folder_path = os.path.abspath(folder_path)


def get_zip_path():
    """
        Returneaza calea catre fisierul ZIP retinuta global.

        Returneaza:
            str: Calea catre fisierul ZIP.
        """
    return _zip_path


def get_folder_path():
    """
        Returneaza calea catre folderul retinuta global.

        Returneaza:
            str: Calea catre folder.
        """
    return _folder_path


def get_temp_dir():
    """
        Creeaza si returneaza un director temporar pentru operatiile de sincronizare.

        Returneaza:
            str: Calea catre directorul temporar.
        """
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_sync_temp")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir


def get_temp_zip_path():
    """
        Returneaza calea catre un fisier ZIP temporar utilizat in procesul de reconstructie a arhivei.

        Returneaza:
            str: Calea catre fisierul ZIP temporar.
        """
    return os.path.join(get_temp_dir(), "temp_sync.zip")


def get_zip_mtime(zip_path, rel_file):
    """
    Obtine timpul de modificare al unui fisier din arhiva ZIP.

    Argumente:
        zip_path (str): Calea catre arhiva ZIP.
        rel_file (str): Calea relativa a fisierului in arhiva.

    Returneaza:
        float: Timpul de modificare al fisierului (in format epoch).
    """
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            if info.filename == rel_file:
                # info.date_time -> (year, month, day, hour, minute, second)
                # transformare
                import datetime, time
                dt = datetime.datetime(*info.date_time)
                return time.mktime(dt.timetuple())
    # daca fisierul nu exista -> return 0
    return 0
