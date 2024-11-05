class LibraryItem:
    def __init__(self, title, year):
        self.title = title.lower()
        self.year = year
        self.is_checked_out = False

    def check_out(self):
        if not self.is_checked_out:
            self.is_checked_out = True
            print(f"'{self.title}' a fost imprumutat.")
        else:
            print(f"'{self.title}' este deja imprumutat.")

    def return_item(self):
        if self.is_checked_out:
            self.is_checked_out = False
            print(f"'{self.title}' a fost returnat.")
        else:
            print(f"'{self.title}' nu este imprumutat.")

    def display_info(self):
        print(f"Titlu: {self.title}")
        print(f"An: {self.year}")
        print(f"Imprumutat: {'Da' if self.is_checked_out else 'Nu'}\n")


class Book(LibraryItem):
    def __init__(self, title, year, author, pages):
        super().__init__(title, year)
        self.author = author
        self.pages = pages

    def display_info(self):
        super().display_info()
        print(f"Autor: {self.author}")
        print(f"Pagini: {self.pages}\n")


class DVD(LibraryItem):
    def __init__(self, title, year, director, duration):
        super().__init__(title, year)
        self.director = director
        self.duration = duration

    def display_info(self):
        super().display_info()
        print(f"Regizor: {self.director}")
        print(f"Durata: {self.duration} minute\n")


class Magazine(LibraryItem):
    def __init__(self, title, year, issue, publisher):
        super().__init__(title, year)
        self.issue = issue
        self.publisher = publisher

    def display_info(self):
        super().display_info()
        print(f"Editie: {self.issue}")
        print(f"Editura: {self.publisher}\n")


def main():
    book = Book(title="Morometii", year=1955, author="Marin Preda", pages=416)
    book.display_info()
    book.check_out()
    book.return_item()
    book.display_info()

    dvd = DVD(title="Amintiri din copilarie", year=1965, director="Elisabeta Bostan", duration=90)
    dvd.display_info()
    dvd.check_out()
    dvd.return_item()
    dvd.display_info()

    magazine = Magazine(title="Stiinta si Tehnica", year=2022, issue="Septembrie", publisher="Asociatia Romana pentru Stiinta")
    magazine.display_info()
    magazine.check_out()
    magazine.return_item()
    magazine.display_info()

if __name__ == "__main__":
    main()