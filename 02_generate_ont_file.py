from pathlib import Path

# UWAGA
# description_1632 ma 418 nie białych znaków
# przy zmianie opisu należy ponownie policzyć liczbę nie białych znaków
# przy pomocy skryptu count_non_whitespace_chars.py
# lub https://www.grammarly.com/character-counter (usuwając znaki """, "\n" oraz z sekcji about "\" ale zostawić """ na końcu i początku treści strony tytułowej biblii) Wynik to wartość w polu "Characters without spaces".
# Otrzymaną liczbę uwzględnić w pliku test_none_of_the_characters_fell.py
description_1632 = (
    "description=Polska Biblia Gdańska 1632\n"
    "short.title=PBG1632\n"
    "lang=pol\n"
    "publish.date=2025\n"
    "publisher=\n"
    "version.major=1\n"
    "version.minor=0.1\n"
    "source=<a href=\"https://github.com/piotrskurzynski/biblia\">https://github.com/piotrskurzynski/biblia</a>\n"
    "about=Polska Biblia Gdańska 1632. "
    "\"Biblia Swięta: to jeſt Księgi Starego y Nowego Przymierza "
    "z Zydowſkiego y Greckiego Języká ná Polſki pilnie y wiernie przetłumáczone. "
    "Cum Gratia & Privilegio S.R.M. we Gdansku Roku MDCXXXII.\"\n"
)

# description_1879 ma 403 nie białych znaków
description_1879 = (
    "description=Polska Biblia Gdańska 1879\n"
    "short.title=PBG1879\n"
    "lang=pol\n"
    "publish.date=2025\n"
    "publisher=\n"
    "version.major=1\n"
    "version.minor=0.1\n"
    "source=<a href=\"https://github.com/piotrskurzynski/biblia\">https://github.com/piotrskurzynski/biblia</a>\n"
    "about=Polska Biblia Gdańska 1879 (1632, rewizja 1879). "
    "\"Biblija Święta to jest wszystko Pismo Święte starego i nowego Testamentu. "
    "Z hebrajskiego i greckiego języka na polski pilnie i wiernie przetłómaczona.\"\n"
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

    if (version_folders == ['1632']):
        output_path = root / "PBG1632_the_word.ont"
        output_path.write_text("\n".join(output_lines) + "\n\n\n" + description_1632, encoding="utf-8")
    elif (version_folders == ['1879']):
        output_path = root / "PBG1879_the_word.ont"
        output_path.write_text("\n".join(output_lines) + "\n\n\n" + description_1879, encoding="utf-8")
    # elif (version_folders == ['20nn']):
        # output_path = root / "PBG20nn_the_word.ont"
        # output_path.write_text("\n".join(output_lines) + "\n\n\n" + description_20nn, encoding="utf-8")

    print(f"Pomyslnie zakonczono modyfikacje i utworzono plik: {output_path}.")

if __name__ == "__main__":
    main()
