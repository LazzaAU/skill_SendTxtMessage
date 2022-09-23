
### TxtMessage senden

## Wofür wird diese Fertigkeit verwendet?

Ursprünglich wurde diese Fertigkeit für die reiferen Benutzer entwickelt, die möglicherweise einen Sturz erleiden
und kann nicht wieder aufstehen. In diesem Sinne könnten sie nach Alice rufen und sagen „Hilfe, ich bin gefallen“ oder einige andere
Äußerungen und Alice sucht nach konfigurierten Notfallkontakten und sendet ihnen entweder eine SMS-Nachricht per
E-Mail SMTP oder über eine Telegrammnachricht, je nachdem, welche Plattform der Benutzer wählt.

Als ich die Fertigkeit geschrieben habe, dachte ich jedoch, dass es keinen Grund gibt, warum man sie nicht verwenden könnte, um einen General zu schicken
Text- oder Telegrammnachricht über Alice an jemanden. Das tut es auch, aber es gibt Einschränkungen.

1. Weder SMS noch Telegramm akzeptieren Antworten von Personen, es handelt sich also um ein Einweg-Nachrichtensystem
2. Vor allem per SMS, auch wenn es heißt, dass die Nachricht gesendet wurde, gibt es keine Garantie dafür, dass der Empfänger sie tatsächlich erhalten hat
aufgrund von Einschränkungen beim kostenlosen Senden von Nachrichten.
3. Die SMS-Funktion ist nur in einigen Ländern wie Amerika und Kanada verfügbar.
Länder wie Australien zum Beispiel haben keine kostenlosen SMS-Gateways zur Verfügung. Weil Telegram internetbasiert ist
Es gibt keine Einschränkungen, daher ist es für alle verfügbar.
4. Die Fähigkeit beruht darauf, dass ein Empfänger einen Vornamen hat, der in Alice/Name-Slot aufgeführt ist.
Für Australier, die jeden „ol mate“ nennen, nennen Shazza, Bazza und zig andere umgangssprachliche Bezeichnungen die Fähigkeit
funktioniert nicht, es sei denn, Sie geben dem Empfänger einen aufgelisteten Vornamen wie Sue, Barry, Richard usw.
Eines Tages werde ich das vielleicht beheben, aber das ist ein zukünftiger Gedanke :)

## Fertigkeit konfigurieren

1. Wenn Sie Telegram nicht installiert haben UND Sie Details in das Feld "Details zum Telegrammempfänger" eingeben
Skill-Einstellungen, Alice wird Telegram während Ihres nächsten Alice-Neustarts herunterladen und installieren. Es wird so gemacht, um zu verhindern
Token-Fehler beim Start jedes Mal, wenn Telegram als Abhängigkeit installiert werden sollte und noch kein Telegram-Token eingetragen wurde
weil ein Benutzer kein Telegram-Konto hat.
2. Alle Felder werden in der Datenbank gespeichert, wenn Sie auf "Bestätigen" klicken

In der Skilleinstellung:

### *Für SMS-Funktion*

Geben Sie in das Feld "SMS-Absenderdetails - Ihre Angaben als Absender... format= Vorname/E-Mail/E-Mail-Passwort" ein
- Beispiel:
  - Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
Sie können so viele hinzufügen, wie Sie möchten, trennen Sie sie einfach durch Kommas wie im obigen Beispiel.
Diese Angaben werden später für die Anmeldung bei Ihrem E-Mail-Konto verwendet, um die SMS zu versenden

Geben Sie in das Feld "SMS-Empfängerdetails" - "Die Empfängerdetails im Format: Vorname/Telefonnummer/isEmergencyContact/smsGateway
- Beispiel:
  - larry/08001234/yes/@txt.att.net, jesus/180098765/no/@vtext.com

Fügen Sie wieder so viele hinzu, wie Sie möchten, aber durch Kommas getrennt.

HINWEIS: Dies wurde bisher nur mit Google Mail getestet. Um ein Gmail-App-Passwort festzulegen, gehen Sie zu [Google App-Passwort einrichten](https://support.google.com/accounts/answer/185833?hl=en)

#### *Lassen Sie uns diese aufschlüsseln*

Format: Vorname/Telefonnummer/istNotfallkontakt/smsGateway


1. FirstName: - Wie oben erwähnt, muss dies ein Listenname von Alice/Name sein. Es ist der Vorname des Empfängers
Der Vorname wird verwendet, um Alice zu fragen, „Sende eine Textnachricht an Mary“ usw

2. Telefonnummer: - Dies ist die Telefonnummer des Empfängers. Es muss "10 Ziffern" lang sein und darf keine Ländercodes enthalten

3. isEmergencyContact: - Hier markieren Sie jemanden als Notfallkontakt oder nicht. Zu addierende Werte sind "nur"
entweder ja oder nein. Ja bedeutet also, dass sie als Notfallkontakt markiert werden und daher eine Nachricht erhalten, wenn Sie dies wünschen
Alice, "Hilfe, ich bin gefallen".

4. smsGateway: - Dies ist das SMS-Gateway, das Ihr Empfänger verwendet. Sie müssen Ihren Kontakt fragen, wer dessen ist
Mobilfunkanbieter ist und dann nachschlagen, was das SMS-Gateway für diesen Anbieter ist. Eine Liste finden Sie hier
   [Wikipedia SMS Gateways](https://en.wikipedia.org/wiki/SMS_gateway)

Das Gateway, das Sie eingeben, muss ein @ am Anfang haben, wie z. B. @vtext.com


### *Für Telegrammfunktion*

Für das Feld Telegrammempfängerdetails – YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact
- Beispiel: larry/Mary/12345/ja

Dies folgt dem gleichen Prinzip wie SMS-Empfänger, verwenden Sie yes oder no für isEmergencyContact und die Kontakte
TelegramId für die "theirChatId"

#### *Alice-Standort-ID*

Geben Sie einen identifizierbaren Ort ein, an dem Alice lebt, damit andere Personen verstehen können, wann eine Notfallnachricht gesendet wird
und Alice nicht erkennt, wer die Anfrage geschrien hat, wird dieser Ortsname zum Helfen verwendet
Klären Sie die Nachricht für den Empfänger.

Beispiel: - "Hallo Notfallkontakt, jemand bei "Mike Pratts Haus" ist gestürzt und braucht sofort Hilfe"

Wo "Mike Pratts House" "Bobs Farm", "Susans Caravan" ""Jacks Place on Bourbon Street" usw. sein könnte.

#### *Notruf bestätigen*

Aktivieren Sie diese Option, um aufgefordert zu werden, wenn Sie vor dem Senden eine Hilfenachricht senden möchten.
Wenn Sie dies deaktivieren, werden möglicherweise Hilfenachrichten an Ihre Notfallkontakte gesendet, falls Alice Sie eines Tages missversteht
Bitte um Hilfe bei etwas völlig anderem :)

#### x Testmodus

Aktivieren Sie dies, um den Skill im Testmodus auszuführen. Im Testmodus funktioniert der Skill wie gewohnt, ABER..
Es wird keine tatsächliche Nachricht gesendet. Es wird nur angezeigt, was in Alices Syslog gesendet würde.

### SICHERHEITSHINWEIS
Mein Vorschlag, sobald Sie das Feld "Absenderangaben" eingegeben haben und mit diesen Angaben zufrieden sind, klicken Sie auf "Bestätigen".
Wenn Sie Alice das nächste Mal herunterfahren, gehen Sie zum Skill-Ordner SendTextMessage, öffnen Sie die Datei config.json.template und ändern Sie sie
```Befehlszeile
"smsSenderDetails": {
"Standardwert": "",
"Datentyp": "Zeichenfolge",
"isSensitive": wahr,
```
isSensitive to true (vom Standardwert false).

*Grund dafür* : Wenn Sie diesen Wert auf "true" ändern, wird das Feld ********** in der GUI anzeigen und somit Ihre schützen
E-Mail-Passwort nicht über die GUI angezeigt werden. Wenn Sie es standardmäßig auf true belassen, ist es nur schwieriger zu sehen, was Sie dort eingeben.
Aus diesem Grund habe ich es bei false belassen, bis ich einen alternativen Plan habe :)