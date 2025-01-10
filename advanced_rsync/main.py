import sys
import re
from folder_sync import initial_sync

# Definim regex-uri pentru validarea locatiilor
FTP_REGEX = r'^ftp:[a-zA-Z0-9]+:[a-zA-Z0-9]+@[a-zA-Z0-9.-]+/[a-zA-Z0-9._/-]+$'
ZIP_REGEX = r'^zip:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+\.zip$'
FOLDER_REGEX = r'^folder:[a-zA-Z]:\\[\\a-zA-Z0-9._-]+$'

def check_location(loc):
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

    if loc1.startswith("folder:") and loc2.startswith("folder:"):
        folder1 = loc1.split("folder:")[1]
        folder2 = loc2.split("folder:")[1]

    initial_sync(folder1, folder2)


if __name__ == '__main__':
    main()