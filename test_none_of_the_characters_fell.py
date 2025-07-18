import re
import unicodedata

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

def clean_references(content):
    # Dołączamy nazwy ksiąg do jednego OR (|) wzorca, posortowane malejąco długością, aby najdłuższe nazwy były dopasowane pierwsze
    sorted_books = sorted(BOOK_NAMES, key=len, reverse=True)
    book_pattern = "|".join(re.escape(book) for book in sorted_books)
    
    # Wzorzec:
    # (opcjonalny przedrostek byref|pref|ref z ewentualną spacją) + nazwa księgi + spacja + liczba:liczba
    # usuwamy cały ten fragment, uwzględniając ewentualne spacje wokół
    pattern = rf"(?:\b(?:byref|pref|ref)\b\s*)?({book_pattern})\s+\d+:\d+"
    
    # Usuwamy wszystkie dopasowania wzorca
    content = re.sub(pattern, "", content)
    
    # Usuwamy nadmiarowe spacje powstałe po usunięciu
    content = re.sub(r'\s{2,}', ' ', content)
    
    # Usuwamy spacje na początku i końcu
    content = content.strip()
    
    return content

def normalize_and_strip(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.strip()
    text = re.sub(r"\s+", "", text)
    return text

# Pliki wejściowe
file1 = "PBG_original.txt"
file2 = "PBG_the_word.ont"


# Wczytaj oryginalne treści
with open(file1, encoding="utf-8") as f:
    content1 = f.read()

with open(file2, encoding="utf-8") as f:
    content2 = f.read()

# Usuń referencje z pliku 2
cleaned_content2 = clean_references(content2)


############   Kod diagnostyczny początek    ##########################
# Kod pomocny w celach diagnostycznych.
# Odkomentuj kod jeśli program zwrócił RÓŻNĄ ilość znaków - potem
# uruchom skrypt locate_char_diff.py w celu określenia miejsca różnicy. 

# modified_file2 = "PBG_modified.txt"
# out1 = "PBG_mod_1.txt"
# out2 = "PBG_mod_2.txt"
# with open(modified_file2, "w", encoding="utf-8") as f:
#     f.write(cleaned_content2)
    
# normalized1 = normalize_and_strip(content1)
# normalized2 = normalize_and_strip(cleaned_content2)

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
count2 = len(normalize_and_strip(cleaned_content2))

description_length = 399 # patrz skrypt 02_generate_ont_file.py
count1 = count1 + description_length

if count1 == count2:
    print("Liczba znaków (bez białych znaków i referencji) jest IDENTYCZNA.")
else:
    print("Liczba znaków (bez białych znaków i referencji) jest RÓŻNA.")
    print(f"{file1}: {count1} znaków")
    print(f"{file2} (po modyfikacji): {count2} znaków")
