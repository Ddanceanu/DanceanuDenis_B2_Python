import random
import os

# Lista participanților
nume = ["Andrei", "Denis", "Sabina", "Robi"]

# Generăm o listă de perechi pentru Secret Santa
perechi = nume.copy()
random.shuffle(perechi)

# Ne asigurăm că nimeni nu își trage propriul nume
while any(nume[i] == perechi[i] for i in range(len(nume))):
    random.shuffle(perechi)

# Dicționar cu perechile pentru Secret Santa
secret_santa = {nume[i]: perechi[i] for i in range(len(nume))}

# Funcția pentru afișarea rezultatului și ștergerea ecranului
def afiseaza_si_sterge():
    while True:
        # Participantul își introduce numele
        participant = input("Introduceți numele dvs. (sau 'exit' pentru a ieși): ")
        if participant.lower() == 'exit':
            break
        elif participant in secret_santa:
            print(f"Persoana pentru care sunteți Secret Santa este: {secret_santa[participant]}")
            input("Apăsați Enter pentru a șterge ecranul.")
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("Nume invalid. Încercați din nou.")

# Apelăm funcția
afiseaza_si_sterge()
