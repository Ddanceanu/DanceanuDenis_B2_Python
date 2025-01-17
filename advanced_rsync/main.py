import sys
import re
from folder_sync import initial_sync, run_sync as folder_run_sync
from zip_sync import run_sync as zip_run_sync

# Definim regex-uri pentru validarea locațiilor
FTP_REGEX = r'^ftp:[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9.-]+/[a-zA-Z0-9._/-]+$'
ZIP_REGEX = r'^zip:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+\.zip$'
FOLDER_REGEX = r'^folder:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+$'

def check_location(loc):
    """
    Verifica daca locatia data este corecta.

    Argumente:
        loc (str): locatia de verificat.

    Returnează:
        bool: true pentru locatie valida, false altfel.
    """
    return bool(re.match(FTP_REGEX, loc) or re.match(ZIP_REGEX, loc) or re.match(FOLDER_REGEX, loc))

def parse_location(loc):
    """
    Extrage tipul si calea din locatie.

    Argumente:
        loc (str): locatia de procesat.

    Returnează:
        tuple: (tip_locatie, cale_locatie)
    """
    if loc.startswith("zip:"):
        return "zip", loc.split("zip:")[1]
    elif loc.startswith("folder:"):
        return "folder", loc.split("folder:")[1]
    else:
        return None, None

def main():
    print("Advanced RSync")
    if len(sys.argv) != 3:
        print("Usage: python main.py <location_1> <location_2>")
        sys.exit(1)

    loc1 = sys.argv[1]
    loc2 = sys.argv[2]

    if not (check_location(loc1) and check_location(loc2)):
        print("One or both locations are invalid.")
        sys.exit(1)

    type1, path1 = parse_location(loc1)
    type2, path2 = parse_location(loc2)

    if type1 == "zip" and type2 == "zip":
        print(f"Syncing ZIP: {path1} with ZIP: {path2}")
        zip_run_sync(path1, path2)

    elif type1 == "zip" and type2 == "folder":
        print(f"Syncing ZIP: {path1} with folder: {path2}")
        zip_run_sync(path1, path2)

    elif type1 == "folder" and type2 == "zip":
        print(f"Syncing folder: {path1} with ZIP: {path2}")
        zip_run_sync(path2, path1)

    elif type1 == "folder" and type2 == "folder":
        print(f"Syncing folder: {path1} with folder: {path2}")
        initial_sync(path1, path2)
        print("Initial sync completed.")
        folder_run_sync(path1, path2)

    else:
        print("Unsupported sync operation between the provided locations.")
        sys.exit(1)

if __name__ == '__main__':
    main()
