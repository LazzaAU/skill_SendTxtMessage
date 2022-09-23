
### SendTxtMessage

## A cosa serve questa abilità?

Inizialmente questa abilità è stata progettata per gli utenti più maturi che potrebbero ritrovarsi a cadere
e non riesce a rialzarsi. Con questo in mente, potrebbero chiamare Alice e dire "aiuto, sono caduto" o molti altri
espressioni e Alice cercherà i contatti di emergenza configurati e invierà loro un messaggio SMS tramite
e-mail SMTP o tramite un messaggio Telegram a seconda della piattaforma scelta dall'utente.

Tuttavia, mentre scrivevo l'abilità, ho pensato che non ci fosse motivo per cui non potresti usarla per inviare un generale
messaggio di testo o telegramma tramite Alice a qualcuno. Quindi fa anche quello, ma ci sono dei limiti.

1. Né SMS né Telegram accetteranno risposte dalle persone, quindi è un sistema di messaggistica a senso unico
2. Soprattutto tramite SMS, anche se può dire messaggio inviato, non c'è garanzia se il destinatario lo ha effettivamente ricevuto
a causa dei limiti di invio gratuito dei messaggi.
3. La funzione SMS è disponibile solo in alcuni paesi come America e Canada.
Ad esempio, artisti del calibro di Australia non hanno gateway SMS gratuiti da utilizzare. Quindi perché Telegram è basato su Internet
non ci sono restrizioni quindi è disponibile per tutti.
4. L'abilità si basa su un destinatario con un nome elencato nello slot Alice/Nome.
Per gli australiani che chiamano tutti 'ol mate, shazza, bazza e un trilione di altri nomi gergali l'abilità
non funzionerà a meno che tu non dia al destinatario un nome elencato, come Sue, Barry, Richard ecc.
Un giorno potrei risolverlo, ma è un pensiero futuro :)

## Configurazione dell'abilità

1. Se non hai installato Telegram E inserisci i dettagli nel campo "Dettagli destinatario Telegram" nella
impostazioni delle abilità, Alice scaricherà e installerà Telegram durante il prossimo riavvio di Alice. È fatto in questo modo per prevenire
errori di token all'avvio ogni volta che Telegram doveva essere installato come dipendenza e tuttavia non era stato inserito alcun token di Telegram
a causa di un utente che non dispone di un account Telegram.
2. Tutti i campi vengono archiviati nel database quando si fa clic su "conferma"

Nell'impostazione delle abilità:

### *Per la funzione SMS*

Inserisci nel campo "Dettagli mittente SMS - I tuoi dati come mittente... format= FirstName/email/emailPassword"
- Esempio:
  - Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
puoi aggiungerne quanti ne vuoi, separali con una virgola come nell'esempio sopra.
Questi dettagli verranno successivamente utilizzati per accedere al tuo account di posta elettronica per inviare l'SMS

Immettere nel campo "Dettagli destinatario SMS" - "I dettagli del destinatario in formato: Nome/Numero telefono/isEmergencyContact/smsGateway
- Esempio:
  - larry/08001234/yes/@txt.att.net, jesus/180098765/no/@vtext.com

Ancora una volta, aggiungi quanti ne vuoi ma separati da virgole.

NOTA: finora è stato testato solo con gmail. per impostare una password per l'app Gmail, vai a [Imposta password per l'app Google](https://support.google.com/accounts/answer/185833?hl=en)

#### *Analizziamo questi*

formato: Nome/Numero di telefono/isEmergencyContact/smsGateway


1. Nome: - Come accennato in precedenza, questo deve essere un nome elencato da Alice/nome. È il nome del destinatario
Il nome viene utilizzato per chiedere ad Alice "invia un messaggio di testo a Mary" ecc

2. Numero di telefono: - Questo è il numero di telefono del destinatario. Deve contenere "10 cifre" e codici paese "NO".

3. isEmergencyContact: - Qui è dove tagghi qualcuno come contatto di emergenza o meno. I valori da aggiungere sono "solo"
o si o no. quindi sì significa che verrebbero contrassegnati come contatti di emergenza e quindi riceveranno un messaggio se lo dici
Alice, "Aiuto, sono caduta".

4. smsGateway: - Questo è il gateway SMS utilizzato dal destinatario. Dovrai chiedere al tuo contatto chi sono
è l'operatore di telefonia mobile e quindi cerca quale sia il gateway sms per quell'operatore. Un elenco può essere trovato qui
   [Wikipedia Sms Gateways](https://en.wikipedia.org/wiki/SMS_gateway)

Il gateway immesso deve avere la @ all'inizio, ad esempio @vtext.com


### *Per la funzione Telegram*

Per il campo Dettagli destinatario di Telegram - YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact
- Esempio: larry/Mary/12345/yes

Questo segue lo stesso principio del destinatario degli SMS, usa sì o no per isEmergencyContact e i contatti
telegramId per "theirChatId"

#### *Id posizione Alice*

Inserisci un luogo identificabile in cui vive Alice, allo scopo che altre persone possano capire quando viene inviato un messaggio di emergenza
e Alice non ha riconosciuto chi ha urlato la richiesta, questo nome di posizione verrà utilizzato per aiutare
chiarire il messaggio al destinatario.

Esempio: - "Ciao contatto di emergenza, qualcuno a "casa di Mike Pratts" è caduto e ha bisogno di aiuto immediatamente"

Dove "casa di Mike Pratts" potrebbe essere "bobs farm", "susans Caravan" ""jacks place on Bourbon Street" ecc.

#### *Conferma chiamata di emergenza*

Abilitare questa opzione se si desidera inviare un messaggio di aiuto prima di inviarlo.
Disabilitare questo potrebbe inviare messaggi di aiuto ai tuoi contatti di emergenza se Alice un giorno ti fraintende
chiedendo aiuto su qualcosa di completamente non correlato :)

#### x Modalità di prova

Abilita questa opzione per eseguire l'abilità in modalità test. Durante la modalità test l'abilità funzionerà normalmente MA..
non invierà alcun messaggio reale. Mostrerà solo ciò che verrebbe inviato nel syslog di Alice.

### NOTA DI SICUREZZA
Il mio suggerimento, una volta che hai inserito il campo "Dettagli mittente" e sei soddisfatto di quei dettagli, fai clic su "conferma"
quindi la prossima volta che spegni Alice vai alla cartella delle abilità SendTextMessage, apri il file config.json.template e modifica
```riga di comando
"smsSenderDetails": {
"valore di default": "",
"dataType" : "stringa",
"isSensitive": vero,
```
isSensitive a true ( dal valore predefinito di false).

*Motivo dell'essere*: ​​la modifica di quel valore in "true" farà visualizzare il campo ********** nella GUI e quindi proteggere il tuo
e-mail password da visualizzare tramite la GUI. Lasciarlo a true per impostazione predefinita rende solo più difficile vedere cosa stai digitando lì,
quindi per questo motivo l'ho lasciato su false fino a quando non mi viene in mente un piano alternativo :)