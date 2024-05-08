# IndentNav #

* Autor: Tony Malykh
* Pobierz [wersja stabilna][1]

Ten dodatek pozwala użytkownikom NVDA nawigować po poziomach wcięcia,
częściach akapitu lub całych akapitach. W przeglądarkach, pomaga znaleźć
akapity oddalone o tę samą odległość od lewej krawędzi ekranu, takie jak
komentarze pierwszego poziomu w hierarchicznym drzewie komentarzy. Podczas
edycji kodu źródłowego w wielu językach programowania, można przeskakiwać
między wierszami o tym samym poziomie wcięcia, jak również szybko odnajdywać
wiersze  o wyższym lub niższym poziomie wcięcia.

## Używanie w przeglądarkach
IndentNav można używać do nawigowania po akapitach oddalonych o konkretną
odległość od lewej krawędzi ekranu. Przede wszystkim, można nacisnąć
NVDA+Alt+Strzałka w dół lub w górę, aby przeskoczyć do następnego lub
poprzedniego akapitu oddalonego od lewej krawędzi ekranu o tę samą
odległość. przydaje się to podczas przeglądania hierarchicznych drzew
komentarzy (np. na reddit.com) do przeskakiwania między komentarzami
pierwszego poziomu z pominięciem wszystkich komentarzy wyższych poziomów.

Ściśle mówiąc, IndentNav można używać w każdej aplikacji, dla której NVDA
dostarcza interceptora drzewa.

Skróty klawiszowe:

* NVDA+Alt+Strzałka w górę lub w dół: przeskakuje do poprzedniego lub
  następnego akapitu oddalonego o tę samą odległość od lewej krawędzi
  ekranu.
* NVDA+alt+Strzałka w lewo: przeskakuje do poprzedniego akapitu oddalonego o
  mniejszą odległość od lewej krawędzi ekranu.
* NVDA+Alt+Ssrzałka w prawo: przeskakuje do następnego akapitu oddalonego o
  większą odległość od lewej krawędzi ekranu.

## Używanie w edytorach tekstu
IndentNav przydaje się również podczas edycji kodu źródłowego w wielu
językach programowania.  W językach takich jak Python, kod źródłowy
koniecznie musi mieć odpowiednio zrobione wcięcie. W przypadku wielu innych
języków programowania, także poleca się o to zadbać.  Używając IndentNav,
można nacisnąć NVDA+Alt+Strzałka w dół lub w górę, aby przeskoczyć do
następnego lub poprzedniego wiersza o tym samym poziomie wcięcia.  Można też
nacisnąć NVDA+Alt+Strzałka w lewo, aby przeskoczyć do wiersza nadrzędnego,
czyli poprzedniego wiersza o niższym poziomie wcięcia.  W Pythonie można
łatwo znaleźć aktualną definicję funkcji lub definicję klasy.  Można również
nacisnąć NVDA+Alt+Strzałka w prawo, aby przejść do pierwszego podrzędnego
elementu danego wiersza, czyli następnego wiersza o wyższym poziomie
wcięcia.

Jeśli w NVDA ustawiono wyrażanie wcięcia wiersza za pomocą dźwięków,
IndentNav szybko odtworzy dźwięki wszystkich pominiętych wierszy.  Jeżeli
będzie ich dużo, dodatek odtworzy same początki dźwięków, aby tylko
zasygnalizować liczbę pominiętych wierszy.

Skróty klawiszowe:

* NVDA+Alt+Strzałka w górę lub w dół: przeskakuje do poprzedniego lub
  następnego wiersza o tym samym poziomie wcięcia w obrębie aktualnego bloku
  o tym samym poziomie wcięcia.
* NVDA+Alt+Control+Strzałka w górę lub w dół: wymusza przeskok do
  poprzedniego lub następnego wiersza o tym samym poziomie wcięcia. W razie
  potrzeby, używając tego polecenia można przeskoczyć do innych bloków o tym
  samym poziomie wcięcia, takich jak inne funkcje Pythona.
* NVDA+alt+Strzałka w lewo: przeskakuje do nadrzędnego wiersza, czyli do
  poprzedniego wiersza o niższym poziomie wcięcia.
* NVDA+Alt+Strzałka w prawo: przeskakuje do pierwszego wiersza podrzędnego,
  czyli do następnego wiersza o wyższym poziomie wcięcia w obrębie bloku o
  tym samym poziomie wcięcia.

## Historia wersji
* [v1.2](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.2.nvda-addon)
  * Dodano wsparcie dla użytkowania międzynarodowego.
  * Dodano nagłówki licencji GPL w plikach źródłowych.
  * Drobne poprawki.
* [v1.1](https://github.com/mltony/nvda-indent-nav/raw/master/releases/IndentNav-1.1.nvda-addon)
  * Wersja pierwotna.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=indentnav
