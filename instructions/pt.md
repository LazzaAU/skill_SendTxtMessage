
### SendTxtMessage

## Para que essa habilidade é usada?

Inicialmente, essa habilidade foi projetada para usuários mais maduros que podem cair
e não consegue voltar. Com isso em mente, eles poderiam chamar Alice e dizer "socorro eu caí" ou várias outras
enunciados e Alice irá procurar contatos de emergência configurados e enviar-lhes uma mensagem SMS via
e-mail SMTP ou por meio de uma mensagem do Telegram, dependendo da plataforma que o usuário escolher.

No entanto, enquanto escrevia a habilidade, pensei que não havia razão para que você não pudesse usá-la para enviar um
mensagem de texto ou telegrama via Alice para alguém. Então ele faz isso também, mas há limitações.

1. Nem SMS nem Telegram aceitarão respostas de pessoas, então é um sistema de mensagens unidirecional
2. Via SMS especialmente, embora possa dizer que a mensagem foi enviada, não há garantia de que o destinatário realmente a recebeu
devido aos limites de envio de mensagens gratuitamente.
3. O recurso SMS está disponível apenas para alguns países, como Estados Unidos e Canadá.
Os gostos da Austrália, por exemplo, não têm gateways SMS gratuitos para usar. Então, porque o Telegram é baseado na Internet
não há restrições, portanto, está disponível para todos.
4. A habilidade depende de um destinatário que tenha um primeiro nome listado no slot Alice/Nome.
Para os australianos que chamam todo mundo de 'ol mate, shazza, bazza e um zilhão de outras gírias nomeiam a habilidade
não funcionará a menos que você dê ao destinatário um primeiro nome listado, como Sue, Barry, Richard etc.
Um dia eu posso consertar isso, mas isso é um pensamento futuro :)

## Configurando a habilidade

1. Se você não tiver o Telegram instalado E inserir detalhes no campo "Detalhes do destinatário do telegrama" no
configurações de habilidade, Alice baixará e instalará o Telegram durante a próxima reinicialização do Alice. É feito desta forma para evitar
erros de token na inicialização sempre que o Telegram fosse instalado como uma dependência e ainda assim nenhum token do Telegram fosse inserido
devido a um usuário não ter uma conta do Telegram.
2. Todos os campos são armazenados no banco de dados quando você clica em "confirmar"

Na configuração de habilidade:

### *Para recurso SMS*

Entre no campo "SMS Sender Details - Seus detalhes como remetente... format= FirstName/email/emailPassword"
- Exemplo:
  - Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
você pode adicionar quantos quiser, basta separá-los por vírgula conforme o exemplo acima.
Esses detalhes serão usados ​​posteriormente para fazer login em sua conta de e-mail para enviar o SMS

Digite no campo "SMS Recipient Details" - "Os detalhes do destinatário no formato: FirstName/PhoneNumber/isEmergencyContact/smsGateway
- Exemplo:
  - larry/08001234/yes/@txt.att.net, jesus/180098765/no/@vtext.com

Novamente, adicione quantos quiser, mas separados por vírgulas.

NOTA: Isso só foi testado com o Gmail até agora. para definir uma palavra-chave do aplicativo do Gmail, acesse [Configurar senha do aplicativo do Google](https://support.google.com/accounts/answer/185833?hl=en)

#### *Vamos detalhar isso*

formato: FirstName/PhoneNumber/isEmergencyContact/smsGateway


1. FirstName: - Como mencionado acima, este precisa ser um nome listado de Alice/name. É o primeiro nome do destinatário
O primeiro nome é usado para pedir a Alice "envie uma mensagem de texto para Mary" etc.

2. Número de telefone: - Este é o número de telefone do destinatário. Ele precisa ter "10 dígitos" e códigos de país "NÃO"

3. isEmergencyContact: - Aqui é onde você marca alguém como contato de emergência ou não. Os valores a serem adicionados são "somente"
ou sim ou não. então sim significa que eles seriam marcados como um contato de emergência e, portanto, receberiam uma mensagem se você disser para
Alice, "Socorro eu caí".

4. smsGateway: - Este é o gateway SMS que seu destinatário usa. Você precisará perguntar ao seu contato quem
operadora de celular é e, em seguida, procure o que é o gateway de sms para essa operadora. Uma lista pode ser encontrada aqui
   [Wikipedia Sms Gateways](https://en.wikipedia.org/wiki/SMS_gateway)

O Gateway que você inserir deve ter o @ no início, como @vtext.com


### *Para Recurso Telegram*

Para o campo Detalhes do destinatário do telegrama - YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact
- Exemplo: larry/Mary/12345/yes

Isso segue o mesmo princípio do destinatário do SMS, use sim ou não para isEmergencyContact e os contatos
telegramId para o "theirChatId"

#### *ID de localização de Alice*

Digite um local identificável em que Alice mora, para que outras pessoas possam entender quando uma mensagem de emergência for enviada
e Alice não reconhece quem gritou o pedido, este nome de local será usado para ajudar
esclarecer a mensagem para o destinatário.

Exemplo: - "Olá, contato de emergência, alguém na "casa do mike Pratts" caiu e precisa de ajuda imediatamente"

Onde "casa de Mike Pratts" poderia ser "fazenda de bobs", "susans Caravan" ""jacks place on Bourbon Street" etc.

#### *Confirmar chamada de emergência*

Ative isso para ser solicitado se você deseja enviar uma mensagem de ajuda antes de enviá-la.
Desativar isso pode enviar mensagens de ajuda para seus contatos de emergência se Alice o entender mal um dia
pedindo ajuda em algo totalmente não relacionado :)

#### x Modo de teste

Ative isso para executar a habilidade no modo de teste. Durante o modo de teste, a habilidade funcionará normalmente, MAS..
ele não enviará nenhuma mensagem real. Ele apenas exibirá o que seria enviado no syslog do Alices.

### NOTA DE SEGURANÇA
Minha sugestão, depois de inserir o campo "Detalhes do remetente" e estiver satisfeito com esses detalhes, clique em "confirmar"
então, na próxima vez que você desligar o Alice, vá para a pasta de habilidades SendTextMessage, abra o arquivo config.json.template e altere
``` linha de comando
"smsSenderDetails": {
"valor padrão": "",
"dataType": "string",
"isSensitive" : verdadeiro,
```
isSensitive para true (do padrão false).

*Razão de ser* : Alterar esse valor para "true" fará com que o campo exiba ********** no gui e, portanto, proteja seu
senha de e-mail de ser visível através do gui. Deixá-lo como verdadeiro por padrão apenas torna mais difícil ver o que você está digitando lá,
então, por esse motivo, deixei em falso até que eu apresentasse um plano alternativo :)