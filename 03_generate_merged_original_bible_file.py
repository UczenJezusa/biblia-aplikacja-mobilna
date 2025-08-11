import os
from pathlib import Path
import re

def detect_base_dir():
    cwd = os.getcwd()
    dirs = [d for d in ("1879", "1632") if os.path.isdir(os.path.join(cwd, d))] # do dodania rok współczesnej rewizji: ,"20nn"
    if len(dirs) == 0:
        raise FileNotFoundError(
            "Nie znaleziono folderu '1879', '1632' ani katalogu w formacie '20nn' w biezacym katalogu."
        )
    
    if len(dirs) > 1:
        raise Exception(
            "Znaleziono wiecej niż jeden folder z plikami tekstowymi biblii. "
            "Zostaw w biezacym katalogu tylko jeden z: '1879', '1632' lub '20nn'."
        )

def main():
    detect_base_dir()

    current_folder = Path.cwd()
    output_file = current_folder / "PBG_original.txt"

    # Wzorzec dopasowujący foldery składające się wyłącznie z cyfr
    digit_only_pattern = re.compile(r"^\d+$")

    with output_file.open("w", encoding="utf-8") as out_f:
        # Tylko bezpośrednie podfoldery z nazwą z cyfr
        digit_folders = sorted(
            [f for f in current_folder.iterdir() if f.is_dir() and digit_only_pattern.match(f.name)],
            key=lambda f: int(f.name)
        )

        for folder in digit_folders:
            # Przeszukujemy REKURENCYJNIE wszystkie pliki .txt w tym folderze i jego podkatalogach
            txt_files = sorted(folder.rglob("*.txt"))
            for txt_file in txt_files:
                with txt_file.open(encoding="utf-8") as f:
                    content = f.read().rstrip()  # Usuń zbędne puste linie z końca
                    out_f.write(content + "\n")  # Dodaj zawartość i nową linię

    # print("Pliki zostały pomyślnie połączone do PBG_original.txt.")

if __name__ == "__main__":
    main()
