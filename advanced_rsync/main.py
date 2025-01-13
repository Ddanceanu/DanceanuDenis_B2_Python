import sys
import re
from folder_sync import initial_sync, run_sync
from zip_sync import run_sync

# Definim regex-uri pentru validarea locatiilor
FTP_REGEX = r'^ftp:[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9.-]+/[a-zA-Z0-9._/-]+$'
ZIP_REGEX = r'^zip:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+\.zip$'
FOLDER_REGEX = r'^folder:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+$'

def check_location(loc):
    """
    Verifica daca locatia data este corecta.

    Argumente:
        loc (str): locatia de verificat.

    Returnează:
        bool: true pentur locatie valoda, false altfel.
    """
    if re.match(FTP_REGEX, loc) or re.match(ZIP_REGEX, loc) or re.match(FOLDER_REGEX, loc):
        return True;
    else:
        return False;

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

    if loc1.startswith("zip:") and loc2.startswith("folder:"):
        zip_path = loc1.split("zip:")[1]
        folder_path = loc2.split("folder:")[1]
        print(f"Snycing ZIP: {zip_path} with folder: {folder_path}")
        run_sync(zip_path, folder_path)

    elif loc2.startswith("zip:") and loc1.startswith("folder:"):
        zip_path = loc2.split("zip:")[1]
        folder_path = loc1.split("folder:")[1]
        print(f"Snycing ZIP: {zip_path} with folder: {folder_path}")
        run_sync(zip_path, folder_path)


    # if loc1.startswith("folder:") and loc2.startswith("folder:"):
    #     folder1 = loc1.split("folder:")[1]
    #     folder2 = loc2.split("folder:")[1]
    #
    # initial_sync(folder1, folder2)
    # print(f"Initial sync completed.")
    # run_sync(folder1, folder2)


if __name__ == '__main__':
    main()