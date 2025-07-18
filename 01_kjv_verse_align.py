#!/usr/bin/env python3
import os
import sys
import re

# ------------------------------------------------------------------------
# LISTY PLIKÓW (relatywnie do katalogu bazowego "1879" lub "1632")
# ------------------------------------------------------------------------


# Kategoria 1: "merge last verse to pre-last"
MERGE_LAST = [
    "03-lev/16.txt",
    "03-lev/24.txt",
    "09-reg/20.txt",
    "64-joh/01.txt",
]

# Kategoria 1b: "merge specific pair" – (plik, numer linii, numer następnej linii)
MERGE_PAIRS = [
    ("11-reg/22.txt", 43),  # połączenie linii 43 i 44
]

# Kategoria 2a: "merge first 2 lines"
MERGE_FIRST2 = [
    "19-psa/003.txt",
    "19-psa/004.txt",
    "19-psa/005.txt",
    "19-psa/006.txt",
    "19-psa/007.txt",
    "19-psa/008.txt",
    "19-psa/009.txt",
    "19-psa/012.txt",
    "19-psa/013.txt",
    "19-psa/014.txt",
    "19-psa/018.txt",
    "19-psa/019.txt",
    "19-psa/020.txt",
    "19-psa/021.txt",
    "19-psa/022.txt",
    "19-psa/030.txt",
    "19-psa/031.txt",
    "19-psa/034.txt",
    "19-psa/036.txt",
    "19-psa/038.txt",
    "19-psa/039.txt",
    "19-psa/040.txt",
    "19-psa/041.txt",
    "19-psa/042.txt",
    "19-psa/044.txt",
    "19-psa/045.txt",
    "19-psa/046.txt",
    "19-psa/047.txt",
    "19-psa/048.txt",
    "19-psa/049.txt",
    "19-psa/053.txt",
    "19-psa/055.txt",
    "19-psa/056.txt",
    "19-psa/057.txt",
    "19-psa/058.txt",
    "19-psa/059.txt",
    "19-psa/061.txt",
    "19-psa/062.txt",
    "19-psa/063.txt",
    "19-psa/064.txt",
    "19-psa/065.txt",
    "19-psa/067.txt",
    "19-psa/068.txt",
    "19-psa/069.txt",
    "19-psa/070.txt",
    "19-psa/075.txt",
    "19-psa/076.txt",
    "19-psa/077.txt",
    "19-psa/080.txt",
    "19-psa/081.txt",
    "19-psa/083.txt",
    "19-psa/084.txt",
    "19-psa/085.txt",
    "19-psa/088.txt",
    "19-psa/089.txt",
    "19-psa/092.txt",
    "19-psa/102.txt",
    "19-psa/108.txt",
    "19-psa/140.txt",
    "19-psa/142.txt",
]

# Kategoria 2b: "merge first 3 lines"
MERGE_FIRST3 = [
    "19-psa/051.txt",
    "19-psa/052.txt",
    "19-psa/054.txt",
    "19-psa/060.txt",
]

# Kategoria 3: "current first -> prev end"
CURRENT_TO_PREV = [
    "04-num/13.txt",
    "04-num/30.txt",
    "09-reg/24.txt",
    "32-ion/02.txt",
    "37-agg/02.txt",
]

# Kategoria 3a: "current first 3 -> prev end"
CURRENT_FIRST3_TO_PREV = [
    "18-iob/39.txt",
]

# Kategoria 4: przeniesienie ostatnich n niepustych wersetów do początku następnego pliku
CURRENT_LAST_N_LINES_TO_NEXT_BEGIN = {
    "21-ecc/04.txt": 1,
    "22-can/05.txt": 1,
    "18-iob/36.txt": 1,
    "18-iob/39.txt": 5,
    "18-iob/40.txt": 9,
}

# Kategoria 4a: jak 4, ale przeniesione n wersetów łączyć z istniejącą pierwszą linią
CURRENT_LAST_N_LINES_TO_NEXT_BEGIN_MERGE = {
    "21-ecc/07.txt": 1,
    "66-apo/12.txt": 1,
}

def detect_base_dir():
    cwd = os.getcwd()
    dirs = [d for d in ("1879", "1632") if os.path.isdir(os.path.join(cwd, d))] # do dodania rok współczesnej rewizji: ,"20nn"
    if len(dirs) == 0:
        raise FileNotFoundError(
            "Nie znaleziono folderu '1879', '1632' ani katalogu w formacie '20nn' w biezacym katalogu."
        )
    
    if len(dirs) > 1:
        raise Exception(
            "Znaleziono wiecej niż jeden katalog bazowy. "
            "Zostaw w biezacym katalogu tylko jeden z: '1879', '1632' lub '20nn'."
        )
    selected = dirs[0]
    base_dir = os.path.join(cwd, selected)
    if selected == "1632":
        merge_pair_lines(base_dir=base_dir, rel_path="43-joh/01.txt", line_num=36)
    return base_dir

def read_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)

def merge_last_verse(base_dir, rel_path):
    """
    Kategoria 1:
    - Usuń puste linie z końca.
    - Połącz ostatnią (niepustą) linię z przedostatnią, dodając spację między nimi.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    lines = read_lines(path)

    # usuń pustą linię na końcu
    while lines and lines[-1].strip() == "":
        lines.pop()

    if len(lines) < 2:
        return
        
    # połącz ostatnią linię z przedostatnią
    last = lines.pop().rstrip("\n")
    lines[-1] = lines[-1].rstrip("\n") + " " + last + "\n"
    write_lines(path, lines)


def merge_pair_lines(base_dir, rel_path, line_num):
    """
    Kategoria 1b:
    - Połącz zawartość linii `line_num` i `line_num+1` (1-indeksowane) w pliku rel_path.
    - Usuń linię `line_num+1`, a wiersz `line_num` rozszerz o spację i zawartość starej linii `line_num+1`.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    lines = read_lines(path)
    idx = line_num - 1  # zamiana na indeks 0-indeksowany

    if idx < 0 or idx + 1 >= len(lines):
        print(f"  [WARN] Niepoprawny zakres linii dla {rel_path}: {line_num}")
        return

    # Połącz linie: (line_num) + spacja + (line_num+1)
    first = lines[idx].rstrip("\n")
    second = lines[idx + 1].rstrip("\n")

    merged = first + " " + second + "\n"
    # Usuń stare linie i wstaw nową
    lines.pop(idx)       # usuwamy starą linię idx
    lines.pop(idx)       # usuwamy starą linię idx+1 (już przesunęła się na idx)
    lines.insert(idx, merged)
    write_lines(path, lines)


def merge_first_n_lines(base_dir, rel_path, n):
    """
    Kategoria 2:
    - Połącz pierwsze n linii pliku (w jedną linię, oddzielając spacją).
    - Usuń te n linii i zastąp je linią wynikową + reszta od n-tej+1.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    lines = read_lines(path)
    if len(lines) < n:
        return

    merged_parts = [lines[i].rstrip("\n") for i in range(n)]
    rest = lines[n:]

    merged_line = " ".join(merged_parts).rstrip() + "\n"
    new_lines = [merged_line] + rest
    write_lines(path, new_lines)


def current_first_n_lines_to_prev_end(base_dir, rel_path, n):
    """ Kategoria 3 i 3a:
    Przenosi pierwsze n niepustych linii z pliku rel_path do pliku poprzedniego (num-1.txt).
    - Jeżeli n > liczba niepustych linii, przeniesie tyle, ile jest.
    - Po przeniesieniu usuwa je z bieżącego pliku i dopisuje (każdą osobno) na końcu pliku poprzedniego.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    # Rozbicie rel_path na katalog i nazwę pliku
    dir_, fname = os.path.split(rel_path)
    try:
        num = int(os.path.splitext(fname)[0])
    except ValueError:
        print(f"  [WARN] Nieprawidłowa nazwa pliku (brak numeru): {rel_path}")
        return

    if num <= 1:
        print(f"  [WARN] Brak poprzedniego pliku dla: {rel_path}")
        return

    prev_fname = f"{num - 1:02d}.txt"
    prev_path = os.path.join(base_dir, dir_, prev_fname)
    if not os.path.isfile(prev_path):
        print(f"  [WARN] Nie znaleziono poprzedniego pliku: {os.path.join(dir_, prev_fname)}")
        return

    # Wczytanie zawartości obu plików
    curr = read_lines(path)
    prev = read_lines(prev_path)

    # Wyciągnięcie kolejnych n niepustych linii z curr
    moved = []
    idx = 0
    while len(moved) < n and idx < len(curr):
        if curr[idx].strip() != "":
            moved.append(curr[idx].rstrip("\n"))
            curr.pop(idx)
        else:
            idx += 1

    if not moved:
        # Nie znaleziono żadnej niepustej linii do przeniesienia
        return

    # Zapis curr (bez przeniesionych linii)
    write_lines(path, curr)

    # Usuń ewentualne puste linie z końca prev
    while prev and prev[-1].strip() == "":
        prev.pop()

    # Dopisz przeniesione linie (każdą jako osobną linijkę) na końcu prev
    for ln in moved:
        prev.append(ln + "\n")

    write_lines(prev_path, prev)


def move_last_n_to_next(base_dir, rel_path, n, merge_with_first=False):
    """
    Przenosi ostatnie n niepustych wierszy z pliku rel_path do początku pliku następującego
    (num+1.txt). Jeśli merge_with_first=True, połączy przeniesione wiersze z istniejącą pierwszą linią.
    """
    # Ścieżka bieżąca i wyznaczenie pliku następnego
    curr_path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(curr_path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    dir_, fname = os.path.split(rel_path)
    try:
        num = int(os.path.splitext(fname)[0])
    except ValueError:
        print(f"  [WARN] Nieprawidłowa nazwa pliku (brak numeru): {rel_path}")
        return

    next_num = num + 1
    next_fname = f"{next_num:02d}.txt"
    next_path = os.path.join(base_dir, dir_, next_fname)

    if not os.path.isfile(next_path):
        print(f"  [WARN] Nie znaleziono następnego pliku: {os.path.join(dir_, next_fname)}")
        return

    # Wczytaj linie obu plików
    curr_lines = read_lines(curr_path)
    next_lines = read_lines(next_path)

    # Usuń puste linie z końca 'curr_lines'
    while curr_lines and curr_lines[-1].strip() == "":
        curr_lines.pop()

    # Wyciągnij ostatnie n niepustych wierszy (od końca)
    moved = []
    idx = len(curr_lines) - 1
    while len(moved) < n and idx >= 0:
        if curr_lines[idx].strip() != "":
            moved.insert(0, curr_lines[idx].rstrip("\n"))
            curr_lines.pop(idx)
        idx -= 1

    if not moved:
        # Nie ma czego przenosić
        write_lines(curr_path, curr_lines)  # mimo wszystko zapisz, jeśli usunięto puste linie
        return

    # Zapisz curr (po usunięciu przeniesionych wierszy)
    write_lines(curr_path, curr_lines)

    # Przygotuj 'next_lines': usuń ewentualne pustą linię na początku, jeśli merge_with_first=False
    if not merge_with_first:
        # Po prostu dołącz przeniesione wiersze przed wszystkimi
        new_next = [ln + "\n" for ln in moved] + next_lines
    else:
        # Wersje 4a: połącz przeniesione wiersze z istniejącą pierwszą linią
        if not next_lines:
            # Jeśli next jest pusty, stwórz nową listę z przeniesionymi wierszami
            new_next = [moved[-1] + "\n"]  # moved zawiera n wierszy, ale n=1 w 4a
        else:
            # Połącz ostatni z przeniesionych wierszy (albo całą treść, jeśli n>1) z pierwszą linią next
            first = next_lines[0].rstrip("\n")
            merged_first = moved[-1] + " " + first + "\n"
            new_next = [merged_first] + next_lines[1:]

    # Zapisz zmodyfikowany 'next_path'
    write_lines(next_path, new_next)


def split_line(base_dir, rel_path, line_number, pattern, capitalize=False, case_insensitive=False):
    """
    Podzieli plik rel_path w bazie base_dir w dokładnie tej linii (1-indeksowanej) na dwie:
    - Znajdzie w linii numer line_number pierwsze wystąpienie pattern (regex lub zwykły tekst),
      usunie ewentualną spację we wzorcu (np. ': ' → ':' albo '. ' → '.'),
      oraz:
      • jeśli capitalize=False – po prostu przeniesie resztę tekstu po wzorcu do kolejnej, nowej linii;
      • jeśli capitalize=True  – w przenoszonej części pierwsza litera wzorca (lub dopasowanej frazy)
                             zostanie zamieniona na wielką.
    - Pozostałe linie zostają niezmienione.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    # Wczytujemy wszystkie linie
    lines = read_lines(path)
    idx = line_number - 1
    if idx < 0 or idx >= len(lines):
        print(f"  [WARN] Niepoprawny numer linii {line_number} w pliku {rel_path}")
        return

    original = lines[idx].rstrip("\n")
    flags = re.IGNORECASE if case_insensitive else 0
    match = re.search(pattern, original, flags)
    if not match:
        # jeśli nie znaleziono wzorca, nic nie robimy
        return

    start, end = match.span()
    # Zamontuj przedziały:
    #   prefix = wszystko przed match.start()
    #   mid    = wzorzec
    #   suffix = wszystko po match.end()
    prefix = original[:start]
    mid    = original[start:end]
    suffix = original[end:]

    # Usuń ewentualną spację na końcu wzorca (": " → ":"; ". " → "."), jeśli ją zawiera
    # Jeśli wzorzec to np. ": ", to mid może zawierać spację. Obetniemy spację:
    mid_stripped = mid.rstrip(" ")

    # Jeśli wymagamy capitalize: we wzorcu (mid_stripped) zamieniamy pierwszą literę na wielką
    if capitalize:
        # Jeśli wzorzec to fraza typu "będę" lub "(?i)alem", 
        # to zastępujemy tę frazę jej wersją z pierwszą wielką literą:
        adj_mid = mid_stripped[0].upper() + mid_stripped[1:]
    else:
        adj_mid = mid_stripped

    # Nowe linie: prefix + ewentualnie znak końca linii 
    # (usuń spację po wzorcu w starej linii, więc oryginalnie "prefix + mid + suffix" zamieniamy na:)
    # Jeśli wzorzec wygląda na słowo (np. "alem", "będę") – przenieś do drugiej linii
    if re.fullmatch(r"[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+", mid_stripped):
        # np. "alem" → trafia w całości na początek nowej linii
        new_first = prefix.rstrip(" ") + "\n"
        new_second = adj_mid + " " + suffix.lstrip(" ") + "\n"
    else:
        # np. ":" → zostaje na końcu pierwszej linii
        new_first = (prefix.rstrip(" ") + adj_mid + "\n")
        new_second = suffix.lstrip(" ") + "\n"

    # Składamy z powrotem: wszystkie linie przed idx, potem new_first, new_second, a potem pozostałe
    new_lines = lines[:idx] + [new_first, new_second] + lines[idx+1:]
    write_lines(path, new_lines)


def special_split_last_line_gal(base_dir, rel_path):
    """
    W ostatniej niepustej linii pliku rel_path:
    - Znajdzie pierwsze wystąpienie ". " lub ": ",
    - oddzieli ten znak interpunkcyjny ('.' lub ':') i pozostawi go na końcu pierwszej linii,
    - resztę tekstu po wzorcu przeniesie do nowej drugiej linii.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    lines = read_lines(path)
    last_idx = len(lines) - 1
    while last_idx >= 0 and lines[last_idx].strip() == "":
        last_idx -= 1
    if last_idx < 0:
        return

    original = lines[last_idx].rstrip("\n")
    pattern = r"\.\s+|:\s+"          # szukamy kropki/spacji lub dwukropka/spacji
    match = re.search(pattern, original)
    if not match:
        return

    start, end = match.span()
    prefix = original[:start]        # wszystko przed kropką/dwukropkiem
    mid    = original[start:end]     # to będzie ". " lub ": "
    suffix = original[end:]          # reszta tekstu po spacji

    mid_stripped = mid.rstrip(" ")   # "." lub ":"
    # Jeśli mid_stripped to dokładnie jeden znak interpunkcyjny ('.' lub ':'), 
    # zostawiamy go w nowej treści pierwszej linii:
    if mid_stripped in (".", ":"):
        new_first  = prefix.rstrip(" ") + mid_stripped + "\n"
        new_second = suffix.lstrip(" ") + "\n"
    else:
        # w tym algorytmie ten przypadek nie powinien wystąpić, bo wzorzec zawsze ". " albo ": "
        new_first  = prefix.rstrip(" ") + "\n"
        new_second = mid_stripped + suffix.lstrip(" ") + "\n"

    tail = lines[last_idx+1:]  # ewentualne puste linie po oryginalnej ostatniej
    new_lines = lines[:last_idx] + [new_first, new_second] + tail
    write_lines(path, new_lines)


def special_split_last_line_acts(base_dir, rel_path):
    """
    W ostatniej niepustej linii pliku rel_path:
    - Znajdzie pierwsze wystąpienie ". ",
    - oddzieli ten znak interpunkcyjny "." i pozostawi go na końcu pierwszej linii,
    - resztę tekstu po wzorcu przeniesie do nowej drugiej linii.
    """
    path = os.path.join(base_dir, rel_path)
    if not os.path.isfile(path):
        print(f"  [WARN] Nie znaleziono pliku: {rel_path}")
        return

    lines = read_lines(path)
    last_idx = len(lines) - 1
    while last_idx >= 0 and lines[last_idx].strip() == "":
        last_idx -= 1
    if last_idx < 0:
        return

    original = lines[last_idx].rstrip("\n")
    pattern = r"\.\s+"          # szukamy kropki/spacji
    match = re.search(pattern, original)
    if not match:
        return

    start, end = match.span()
    prefix = original[:start]        # wszystko przed kropką/dwukropkiem
    mid    = original[start:end]     # to będzie ". "
    suffix = original[end:]          # reszta tekstu po spacji

    mid_stripped = mid.rstrip(" ")   # "." lub ":"
    # Jeśli mid_stripped to dokładnie '.', 
    # zostawiamy go w nowej treści pierwszej linii:
    if mid_stripped in ("."):
        new_first  = prefix.rstrip(" ") + mid_stripped + "\n"
        new_second = suffix.lstrip(" ") + "\n"
    else:
        # w tym algorytmie ten przypadek nie powinien wystąpić, bo wzorzec zawsze ". "
        new_first  = prefix.rstrip(" ") + "\n"
        new_second = mid_stripped + suffix.lstrip(" ") + "\n"

    tail = lines[last_idx+1:]  # ewentualne puste linie po oryginalnej ostatniej
    new_lines = lines[:last_idx] + [new_first, new_second] + tail
    write_lines(path, new_lines)


def main():
    base = detect_base_dir()
    
    # Kategoria 1: MERGE_LAST (połączenie dwóch ostatnich linii)
    for rel in MERGE_LAST:
        # print(f"→ Merge last verse w: {rel}")
        merge_last_verse(base, rel)

    # Kategoria 1b: MERGE_PAIRS (połączenie konkretnych linii)
    for rel, line_num in MERGE_PAIRS:
        # print(f"→ Merge pair lines {line_num} & {line_num+1} w: {rel}")
        merge_pair_lines(base, rel, line_num)

    # Kategoria 2a: MERGE_FIRST2 (pierwsze 2 linie)
    for rel in MERGE_FIRST2:
        # print(f"→ Merge first 2 lines w: {rel}")
        merge_first_n_lines(base, rel, 2)

    # Kategoria 2b: MERGE_FIRST3 (pierwsze 3 linie)
    for rel in MERGE_FIRST3:
        # print(f"→ Merge first 3 lines w: {rel}")
        merge_first_n_lines(base, rel, 3)

    # Kategoria 3: CURRENT_TO_PREV
    for rel in CURRENT_TO_PREV:
        # print(f"→ Current first→Prev w: {rel}")
        current_first_n_lines_to_prev_end(base, rel, 1)

    # Kategoria 3a: CURRENT_FIRST3_TO_PREV
    # print(f"→ Current first 3→Prev w: {CURRENT_FIRST3_TO_PREV[0]}")
    current_first_n_lines_to_prev_end(base, CURRENT_FIRST3_TO_PREV[0], 3)

    # Kategoria 4: CURRENT_LAST_N_LINES_TO_NEXT_BEGIN
    for rel, n in CURRENT_LAST_N_LINES_TO_NEXT_BEGIN.items():
        # print(f"→ Current last {n} lines: {rel} → begin of the next file")
        move_last_n_to_next(base, rel, n, merge_with_first=False)

    # Kategoria 4a: CURRENT_LAST_N_LINES_TO_NEXT_BEGIN_MERGE
    for rel, n in CURRENT_LAST_N_LINES_TO_NEXT_BEGIN_MERGE.items():
        # print(f"→ Current last {n} lines: {rel} → begin of the next file with merge")
        move_last_n_to_next(base, rel, n, merge_with_first=True)

    # Kategoria 5: SPLIT_LINE; pattern = ": "
    # print("→ Split line 30 of 24-ier/29.txt")
    split_line(base_dir=base, rel_path="24-ier/29.txt", line_number=30, pattern=r":\s+")

    # Kategoria 6: SPLIT_LINE; pattern = ". "
    # print("→ Split line 11 of 47-cor/13.txt")
    split_line(base_dir=base, rel_path="47-cor/13.txt", line_number=11, pattern=r"\.\s+")

    # Kategoria 7a: SPLIT_LINE; pattern = "będę"
    # print("→ Split last line of 19-psa/013.txt")
    split_line(base_dir=base, rel_path="19-psa/013.txt", line_number=5,pattern=r"będę", capitalize=True)

    # Kategoria 7a: SPLIT_LINE; pattern = "alem"/"Alem"
    # print("→ Split last line of 47-cor/11.txt")
    split_line(base_dir=base, rel_path="47-cor/11.txt", line_number=32, pattern=r"(?i)alem", capitalize=True, case_insensitive=True)

    # Kategoria 8: SPECIAL_SPLIT_LAST_LINE_GAL; pattern = ". " lub ": "
    # print("→ Special split last line of 48-gal/01.txt")
    special_split_last_line_gal(base_dir=base, rel_path="48-gal/01.txt")

    # Kategoria 9: SPECIAL_SPLIT_LAST_LINE_ACTS; pattern = ". "
    # print("→ Special split last line of 44-act/19.txt")
    special_split_last_line_acts(base_dir=base, rel_path="44-act/19.txt")

    # print("\nPomyslnie zakonczono modyfikacje.")


if __name__ == "__main__":
    main()
