import os
import pathlib

# Mapowanie znaków do zamiany
REPLACEMENTS = {
    "°": "go",
    " :": ":",
    " ;": ";",
    " /": ",",
    "ƺ": "sz",
    "ó": "o",
    "Ó": "O",
    "( ": "(",
    " )": ")",
    " ?": "?",
    " !": "!"
}

def modify_text(content):
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
    return content

def process_txt_files(directory):
    base_dir = pathlib.Path(directory).resolve()  # Ścieżka bazowa (bieżący katalog)

    for root, _, files in os.walk(directory):
        root_path = pathlib.Path(root).resolve()
        
        # Pomijamy katalog główny (tylko przeszukujemy podfoldery)
        if root_path == base_dir:
            continue

        for file in files:
            if file.endswith(".txt"):
                file_path = root_path / file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                modified_content = modify_text(content)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(modified_content)

if __name__ == "__main__":
    folder = pathlib.Path(__file__).parent  # Katalog, w którym znajduje się skrypt
    process_txt_files(folder)
    print("Pomyslnie zmieniono ortografie.")
