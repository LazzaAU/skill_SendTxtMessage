
### Wyślij wiadomość tekstową

## Do czego służy ta umiejętność?

Początkowo ta umiejętność została zaprojektowana z myślą o bardziej dojrzałych użytkownikach, którzy mogą paść ofiarą upadku
i nie jest w stanie wstać. Mając to na uwadze, mogli wezwać Alice i powiedzieć „pomóż upadłem” lub kilka innych
wypowiedzi, a Alicja wyszuka skonfigurowane kontakty alarmowe i wyśle ​​im wiadomość SMS za pośrednictwem
e-mail SMTP lub za pośrednictwem wiadomości Telegram w zależności od platformy wybranej przez użytkownika.

Jednak pisząc umiejętność, pomyślałem, że nie ma powodu, dla którego nie mógłbyś użyć go do wysłania generała
wiadomość SMS lub telegram przez Alicję do kogoś. Więc to też robi, ale istnieją ograniczenia.

1. Ani SMS, ani Telegram nie będą akceptować odpowiedzi od ludzi, więc jest to system wiadomości jednokierunkowych
2. Szczególnie za pośrednictwem wiadomości SMS, chociaż może to oznaczać, że wiadomość została wysłana, nie ma gwarancji, że odbiorca faktycznie ją otrzymał
ze względu na limity wysyłania wiadomości za darmo.
3. Funkcja SMS jest dostępna tylko w niektórych krajach, takich jak Ameryka i Kanada.
Na przykład Australia nie ma darmowych bramek SMS. Więc ponieważ Telegram jest oparty na Internecie
nie ma żadnych ograniczeń, dlatego jest dostępny dla każdego.
4. Umiejętność polega na tym, że odbiorca ma imię wymienione w slocie Alicja/Imię.
Dla Australijczyków, którzy nazywają wszystkich „ol mate, shazza, bazza i milion innych slangów, to umiejętność
nie zadziała, jeśli nie podasz odbiorcy imienia z listy , np. Sue, Barry, Richard itp.
Pewnego dnia może to naprawię, ale to przyszła myśl :)

## Konfiguracja umiejętności

1. Jeśli nie masz zainstalowanego Telegrama ORAZ wprowadzasz dane w polu „Szczegóły odbiorcy telegramu” w polu
ustawienia umiejętności, Alice pobierze i zainstaluje Telegram podczas następnego restartu Alice. Odbywa się to w ten sposób, aby zapobiec
błędy tokena podczas uruchamiania za każdym razem, gdy Telegram miał być instalowany jako zależność, a mimo to nie został wprowadzony token Telegrama
ze względu na to, że użytkownik nie ma konta Telegram.
2. Wszystkie pola zostają zapisane w bazie danych po kliknięciu „potwierdź”

W ustawieniu umiejętności:

### *Dla funkcji SMS*

Wejdź w pole "Szczegóły nadawcy SMS - Twoje dane jako nadawcy... format= Imię/email/hasło e-mail"
- Przykład:
  - Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
możesz dodać tyle, ile chcesz, po prostu oddziel je przecinkami, jak w powyższym przykładzie.
Dane te zostaną później wykorzystane do zalogowania się na konto e-mail w celu wysłania SMS-a

Wpisz w pole "Szczegóły odbiorcy SMS" - "Dane odbiorcy w formacie: Imię/Numer Telefonu/Kontakt w nagłych wypadkach/Brama SMS
- Przykład:
  - larry/08001234/tak/@txt.att.net, jezus/180098765/no/@vtext.com

Ponownie dodaj tyle, ile chcesz, ale oddziel je przecinkami.

UWAGA: do tej pory zostało to przetestowane tylko z Gmailem. aby ustawić pawword aplikacji Gmail, przejdź do [Ustawianie hasła aplikacji Google](https://support.google.com/accounts/answer/185833?hl=pl)

#### *Rozbijmy te*

format: Imię/Numer Telefonu/Kontakt w nagłych wypadkach/Brama SMS


1. Imię: - Jak wspomniano powyżej, musi to być imię i nazwisko z listy Alice/imię. To imię odbiorcy
Imię jest używane do proszenia Alicji „wyślij wiadomość tekstową do Marii” itp.

2. Numer telefonu: - To jest numer telefonu odbiorcy. Musi mieć długość „10 cyfr” i kody krajów „NIE”

3. isEmergencyContact: - Tutaj oznaczasz kogoś jako kontakt alarmowy lub nie. Wartości do dodania to „tylko”
tak lub nie. więc tak oznacza, że ​​zostaną oznaczone jako kontakt alarmowy i dlatego otrzymają wiadomość, jeśli powiesz:
Alicja, "Pomóż mi upadłem".

4. smsGateway: - Jest to bramka SMS, z której korzysta Twój odbiorca. Musisz zapytać osobę kontaktową, kto jej
operator komórkowy, a następnie sprawdź, jaka jest bramka SMS dla tego operatora. Listę można znaleźć tutaj
   [Bramki SMS Wikipedii](https://en.wikipedia.org/wiki/SMS_gateway)

Wprowadzona bramka musi mieć na początku znak @, na przykład @vtext.com


### *Dla funkcji telegramu*

Dla pola Szczegóły odbiorcy telegramu — YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact
- Przykład: larry/Mary/12345/tak

Działa to na tej samej zasadzie co odbiorca SMS, użyj tak lub nie dla isEmergencyContact i kontaktów
telegramId dla "ichChatId"

#### *Identyfikator lokalizacji Alicji*

Wprowadź możliwą do zidentyfikowania lokalizację, w której mieszka Alicja, aby inne osoby mogły zrozumieć, kiedy zostanie wysłana wiadomość alarmowa
a Alicja nie rozpoznaje, kto wykrzyknął prośbę, ta nazwa lokalizacji zostanie użyta do pomocy
wyjaśnić wiadomość odbiorcy.

Przykład: - „Cześć, kontakt alarmowy, ktoś w „domu Mike'a Prattsa” upadł i potrzebuje natychmiastowej pomocy”

Gdzie "dom Mike'a Prattsa" mógłby być "farmą bobslejów", "susans Caravan", "miejscem jacks na Bourbon Street" itp.

#### *Potwierdź połączenie alarmowe*

Włącz tę opcję, aby wyświetlić monit, jeśli chcesz wysłać wiadomość pomocy przed jej wysłaniem.
Wyłączenie tej opcji może spowodować wysłanie wiadomości pomocy do kontaktów alarmowych, jeśli Alice pewnego dnia Cię nie zrozumie
prosząc o pomoc w czymś zupełnie niezwiązanym :)

#### x Tryb testowy

Włącz tę opcję, aby uruchomić umiejętność w trybie testowym. W trybie testowym umiejętność będzie działać normalnie, ALE..
nie wyśle ​​żadnej rzeczywistej wiadomości. Wyświetli tylko to, co zostanie wysłane w dzienniku systemowym Alicji.

### UWAGA DOTYCZĄCA BEZPIECZEŃSTWA
Moja sugestia, po wpisaniu pola „Dane nadawcy” i zadowoleniu z tych danych, należy kliknąć „potwierdź”
następnie następnym razem, gdy wyłączysz Alice, przejdź do folderu umiejętności SendTextMessage, otwórz plik config.json.template i zmień
„polecenie”
"smsSenderDetails": {
"domyślna wartość": "",
"DataType" : "string",
"isSensitive" : prawda,
````
isSensitive na true ( od domyślnego false).

*Powód* : Zmiana tej wartości na „prawda” spowoduje, że pole będzie wyświetlane ********** w interfejsie użytkownika, a tym samym będzie chronić twoje
hasło e-mail, aby było widoczne w gui. Domyślne pozostawienie tego jako true sprawia, że ​​trudniej jest zobaczyć, co tam piszesz,
więc z tego powodu zostawiłem to jako fałszywe, dopóki nie wymyślę alternatywnego planu :)