# DEPRECATED


from pathlib import Path

BOOK_NAMES = [
    "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
    "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
    "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
    "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
    "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
    "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark",
    "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
    "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
    "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter",
    "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
]

def main():
    root = Path(".")
    version_folders = [folder for folder in ["1632", "1879"] if (root / folder).is_dir()]

    if len(version_folders) == 0:
        raise FileNotFoundError("Nie znaleziono folderu 1632 ani 1879 w biezacym katalogu.")
    if len(version_folders) > 1:
        raise Exception("Umiesc w biezacym katalogu tylko jeden folder - 1879 lub 1632.")

    version_path = root / version_folders[0]
    output_lines = []

    for idx, book_folder in enumerate(sorted(version_path.iterdir())):
        if not book_folder.is_dir():
            continue

        book_name = BOOK_NAMES[idx]
        chapter_files = sorted(book_folder.glob("*.txt"))

        for chapter_idx, chapter_file in enumerate(chapter_files, start=1):
            with chapter_file.open(encoding="utf-8") as f:
                for verse_idx, line in enumerate(f, start=1):
                    verse = line.strip()
                    if verse:
                        reference = f"{book_name} {chapter_idx}:{verse_idx}"
                        output_lines.append(f"{reference} {verse}")

    output_path = root / "PBG_the_word.ont"
    with output_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(output_lines) + "\n")

    print(f"Pomyslnie zakonczono modyfikacje i utworzono plik: {output_path}.")

if __name__ == "__main__":
    main()
