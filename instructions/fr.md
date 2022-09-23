
### EnvoyerTxtMessage

## A quoi sert cette compétence ?

Initialement, cette compétence a été conçue pour les utilisateurs plus matures qui peuvent se retrouver en train de tomber
et impossible de se relever. Dans cet esprit, ils pourraient appeler Alice et dire "au secours, je suis tombé" ou plusieurs autres
et Alice recherchera les contacts d'urgence configurés et leur enverra soit un message SMS via
e-mail SMTP ou via un message Telegram en fonction de la plate-forme choisie par l'utilisateur.

Cependant, en écrivant la compétence, j'ai pensé qu'il n'y avait aucune raison pour que vous ne puissiez pas l'utiliser pour envoyer un général
message texte ou télégramme via Alice à quelqu'un. Donc, il le fait aussi, mais il y a des limites.

1. Ni SMS ni Telegram n'accepteront les réponses des gens, c'est donc un système de messagerie à sens unique
2. Par SMS en particulier, bien qu'il puisse indiquer un message envoyé, il n'y a aucune garantie que le destinataire l'ait réellement reçu
en raison des limites d'envoi de messages gratuits.
3. La fonction SMS n'est disponible que dans certains pays tels que l'Amérique et le Canada.
Les pays comme l'Australie, par exemple, n'ont pas de passerelles SMS gratuites à utiliser. Donc, parce que Telegram est basé sur Internet
il n'y a pas de restrictions donc c'est accessible à tous.
4. La compétence repose sur un destinataire dont le prénom est répertorié dans l'emplacement Alice/Nom.
Pour les Australiens qui appellent tout le monde 'ol mate, shazza, bazza, et un zillion d'autres noms d'argot la compétence
ne fonctionnera que si vous donnez au destinataire un prénom répertorié, comme Sue, Barry, Richard, etc.
Un jour, je pourrais résoudre ce problème, mais c'est une pensée future :)

## Configuration de la compétence

1. Si vous n'avez pas installé Telegram ET que vous entrez des détails dans le champ "Détails du destinataire du télégramme" dans le
paramètres de compétence, Alice téléchargera et installera Telegram lors de votre prochain redémarrage d'Alice. C'est fait de cette façon pour empêcher
erreurs de jeton au démarrage à chaque fois si Telegram devait être installé en tant que dépendance et pourtant aucun jeton Telegram n'a été saisi
en raison d'un utilisateur n'ayant pas de compte Telegram.
2. Tous les champs sont stockés dans la base de données lorsque vous cliquez sur "confirmer"

Dans le cadre des compétences :

### *Pour la fonction SMS*

Entrez dans le champ "SMS Sender Details - Vos coordonnées en tant qu'expéditeur... format= FirstName/email/emailPassword"
- Exemple:
  -Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
vous pouvez en ajouter autant que vous le souhaitez, il suffit de les séparer par des virgules comme dans l'exemple ci-dessus.
Ces informations seront ensuite utilisées pour vous connecter à votre compte de messagerie afin d'envoyer le SMS.

Entrez dans le champ "Détails du destinataire du SMS" - "Les détails du destinataire au format : FirstName/PhoneNumber/isEmergencyContact/smsGateway
- Exemple:
  - larry/08001234/yes/@txt.att.net, jesus/180098765/no/@vtext.com

Encore une fois, ajoutez-en autant que vous le souhaitez, mais en les séparant par des virgules.

REMARQUE : jusqu'à présent, cela n'a été testé qu'avec Gmail. pour définir un mot de passe d'application Gmail, accédez à [Configurer le mot de passe de l'application Google](https://support.google.com/accounts/answer/185833?hl=en)

#### * Décomposons-les *

format : Prénom/NuméroTéléphone/estContactEmergence/passerelle sms


1. Prénom : - Comme mentionné ci-dessus, il doit s'agir d'un nom répertorié d'Alice/nom. C'est le prénom du destinataire
Le prénom est utilisé pour demander à Alice "envoyer un SMS à Marie", etc.

2. Numéro de téléphone : - Il s'agit du numéro de téléphone du destinataire. Il doit comporter "10 chiffres" et "NON" les codes de pays

3. isEmergencyContact : - C'est ici que vous marquez quelqu'un comme contact d'urgence ou non. Les valeurs à ajouter sont "uniquement"
soit oui soit non. donc oui signifie qu'ils seraient étiquetés comme contact d'urgence et recevraient donc un message si vous dites à
Alice, "Au secours je suis tombée".

4. smsGateway : - Il s'agit de la passerelle SMS utilisée par votre destinataire. Vous devrez demander à votre contact qui est son
est l'opérateur de téléphonie mobile, puis recherchez la passerelle SMS de cet opérateur. Une liste est disponible ici
   [Passerelles SMS Wikipédia](https://en.wikipedia.org/wiki/SMS_gateway)

La passerelle que vous entrez doit avoir le @ au début, comme @vtext.com


### *Pour la fonctionnalité de télégramme*

Pour le champ Détails du destinataire du télégramme - YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact
- Exemple : larry/Mary/12345/yes

Cela suit le même principe que le destinataire du SMS, utilisez oui ou non pour isEmergencyContact et les contacts
telegramId pour "theirChatId"

#### *Identifiant de l'emplacement d'Alice*

Entrez un lieu identifiable où vit Alice, afin que d'autres personnes puissent comprendre lorsqu'un message d'urgence est envoyé
et Alice ne reconnaît pas qui a crié la demande, ce nom de lieu sera utilisé pour aider
clarifier le message au destinataire.

Exemple : - "Bonjour contact d'urgence, quelqu'un à la "maison de Mike Pratts" est tombé et a besoin d'aide immédiatement"

Où "mike Pratts house" pourrait être "bobs farm", "susans Caravan" ""jacks place on Bourbon Street" etc.

#### *Confirmer l'appel d'urgence*

Activez cette option pour être invité si vous souhaitez envoyer un message d'aide avant de l'envoyer.
Désactiver cela peut envoyer des messages d'aide à vos contacts d'urgence si Alice vous comprend mal un jour
demander de l'aide sur quelque chose qui n'a rien à voir :)

#### x Mode test

Activez cette option pour exécuter la compétence en mode test. Pendant le mode test, la compétence fonctionnera normalement MAIS ..
il n'enverra aucun message réel. Il affichera simplement ce qui serait envoyé dans le syslog d'Alice.

### NOTE DE SÉCURITÉ
Ma suggestion, une fois que vous avez entré le champ "Détails de l'expéditeur" et que vous êtes satisfait de ces détails, cliquez sur "confirmer"
puis la prochaine fois que vous arrêterez Alice, allez dans le dossier de compétences SendTextMessage, ouvrez le fichier config.json.template et modifiez
```ligne de commande
"smsSenderDetails": {
"valeur par défaut": "",
"TypeDonnées" : "chaîne",
"isSensitive" : vrai,
```
isSensitive à true ( à partir de la valeur par défaut de false).

*Raison en cours* : Changer cette valeur en "true" fera afficher le champ ********** dans l'interface graphique et protégera donc votre
mot de passe e-mail d'être visible via l'interface graphique. Le laisser sur true par défaut rend plus difficile de voir ce que vous tapez là-dedans,
donc pour cette raison, je l'ai laissé sur false jusqu'à ce que je propose un plan alternatif :)