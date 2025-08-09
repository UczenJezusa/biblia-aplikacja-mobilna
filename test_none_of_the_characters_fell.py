import re
import unicodedata
from pathlib import Path

# BOOK_NAMES = [
#     "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges",
#     "Ruth", "1 Samuel", "2 Samuel", "1 Kings", "2 Kings", "1 Chronicles",
#     "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalms", "Proverbs",
#     "Ecclesiastes", "Song of Songs", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel",
#     "Daniel", "Hosea", "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum",
#     "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew", "Mark",
#     "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians",
#     "Ephesians", "Philippians", "Colossians", "1 Thessalonians", "2 Thessalonians",
#     "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews", "James", "1 Peter",
#     "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation"
# ]

def normalize_and_strip(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    return text

# Pliki wejściowe
file1 = "PBG_original.txt"

# Sprawdź istnienie file1
if not Path(file1).exists():
    raise FileNotFoundError(f"Brak pliku wejsciowego w biezacym folderze: PBG_original.txt")

# Możliwe nazwy dla file2 — priorytetowana lista
candidates = [
    "PBG1632_the_word.ont",
    "PBG1879_the_word.ont",
    # "PBG20nn_the_word.ont"
]

# Zbierz które z candidate istnieją
existing = [name for name in candidates if Path(name).exists()]

if len(existing) == 0:
    raise FileNotFoundError(
        "Nie znaleziono pliku PBGnnnn_the_word.ont w biezacym folderze."
    )
elif len(existing) > 1:
    raise FileExistsError(
        "Znaleziono więcej niż jeden plik PBGnnnn_the_word.ont. "
        "Usuń niepotrzebne pliki.\n"
        "Znalezione pliki: " + ", ".join(existing)
    )
else:
    file2 = existing[0]


# Wczytaj oryginalne treści
with open(file1, encoding="utf-8") as f:
    content1 = f.read()

with open(file2, encoding="utf-8") as f:
    content2 = f.read()

############   Kod diagnostyczny początek    ##########################
# Kod pomocny w celach diagnostycznych.
# Odkomentuj kod jeśli program zwrócił RÓŻNĄ ilość znaków - potem
# uruchom skrypt locate_char_diff.py w celu określenia miejsca różnicy. 

# modified_file2 = "PBG_modified.txt"
# out1 = "PBG_mod_1.txt"
# out2 = "PBG_mod_2.txt"
# with open(modified_file2, "w", encoding="utf-8") as f:
#     f.write(content2)
    
# normalized1 = normalize_and_strip(content1)
# normalized2 = normalize_and_strip(content2)

# # Zapis oczyszczonych wersji do plików
# with open(out1, "w", encoding="utf-8") as f:
#     f.write(normalized1)
# with open(out2, "w", encoding="utf-8") as f:
#     f.write(normalized2)

# # Porównanie długości
# count1 = len(normalized1)
# count2 = len(normalized2)

#############   Kod diagnostyczny koniec   ##########################


# Porównanie długości
count1 = len(normalize_and_strip(content1))
count2 = len(normalize_and_strip(content2))

# W celu uzyskania długości description patrz: skrypt 02_generate_ont_file.py
if file2 == candidates[0]: # PBG1632_the_word.ont
    description_length = 418
elif file2 == candidates[1]: # PBG1879_the_word.ont
    description_length = 403
# elif file2 == candidates[2]: # PBG20nn_the_word.ont
#     description_length = 

count1 = count1 + description_length

if count1 == count2:
    print("Liczba znaków (bez białych znaków) jest IDENTYCZNA.")
else:
    print("Liczba znaków (bez białych znaków) jest RÓŻNA.")
    print(f"{file1}: {count1} znaków")
    print(f"{file2}: {count2} znaków")
