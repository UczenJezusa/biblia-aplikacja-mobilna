# Instrukcja tworzenia pliku Biblii Gdańskiej w formacie przyjaznym aplikacjom mobilnym

### Wstęp

**Celem projektu jest umieszczenie współczesnej rewizji tekstu Biblii Gdańskiej w aplikacjach mobilnych oraz portalach internetowych.**

Ze względu na trwające poprawki w tekście cyfrowym pisma świętego (https://github.com/piotrskurzynski/biblia), sensowność projektu ogranicza się do:
- aktualizowanie tekstu z wydania 1879 roku np. co rok, dwa lata w aplikacjach mobilnych,
- czekanie na współczesną rewizję Biblii Gdańskiej, a potem stworzenie finalnego pliku biblii rewizji współczesnej używając niżej opisanych skryptów (możliwe wymagane zmiany w oprogramowaniu w celu prawidłowego działania - więcej informacji niżej).

Aby teskt biblii był poprawnie wyświetlany w mobilnych aplikacjach biblijnych (np. "mybible" czy "MySword") jej sumaryczna ilość linii (wersetów) musi równać się ilości linii biblii King James Version (KJV). Biblia Gdańska oryginalnie ma trochę więcej wersetów. Wyjściowy plik biblii uzyskany po wykonaniu poniższych skryptów, zawiera ilość linii (wersetów) zgodną z KJV.

UWAGA!<br>
Aktualnie niniejsza instrukcja działa tylko dla tekstu z rewizji z 1879 roku. Informacje o możliwym prawidłowym działaniu w przyszłości dla tekstu z 1632 roku można znaleźć w pliku `INFO - UPDATE 1632.txt` w katalogu `Rozwój oprogramowania`.

Stworzenie pliku biblii dla współczesnej rewizji będzie najbardziej zbliżone do tworzenia pliku na bazie tekstu z 1632 roku. Lista rzeczy które należy zmienić w oprogramowaniu dla pliku biblii z 1632 roku tak, aby wyjściowy plik był poprawnie tworzony dla współczesnego wydania, obejmuje np.:
- zmiany w skrypcie `01_kjv_verse_align.py` (szczegóły niżej),
- nie używanie skryptu `1632_02_orthography.py`.

Poniżej znajduje się instrukcja jak z plików tekstowych biblii uzyskać plik typu The Word z rozszerzeniem `.ont`, kompatybilny z biblijnymi aplikacjami mobilnymi. Uzyskany plik można udostępnić moderatorom aplikacji mobilnych (np. kontakt poprzez wiadomość email; dla wordproject.org same pliki tekstowe biblii są wystarczające). Dzięki temu można w prosty i szybki sposób zaktualizować cały tekst biblii dostępny w aplikacji mobilnej.

Sprawdzone działanie na Windows, lecz nie powinno być problemów z innymi systemami operacyjnymi (W terminalu Linux skrypty uruchamia się używając `/` zamiast `\`). Poniższa instrukcja opisana jest dla systemu operacyjnego Windows.

### 1. Przygotowanie

- Wypakuj plik ZIP "Instrukcja - biblia w aplikacji mobilnej" w wybranym przez siebie folderze. W przypadku czytania tej instrukcji z poziomu platformy GitHub, należy najpierw pobrać pliki zamieszczone na GitHubie z https://github.com/UczenJezusa/biblia-aplikacja-mobilna poprzez wybranie zielonej ikony z napisem `Code` -> `Download ZIP`. Następnie wypakować plik ZIP w wybranym przez siebie folderze.
- Umieść w wypakowanym folderze (od tej pory nazywany on będzie folderem ze skryptami) folder biblii zawierający pliki tekstowe ze zdalnego repozytorium na Github'ie: https://github.com/piotrskurzynski/biblia - na stronie internetowej pobrać i wypakować plik ZIP analogicznie do opisu wyżej i skopiować folder `1879` lub `1632` do folderu ze skryptami.
	
UWAGA 1:<br>
W danym momencie może znajdować się tylko jeden z wyżej wymienionych folderów w folderze ze skryptami. W przeciwnym przypadku skrypt nie dokona modyfikacji na plikach i wyświetli stosowny komunikat.

UWAGA 2:<br>
~~~~
W niniejszym pliku występują fragmenty kodu lub komend oznaczone na początku
i końcu znakami np. ```html, ```powershell, ``` lub `.
Są one widoczne w przypadku wyświetlania pliku w programie który nie obsługuje
kodowania plików z rozszerzeniem .md, np. w Notatniku czy NotePad++.
W przypadku kopiowania takich fragmentów kodu lub komend,
należy pominąć te oznaczenia.
~~~~

- Przy pierwszym uruchamianiu skryptu w terminalu PowerShell może być wymagane włączenie możliwości ich uruchamiania w WindowsPowerShell:
w tym celu uruchom Windows PowerShell jako administrator (żeby znaleźć program można w dolnym pasku, w polu wyszukiwania wpisać frazę `Windows PowerShell`)
Następnie wprowadź komendę i naciśnij Enter:
```powershell
Set-ExecutionPolicy RemoteSigned
```

Dla łatwiejszego wprowadzania poniższych komend, można po prostu skopiować i wkleić komendę. Wklejanie tekstu do terminala PowerShell może działać na dwa sposoby: `Ctrl + V` i/lub prawy przycisk myszy.

- Po uruchomieniu terminala przejść do folderu ze skryptami np. żeby przejść na dysk D: wpisać komendę i nacisnąć Enter:
```powershell
cd D:
```

A potem poniższą komendę aby przejść do folderu ze skryptami (wpisać swoją ścieżkę):
```powershell
cd tutaj/sciezka/do/mojego/folderu
```

Można używać klawisza `Tab` do łatwego uzupełniania niepełnej nazwy folderu/skryptu.

---

### 2. [dla tekstu z 1632 roku] Poprawa kursywy oraz ortografia (jeśli dokonuje się zmian nad tekstem z 1879, należy pominąć ten punkt i przejść do następnego)

- Poprawa kursywy oraz ortografia:
W terminalu uruchomić polecenie (wklej poniższy tekst do terminala PowerShell i naciśnij Enter):
```powershell
python .\1632_01_fix_italics.py
```

Jeśli pojawi się komunikat `Wykryto n bledow tagowania`, należy poprawić ręcznie podane linie tekstu: otworzyć wymieniony w komunikacie plik .txt znaleźć stosowną linię, porównać z oryginałem skanu (szczegóły: https://github.com/piotrskurzynski/biblia/blob/main/info.md) i nanieść zmianę.
Najlepiej dodatkowo od razu zgłosić na podanej stronie internetowej błąd.
Możliwe że pojawi się więcej komunikatów odnoszących się do tej samej linii tekstu - wówczas wystarczy poprawić tylko tę jedną linię.
Dla pewności można uruchomić powyższy skrypt jeszcze raz - powinien pojawić się komunikat:`Brak bledow tagowania.` - w takiej sytuacji można przejść do kolejnego kroku:

Uruchomić kolejny skrypt komendą:
```powershell
python .\1632_02_orthography.py
```

Pomyślna modyfikacja jest potwierdzona pokazaniem się komunikatu: `Pomyslnie zmieniono ortografie.`


### 3. Uzyskanie pliku w formacie The Word

Po przejściu do folderu ze skryptami w terminalu, uruchomić polecenie (wklej poniższy tekst do terminala PowerShell i naciśnij Enter):
```powershell
python .\03_generate_merged_original_bible_file.py; if ($?) { python .\01_kjv_verse_align.py; if ($?) { python .\02_generate_ont_file.py } }
```

UWAGA!
Niektóre modyfikacje w skrypcie `01_kjv_verse_align.py` zależą od konkretnych znaków w tekście. Zatem przy pracy nad tekstem rewizji współczesnej (nie 1879 czy 1632, ale 20nn) należy upewnić się czy skrypt poprawnie modyfikuje pliki wymienione na końcu tego pliku*.

Pomyślna modyfikacja jest wtedy, gdy pojawią się TYLKO napis `Pomyslnie zakonczono modyfikacje i utworzono plik: PBG_the_word.ont.`

Na tym etapie wyjściowy plik biblii `PBG_the_word.ont` powinien zawierać dokładnie 31 102 niepuste linie tekstu (nie licząc opisu na końcu biblii) - dokładnie tyle ile ich zawiera biblia KJV. 
Należy to sprawdzić uruchamiając plik np. w Notatniku (prawy przycisk myszy na nazwie pliku -> `Otwórz za pomocą...` -> `Więcej aplikacji` -> wybrać np. `Notatnik`). W przypadku używania aplikacji Notatnik w dolnym pasku wyświetla się liczba linii w której aktualnie się znajduje użytkownik. Przejść do koniec pliku tekstowego i sprawdzić czy dla kursora znajdującego się w ostatniej niepustej linii (poza opisem na końcu pliku), wartość Lin to 31 102.

Jeśli numeracja się zgadza, warto jeszcze przetestować czy powyższe modyfikacje nie zmieniły ilości znaków w tekście.

### 4. Testowanie wprowadzonych modyfikacji

Aby przetestować czy liczba znaków przed i po modyfikacji jest taka sama, należy uruchomić skrypt:
```powershell
python .\test_none_of_the_characters_fell.py
```

Jeśli po wykonaniu skryptu ukazuje się komunikat o identycznej ilości znaków, plik jest gotowy do udostępnienia go moderatorom poszczególnych mobilnych aplikacji biblijnych.


---

### Informacje dodatkowe

Więcej szczegółów o tym jak działają skrypty i możliwości ich modyfikacji można znaleźć w poszczególnych skryptach `*.py` w oraz plikach w katalogu `Rozwój oprogramowania`.



* Lista plików których modyfikacja zależy od konkretnego znaku w tekście. Numeracja odpowiada kategoriom w skrypcie `01_kjv_verse_align.py`:
5) wstawić nową linię po pierwszym wystąpieniu ": " w linii 30. Dodatkowo usunąć z ": " spację.
24-ier/29.txt

6) to samo ale po wystąpieniu kropki w linii 11:
47-cor/13.txt

7) po niżej wymienionej frazie, resztę tekstu z ostatniej linii przenieś do nowej następnej linii, wraz z tą frazą, zamieniając wyraz we frazie na pisany z dużej litery. Dodatkowo usunąć spację będącą przed frazą.
19-psa/013.txt przed "będę" wstaw nową linię
47-cor/11.txt przed "alem" wstaw nową linię, nie bierz pod uwagę wielkości liter słowa "alem"

8) w ostatniej linii po wystąpieniu ". " lub ": " resztę tekstu przenieść do nowej następnej linii. Dodatkowo usunąć spację z ". " lub ": ".
48-gal/01.txt

9) to samo co 8) ale po wystąpieniu ". ":
44-act/19.txt
