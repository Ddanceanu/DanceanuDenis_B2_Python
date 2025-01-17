import ssl
from ftplib import FTP_TLS

hostname = "127.0.0.1"
username = "user"
password = "denis"
local_file_path = r"C:\Users\ddanc\Documents\PythonLabs\advanced_rsync\test1\das.txt"
remote_path = "das.txt"

try:
    # Context TLS care negociază cea mai bună versiune (TLS1.2 / 1.3)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl_context.check_hostname = False

    ftps = FTP_TLS(context=ssl_context)
    ftps.set_debuglevel(2)  # Vezi mesajele de debug

    # Pas 1: Conectează-te la portul 21
    print("Connecting (FTPS explicit) la port 21 ...")
    ftps.connect(host=hostname, port=21)

    # Pas 2: Inițiază TLS (AUTH TLS)
    ftps.auth()

    # Pas 3: Login
    ftps.login(user=username, passwd=password)

    # Pas 4: Protejează canalul de date
    ftps.prot_p()

    # Pas 5: Upload
    with open(local_file_path, 'rb') as f:
        ftps.storbinary(f"STOR " + remote_path, f)

    print("Upload realizat cu succes!")

    ftps.quit()
except Exception as e:
    print(f"Eroare (explicit): {e}")

Eroare: [SSL: SHUTDOWN_WHILE_IN_INIT] shutdown while in init (_ssl.c:2696)  still this