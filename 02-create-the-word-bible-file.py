from pathlib import Path

# UWAGA
# description ma 296 343 nie białych znaków
# przy zmianie opisu należy ponownie policzyć liczbę nie białych znaków
# przy pomocy skryptu licz_ilosc_znakow_bez_bialych_znakow.py
# oraz uwzględnić ją w pliku test_nie_upadl_zaden_znak.py
description = (
    "description=Polska Biblia Gdańska 1879\n"
    "short.title=PBG\n"
    "lang=pol\n"
    "publish.date=2025\n"
    "publisher=\n"
    "version.major=1\n"
    "version.minor=0.1\n"
    "source=<a href=\"https://github.com/piotrskurzynski/biblia\">https://github.com/piotrskurzynski/biblia</a>\n"
    "about=Polska Biblia Gdańska 1879 (1632, rewizja 1879). "
    "\"Biblija Święta to jest wszystko Pismo Święte starego i nowego Testamentu. "
    "Z hebrajskiego i greckiego języka na polski pilnie i wiernie przetłómaczona.\""
)



def main():
    root = Path(".")
    version_folders = [folder for folder in ["1632", "1879"] if (root / folder).is_dir()]

    if len(version_folders) == 0:
        raise FileNotFoundError("Nie znaleziono folderu 1632 ani 1879 w biezacym katalogu.")
    if len(version_folders) > 1:
        raise Exception("Umiesc w biezacym katalogu tylko jeden folder - 1879 lub 1632.")

    version_path = root / version_folders[0]
    output_lines = []

    for book_folder in sorted(version_path.iterdir()):
        if not book_folder.is_dir():
            continue

        for chapter_file in sorted(book_folder.glob("*.txt")):
            with chapter_file.open(encoding="utf-8") as f:
                for line in f:
                    verse = line.strip()
                    if verse:
                        output_lines.append(verse)

    output_path = root / "PBG_the_word.ont"
    output_path.write_text("\n".join(output_lines) + "\n\n\n" + description + "\n", encoding="utf-8")

    print(f"Pomyslnie zakonczono modyfikacje i utworzono plik: {output_path}.")

if __name__ == "__main__":
    main()
