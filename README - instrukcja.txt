### Wstęp

UWAGA!
Aktualnie niniejsza instrukcja działa tylko dla tekstu z rewizji z 1879 roku. Informacje o możliwym prawidłowym działaniu w przyszłości dla tekstu z 1632 roku można znaleźć w pliku "INFO - UPDATE 1632.txt" pod katalogiem "Rozwój oprogramowania".
Również w przypadku chęci użycia kodu do współczesnej rewizji tekstu 20nn rok, należy zapoznać się z całą niniejszą instrukcją oraz wymagane są zmiany w kodzie co najmniej skryptu 01-align-to-kjv-verses-structure.py

Niniejsza instrukcja pokazuje jak z plików tekstowych biblii uzyskać plik typu The Word z rozszerzeniem *.ont, kompatybilny z biblijnymi aplikacjami mobilnymi. Uzyskany plik można udostępnić moderatorom aplikacji mobilnych (np. kontakt poprzez wiadomość email). Dzięki temu można w prosty i szybki sposób zaktualizować cały tekst biblii dostępny w aplikacji mobilnej.

Sprawdzone działanie na Windows, lecz nie powinno być problemów z innymi systemami operacyjnymi. Poniższa instrukcja opisana jest dla systemu operacyjnego Windows.

Aby biblia była poprawnie wyświetlana w mobilnych aplikacjach biblijnych (np. "mybible" czy "MySword") jej sumaryczna ilość linii (wersetów) musi równać się ilości linii biblii King James Version (KJV). Biblia Gdańska oryginalnie ma trochę więcej wersetów. Wyjściowy plik biblii uzyskany po wykonaniu skryptów, zawiera ilość linii (wersetów) zgodną z KJV.

=========================================

### 1. Przygotowanie.


- Wypakuj plik ZIP "Instrukcja - biblia w aplikacji mobilnej" w wybranym przez siebie folderze.
- Umieść w wypakowanym folderze (od tej pory nazywany on będzie folderem ze skryptami) folder biblii zawierający pliki tekstowe ze zdalnego repozytorium na Github'ie:
	można to zrobić wchodząc na stronę internetową https://github.com/piotrskurzynski/biblia
	potem wybrać zieloną ikonę z napisem "Code" -> Download ZIP.
	Następnie wypakować plik ZIP i skopiować folder "1632" lub "1879" do folderu ze skryptami.
	
UWAGA!
W danym momencie może znajdować się tylko jeden z wyżej wymienionych folderów w folderze ze skryptami. W przeciwnym przypadku skrypt nie dokona modyfikacji na plikach i wyświetli stosowny komunikat.

- Używając systemu operacyjnego Windows, uruchom terminal PowerShell. Terminal można znaleźć wpisując w pasku wyszukiwania systemu Windows "PowerShell".
- Po uruchomieniu terminala przejść do folderu ze skryptami (np. wpisanie "cd D:" i naciśnięcie Enter żeby przejść na dysk D:, a potem cd tutaj/sciezka/do/mojego/folderu aby przejść do konkretnego folderu)
Można używać klawisza Tab do łatwego uzupełniania niepełnej nazwy folderu/skryptu.

Dla łatwiejszego wprowadzania poniższych komend, można po prostu skopiować i wkleić komendę. Wklejanie tekstu do terminala PowerShell może działać na dwa sposoby: Ctrl + V i/lub prawy przycisk myszy.

- Przy pierwszym uruchamianiu skryptu w terminalu PowerShell może być wymagane włączenie możliwości ich uruchamiania w WindowsPowerShell:
w tym celu uruchom Windows PowerShell jako administrator (żeby znaleźć program można w dolnym pasku, w polu wyszukiwania wpisać frazę "Windows PowerShell")
Następnie wprowadź komendę i naciśnij enter:
Set-ExecutionPolicy RemoteSigned

----------------

### 2. W przypadku pracy nad tekstem z 1632 roku: (jeśli dokonuje się zmian nad tekstem z 1879, należy pominąć ten punkt i przejść do następnego.)

- Poprawa kursywy oraz ortografia:
W terminalu uruchomić polecenie (wklej poniższy tekst do terminala PowerShell i naciśnij Enter):
python .\1632-01-poprawa-kursywy.py

Jeśli pojawi się komunikat "Wykryto n błędów tagowania", należy poprawić ręcznie podane linie tekstu: otworzyć wymieniony w komunikacie plik .txt znaleźć stosowną linię, porównać z oryginałem skanu (szczegóły: https://github.com/piotrskurzynski/biblia/blob/main/info.md) i nanieść zmianę.
Najlepiej dodatkowo od razu zgłosić na podanej stronie internetowej błąd.
Możliwe że pojawi się więcej komunikatów odnoszących się do tej samej linii tekstu - wówczas wystarczy poprawić tylko tę jedną linię.
Dla pewności można uruchomić powyższy skrypt jeszcze raz - powinien pojawić się komunikat:"Brak błędów tagowania." - w takiej sytuacji można przejść do kolejnego kroku:

Uruchomić kolejny skrypt komendą:
python .\1632-02-ortografia.py

Pomyślna modyfikacja jest potwierdzona pokazaniem się komunikatu: "Pomyslnie zmieniono ortografie.".


### 3. Uzyskanie pliku w formacie The Word.

Po przejściu do folderu ze skryptami w terminalu, uruchomić polecenie (wklej poniższy tekst do terminala PowerShell i naciśnij Enter):
python .\03-create-original-merged-bible-file.py; if ($?) { python .\01-align-to-kjv-verses-structure.py; if ($?) { python .\02-create-the-word-bible-file.py } }

UWAGA!
Niektóre modyfikacje (w skrypcie 01-align-to-kjv-verses-structure) zależą od konkretnych znaków w tekście. Zatem dla wersji z poprawkami (nie 1879 czy 1632, ale 20nn) należy upewnić się czy skrypt poprawnie modyfikuje pliki wymienione na końcu tego pliku*.

Pomyślna modyfikacja jest wtedy, gdy pojawią się >> tylko << napis "Pomyslnie zakonczono modyfikacje i utworzono plik: PBG_the_word.ont.".

Na tym etapie wyjściowy plik biblii "PBG_the_word.ont" powinien zawierać dokładnie 31 102 niepuste linie tekstu (nie licząc opisu na końcu biblii) - dokładnie tyle ile ich zawiera biblia KJV. 
Należy to sprawdzić uruchamiając plik np. w notatniku - prawy przycisk myszy na nazwie pliku -> Otwórz za pomocą... -> Więcej aplikacji -> wybrać np. Notatnik. W przypadku używania aplikacji Notatnik w dolnym pasku wyświetla się liczba linii w której aktualnie się znajduje użytkownik. Przejść do koniec pliku tekstowego i sprawdzić czy dla kursora znajdującego się w ostatniej niepustej linii, wartość Lin to 31 102.

Jeśli numeracja się zgadza, warto jeszcze przetestować czy powyższe modyfikacje nie zmieniły ilości znaków w tekście:

### 4. Testowanie wprowadzonych modyfikacji.

Aby przetestować czy liczba znaków przed i po modyfikacji jest taka sama, należy uruchomić skrypt:
python .\test_nie_upadl_zaden_znak.py

Jeśli po wykonaniu skryptu ukazuje się komunikat o identycznej ilości znaków, plik jest gotowy do udostępnienia go moderatorom poszczególnych mobilnych aplikacji biblijnych.


________________________________________________________

Więcej szczegółów o tym jak działają skrypty i możliwości ich modyfikacji można znaleźć w poszczególnych skryptach *.py w oraz plikach w katalogu "Rozwój oprogramowania"



* - Lista plików których modyfikacja zależy od konkretnego znaku w tekście. Numeracja odpowiada kategoriom w skrypcie 01-align-to-kjv-verses-structure.py:
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
