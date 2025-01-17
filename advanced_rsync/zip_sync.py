import os
import shutil
import time
import zipfile

# liste globale ce retin caile fisierelor
global_file_paths1 = []
global_file_paths2 = []

# variabile globale pentru calea zip
_zip_path1 = None
_zip_path2 = None

def set_paths(loc1, loc2):  # seteaza global caile pentru loc1 si loc2
    """
    Stocheaza global caile pentru loc1 si loc2, care pot fi .zip sau directoare.

    Argumente:
        loc1 (str): Calea catre primul fisier sau director.
        loc2 (str): Calea catre al doilea fisier sau director.

    Actiuni:
        Evalueaza daca cele doua cai primite sunt fisiere zip si le stocheaza global.
    """
    global _zip_path1, _zip_path2
    _zip_path1 = None
    _zip_path2 = None
    abs1 = os.path.abspath(loc1)
    abs2 = os.path.abspath(loc2)
    # verificare zip loc1
    if os.path.isfile(abs1) and zipfile.is_zipfile(abs1):
        _zip_path1 = abs1
    # verificare zip loc2
    if os.path.isfile(abs2) and zipfile.is_zipfile(abs2):
        _zip_path2 = abs2

def get_zip_path1():  # returneaza calea zip1
    """
    Returneaza calea catre primul fisier zip global.

    Returneaza:
        str: calea catre fisierul zip1 sau None.
    """
    return _zip_path1

def get_zip_path2():  # returneaza calea zip2
    """
    Returneaza calea catre al doilea fisier zip global.

    Returneaza:
        str: calea catre fisierul zip2 sau None.
    """
    return _zip_path2

def is_zip(path):  # verifica daca path-ul e zip
    """
    Verifica daca un path specificat este un fisier zip valid.

    Argumente:
        path (str): Calea catre fisier.

    Returneaza:
        bool: True daca este zip valid, altfel False.
    """
    return os.path.isfile(path) and zipfile.is_zipfile(path)

def is_in_zip(path):  # verifica daca un path se afla intr-un zip cunoscut
    """
    Verifica daca un path incepe cu calea globala a zip1 sau zip2.

    Argumente:
        path (str): Calea completa catre fisier.

    Returneaza:
        int|None: 1 daca tine de zip_path1, 2 daca tine de zip_path2, altfel None.
    """
    z1 = get_zip_path1()
    z2 = get_zip_path2()
    if z1 and path.startswith(z1):
        return 1
    elif z2 and path.startswith(z2):
        return 2
    return None

def get_rel_path(full_path, zip_index):  # obtine calea relativa din zip
    """
    Transforma o cale completa (ce incepe cu un zip) in calea relativa din acel zip.

    Argumente:
        full_path (str): Calea completa catre fisier.
        zip_index (int): 1 sau 2, in functie de zip-ul in care se afla fisierul.

    Returneaza:
        str: Calea relativa in zip.
    """
    if zip_index == 1:
        prefix = get_zip_path1()
    else:
        prefix = get_zip_path2()
    return full_path.replace(prefix, "").lstrip("\\/")

def get_temp_dir():  # returneaza folderul temporar
    """
    Returneaza calea catre un folder temporar folosit pentru operatii intermediare.

    Returneaza:
        str: Calea catre folderul temporar (creat daca nu exista).
    """
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "zip_sync_temp")
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def get_temp_zip_path():  # returneaza calea catre un zip intermediar
    """
    Returneaza calea catre fisierul zip temporar folosit in operatii de reconstructie.

    Returneaza:
        str: Calea catre fisierul zip temporar.
    """
    return os.path.join(get_temp_dir(), "temp_sync.zip")

def list_files(path):  # creeaza o lista cu toate fisierele (cai relative) din folder sau zip
    """
    Creeaza o lista cu toate caile relative ale fisierelor dintr-o locatie (folder sau fisier zip).

    Argumente:
        path (str): Calea catre folder sau fisier zip.

    Returneaza:
        list: O lista cu toate caile relative existente, inclusiv subfoldere (sau structuri in zip).
    """
    if is_zip(path):
        file_paths = []
        with zipfile.ZipFile(path, 'r') as zf:
            file_paths = [f for f in zf.namelist() if not f.endswith('/')]
        return file_paths
    else:
        file_paths = []
        for root, dirs, files in os.walk(path):
            for filename in files:
                full_path = os.path.join(root, filename)
                relative_path = full_path.replace(path, "").lstrip("\\/")
                file_paths.append(relative_path)
        return file_paths

def get_zip_mtime(zip_path, rel_file):  # intoarce mtime al unui fisier din zip
    """
    Returneaza mtime (epoch) al unui fisier dintr-un fisier zip.

    Argumente:
        zip_path (str): Calea catre fisierul zip.
        rel_file (str): Calea relativa a fisierului din zip.

    Returneaza:
        float: Timpul in format epoch al fisierului sau 0 daca nu exista.
    """
    with zipfile.ZipFile(zip_path, 'r') as zf:
        for info in zf.infolist():
            if info.filename == rel_file:
                import datetime
                dt = datetime.datetime(*info.date_time)
                return time.mktime(dt.timetuple())
    return 0

def copy_file(src, dst):  # copiaza un fisier src -> dst (zip/folder)
    """
    Copiaza un fisier de la sursa la destinatie, unde sursa/destinatia pot fi in zip sau pe disc.

    Argumente:
        src (str): Calea sursa catre fisier.
        dst (str): Calea destinatie catre fisier.

    Actiuni:
        - Daca src este intr-un zip, se extrage temporar si se copiaza catre destinatie.
        - Daca dst este intr-un zip, se reconstruieste zip-ul si se introduce noul fisier.
        - Daca ambele sunt zip, se extrage din primul si se adauga in al doilea.
        - Daca ambele sunt foldere, se face copy2 direct.
    """
    src_zip_index = is_in_zip(src)
    dst_zip_index = is_in_zip(dst)

    # ZIP -> FOLDER
    if src_zip_index and not dst_zip_index:
        rel_path = get_rel_path(src, src_zip_index)
        zip_path = get_zip_path1() if src_zip_index == 1 else get_zip_path2()
        with zipfile.ZipFile(zip_path, 'r') as zf:
            try:
                zinfo = zf.getinfo(rel_path)
            except KeyError:
                print(f"[WARN] {rel_path} nu exista in zip!")
                return
            temp_extract = os.path.join(get_temp_dir(), rel_path)
            os.makedirs(os.path.dirname(temp_extract), exist_ok=True)
            zf.extract(rel_path, os.path.dirname(temp_extract))
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(temp_extract, dst)
            import datetime
            z_dt = datetime.datetime(*zinfo.date_time)
            zip_mtime = time.mktime(z_dt.timetuple())
            os.utime(dst, (zip_mtime, zip_mtime))

    # FOLDER -> ZIP
    elif not src_zip_index and dst_zip_index:
        rel_path = get_rel_path(dst, dst_zip_index)
        zip_path = get_zip_path1() if dst_zip_index == 1 else get_zip_path2()
        with zipfile.ZipFile(zip_path, 'r') as old_zip:
            old_files = old_zip.namelist()
            temp_zip_path = get_temp_zip_path()
            with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                for item in old_files:
                    if item != rel_path:
                        old_info = old_zip.getinfo(item)
                        data = old_zip.read(item)
                        new_info = zipfile.ZipInfo(item)
                        new_info.date_time = old_info.date_time
                        new_zip.writestr(new_info, data)
                mtime = os.path.getmtime(src)
                import datetime
                dt = datetime.datetime.fromtimestamp(mtime)
                new_info2 = zipfile.ZipInfo(rel_path)
                new_info2.date_time = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
                with open(src, 'rb') as f:
                    data = f.read()
                new_zip.writestr(new_info2, data)
        shutil.move(temp_zip_path, zip_path)

    # ZIP -> ZIP
    elif src_zip_index and dst_zip_index:
        src_rel = get_rel_path(src, src_zip_index)
        dst_rel = get_rel_path(dst, dst_zip_index)
        src_zip_path = get_zip_path1() if src_zip_index == 1 else get_zip_path2()
        dst_zip_path = get_zip_path1() if dst_zip_index == 1 else get_zip_path2()
        temp_extract = os.path.join(get_temp_dir(), src_rel)
        with zipfile.ZipFile(src_zip_path, 'r') as zf:
            try:
                old_info = zf.getinfo(src_rel)
            except KeyError:
                print(f"[WARN] {src_rel} nu exista in sursa!")
                return
            os.makedirs(os.path.dirname(temp_extract), exist_ok=True)
            zf.extract(src_rel, os.path.dirname(temp_extract))
        with zipfile.ZipFile(dst_zip_path, 'r') as old_zip:
            old_files = old_zip.namelist()
            temp_zip_path = get_temp_zip_path()
            with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                for item in old_files:
                    if item != dst_rel:
                        oinfo = old_zip.getinfo(item)
                        data = old_zip.read(item)
                        new_info = zipfile.ZipInfo(item)
                        new_info.date_time = oinfo.date_time
                        new_zip.writestr(new_info, data)
                import datetime
                dt = datetime.datetime(*old_info.date_time)
                new_info2 = zipfile.ZipInfo(dst_rel)
                new_info2.date_time = (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
                with open(temp_extract, 'rb') as f:
                    data = f.read()
                new_zip.writestr(new_info2, data)
        shutil.move(temp_zip_path, dst_zip_path)

    # FOLDER -> FOLDER
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

def delete_file(path):  # sterge un fisier din folder sau zip
    """
    Sterge un fisier existent de pe disc sau din zip.

    Argumente:
        path (str): Calea catre fisierul ce va fi sters.

    Actiuni:
        - Daca fisierul este in zip, se reconstruieste zip-ul fara acel fisier.
        - Daca fisierul este pe disc, se sterge direct.
    """
    zip_idx = is_in_zip(path)
    if zip_idx:
        rel_path = get_rel_path(path, zip_idx)
        zip_path = get_zip_path1() if zip_idx == 1 else get_zip_path2()
        with zipfile.ZipFile(zip_path, 'r') as old_zip:
            old_files = old_zip.namelist()
            if rel_path not in old_files:
                return
            temp_zip_path = get_temp_zip_path()
            with zipfile.ZipFile(temp_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as new_zip:
                for item in old_files:
                    if item != rel_path:
                        data = old_zip.read(item)
                        old_info = old_zip.getinfo(item)
                        new_info = zipfile.ZipInfo(item)
                        new_info.date_time = old_info.date_time
                        new_zip.writestr(new_info, data)
        shutil.move(temp_zip_path, zip_path)
        print(f"Deleted (from ZIP) {path}")
    else:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")

def initial_sync(loc1, loc2):  # sincronizare initiala
    """
    Sincronizeaza initial doua locatii (zip sau foldere).

    Argumente:
        loc1 (str): Calea catre prima locatie (zip/folder).
        loc2 (str): Calea catre a doua locatie (zip/folder).

    Actiuni:
        - Copiaza fisierele lipsa intre cele doua locatii.
        - Actualizeaza fisierele care au mtime mai nou in cealalta locatie.
        - Actualizeaza listele globale cu fisiere.
    """
    global global_file_paths1, global_file_paths2
    set_paths(loc1, loc2)
    files1 = list_files(loc1)
    files2 = list_files(loc2)
    # din loc1 -> loc2
    for file in files1:
        src = os.path.join(loc1, file)
        dst = os.path.join(loc2, file)
        if file not in files2:
            copy_file(src, dst)
        else:
            if is_zip(loc1):
                mtime1 = get_zip_mtime(loc1, file)
            else:
                mtime1 = os.path.getmtime(src)
            if is_zip(loc2):
                mtime2 = get_zip_mtime(loc2, file)
            else:
                mtime2 = os.path.getmtime(dst)
            if mtime1 > mtime2:
                copy_file(src, dst)
                print(f"Updated {src} -> {dst}")
    # din loc2 -> loc1
    for file in files2:
        src = os.path.join(loc2, file)
        dst = os.path.join(loc1, file)
        if file not in files1:
            copy_file(src, dst)
        else:
            if is_zip(loc2):
                mtime2 = get_zip_mtime(loc2, file)
            else:
                mtime2 = os.path.getmtime(src)
            if is_zip(loc1):
                mtime1 = get_zip_mtime(loc1, file)
            else:
                mtime1 = os.path.getmtime(dst)
            if mtime2 > mtime1:
                copy_file(src, dst)
                print(f"Updated {src} -> {dst}")
    global_file_paths1 = list_files(loc1)
    global_file_paths2 = list_files(loc2)

def sync_folders(loc1, loc2):  # sincronizare continua intre locatii
    """
    Mentine sincronizarea continua intre loc1 si loc2 (ambele pot fi zip/folder).

    Argumente:
        loc1 (str): Prima locatie (zip/folder).
        loc2 (str): A doua locatie (zip/folder).

    Actiuni:
        - Sterge fisierele care au fost sterse in cealalta locatie.
        - Copiaza fisierele lipsa intre locatii.
        - Actualizeaza fisierele in functie de mtime.
        - Actualizeaza listele globale cu fisiere.
    """
    global global_file_paths1, global_file_paths2

    # stergere fisiere disparute din loc1
    current_files1 = list_files(loc1)
    for file in global_file_paths1:
        if file not in current_files1:
            file_path2 = os.path.join(loc2, file)
            if file in global_file_paths2:
                delete_file(file_path2)

    # stergere fisiere disparute din loc2
    current_files2 = list_files(loc2)
    for file in global_file_paths2:
        if file not in current_files2:
            file_path1 = os.path.join(loc1, file)
            if file in global_file_paths1:
                delete_file(file_path1)

    # actualizare liste
    global_file_paths1 = list_files(loc1)
    global_file_paths2 = list_files(loc2)

    # copiere fisiere lipsa loc1->loc2
    for file in global_file_paths1:
        if file not in global_file_paths2:
            src = os.path.join(loc1, file)
            dst = os.path.join(loc2, file)
            copy_file(src, dst)

    # copiere fisiere lipsa loc2->loc1
    for file in global_file_paths2:
        if file not in global_file_paths1:
            src = os.path.join(loc2, file)
            dst = os.path.join(loc1, file)
            copy_file(src, dst)

    # actualizare fisiere comune
    intersectie = set(global_file_paths1).intersection(global_file_paths2)
    for file in intersectie:
        path1 = os.path.join(loc1, file)
        path2 = os.path.join(loc2, file)
        if is_zip(loc1):
            mtime1 = get_zip_mtime(loc1, file)
        else:
            mtime1 = os.path.getmtime(path1)
        if is_zip(loc2):
            mtime2 = get_zip_mtime(loc2, file)
        else:
            mtime2 = os.path.getmtime(path2)
        if mtime1 > mtime2:
            copy_file(path1, path2)
        elif mtime2 > mtime1:
            copy_file(path2, path1)

    # actualizare liste in final
    global_file_paths1 = list_files(loc1)
    global_file_paths2 = list_files(loc2)

def run_sync(loc1, loc2):  # initiaza si mentine sincronizarea
    """
    Initiaza sincronizarea initiala si apoi mentine sincronizarea intre loc1 si loc2.

    Argumente:
        loc1 (str): Prima locatie (zip/folder).
        loc2 (str): A doua locatie (zip/folder).

    Actiuni:
        - Apeleaza initial_sync pentru sincronizare initiala.
        - Ruleaza continuu sync_folders la un interval de 1 secunda.
    """
    initial_sync(loc1, loc2)
    print(f"Starting continuous sync between:\n  {loc1}\n  {loc2}")
    while True:
        sync_folders(loc1, loc2)
        time.sleep(1)
