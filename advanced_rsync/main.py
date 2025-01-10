import sys
import re

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

    if (check_location(loc1) and check_location(loc2)):
        print("Both locations are valid.")
    else:
        print("One or both locations are invalid.")
        sys.exit(1)


if __name__ == '__main__':
    main()