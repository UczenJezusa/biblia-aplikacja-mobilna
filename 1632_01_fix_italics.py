import os
import pathlib
import re

# Mapowanie znaków do zamiany
REPLACEMENTS = {
    "</> ": "</i> ",
    "<> ": "</i> ",
    "<i> ": "</i> ",
    "<i/>": "</i>",
    " <>": " <i>"
}

def modify_text(line, file_path, line_number, changes_log):
    """Modyfikuje linie według reguł zamiany i loguje zmiany"""
    modified = False
    for old, new in REPLACEMENTS.items():
        if old in line:
            line = line.replace(old, new)
            changes_log.append((file_path, line_number, old, new))
            modified = True
    return line, modified

def check_tagging_errors(line, file_path, line_number, errors_log):
    """Sprawdza błędne tagowanie <i> i </i>"""

    open_tags = [m.start() for m in re.finditer(r"<i>", line)]
    close_tags = [m.start() for m in re.finditer(r"</i>", line)]
    
    # Więcej otwierających niż zamykających → brakuje </i>
    if len(open_tags) > len(close_tags):
        errors_log.append((file_path, line_number, "Brakujace </i>", line.strip()))
    # Więcej zamykających niż otwierających → brakuje <i>
    elif len(close_tags) > len(open_tags):
        errors_log.append((file_path, line_number, "Brakujace <i>", line.strip()))

    # Sprawdzamy, czy tagi są poprawnie naprzemiennie ułożone
    all_tags = sorted(open_tags + close_tags)  # Lista wszystkich pozycji tagów
    
    if len(all_tags) % 2 != 0:  # Jeśli liczba tagów nieparzysta, to błąd
        errors_log.append((file_path, line_number, "Nieparzysta liczba tagow <i>", line.strip()))
    
    else:
        # Naprzemienność tagów <i> i </i>
        for i in range(0, len(all_tags) - 1, 2):
            if all_tags[i] in close_tags:  # Jeśli pierwszy w parze jest </i>, to błąd
                errors_log.append((file_path, line_number, "Bledna kolejnosc tagow <i></i>", line.strip()))
                break

def process_txt_files(directory):
    base_dir = pathlib.Path(directory).resolve()  # Ścieżka bazowa (bieżący katalog)
    changes_log = []  # Log zamian
    errors_log = []   # Log błędów tagowania

    for root, _, files in os.walk(directory):
        root_path = pathlib.Path(root).resolve()
        
        # Pomijamy katalog główny (tylko przeszukujemy podfoldery)
        if root_path == base_dir:
            continue

        for file in files:
            if file.endswith(".txt"):
                file_path = root_path / file
                modified = False
                new_lines = []

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i, line in enumerate(lines):
                    new_line, changed = modify_text(line, file_path, i + 1, changes_log)
                    check_tagging_errors(new_line, file_path, i + 1, errors_log)
                    new_lines.append(new_line)
                    if changed:
                        modified = True

                if modified:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(new_lines)

    return changes_log, errors_log

if __name__ == "__main__":
    folder = pathlib.Path(__file__).parent  # Katalog, w którym znajduje się skrypt
    changes, errors = process_txt_files(folder)

    # Wypisujemy zmiany dokonane w plikach
    if changes:
        print(f"Pomyslnie poprawiono {len(changes)} tagowan kursywy:")
        for file_path, line_number, old, new in changes:
            print(f"{file_path} (Linia {line_number}): '{old}' -> '{new}'")
    else:
        print("Nie wykonano zadnych poprawek tagowan kursywy.")

    # Wypisujemy znalezione błędy w tagowaniu
    if errors:
        print(f"\nWykryto {len(errors)} bledow tagowania:")
        for file_path, line_number, error, line_content in errors:
            print(f"{file_path} (Linia {line_number}): Uwaga nalezy poprawic [{error}] → {line_content}")
    else:
        print("\nBrak bledow tagowania.")
