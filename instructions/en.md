### SendTxtMessage

## What is this skill used for ?

Initially this skill was designed for the more mature users who may find themselves taking a fall 
and not able to get back up. With that in mind, they could call for Alice and say "help I've fallen" or several other
utternaces and Alice will search for configured emergency contacts and send them either an SMS message via 
email SMTP or via a Telegram message depending on what platform the user chooses.

However, whilst writing the skill I thought there's no reason why you couldn't use it to send a general 
text or telegram message via Alice to someone. So it does that too, but there is limitations.

1. Neither SMS nor Telegram will accept replies from people, so it's a one way message
2. Via SMS especially, although it may say message sent, there's no garuntee's the recipient actually recieved it
due to limits of sending messages for free.
3. SMS feature is only available to some countries such as America. 
The likes of Australia for example don't have free SMS gateways to use. So because Telegram is internet based
there is no restrictions therefore it's available to everyone.
4. The skill relies on a recipient having a first name that is listed in Alice/Name slot. 
For Australians that call everyone 'ol mate, shazza, bazza, and a zillion other slang names the skill 
won't work unless you give the recipient a listed first name , like Sue, barry, richard etc. 
One day I might fix that but that's a future thought :)

## Configuring the skill

1. The skill depends on Telegram skill being installed. Regardless if you only want to use the SMS side of it
This should be installed for you when you installed this skill
2. All fields get stored in the database when you click "confirm"

In the skill setting:

### <u>*For SMS feature*</u>

Enter into the "SMS Sender Details field - Your details as the sender... format= FirstName/email/emailPassword"
- Example:
  - Larry/larry@email.com/123456, Mary/mary@gmail.com/987654"
you can add as many as you like , just comma seperate them as per above example.
These details will later get used for logging into your email account in order to send the SMS

Enter into the "SMS Recipient Details" field - "The recipient details in format: FirstName/PhoneNumber/isEmergencyContact/smsGateway
- Example:
  - larry/08001234/yes/@txt.att.net, jesus/180098765/no/@vtext.com

Again, add as many as you like but comma seperated.

NOTE: This has only been tested with gmail so far. to set a gmail app pawword go to [Setup Google App Password](https://support.google.com/accounts/answer/185833?hl=en)

#### <u>*Let's break down these*</u>

format: FirstName/PhoneNumber/isEmergencyContact/smsGateway


1. FirstName: - As mentioned above, this needs to be a listed name from Alice/name. It's the first name of the recipient
The First name is used for asking Alice "send a text message to Mary" etc

2. Phone number: - This is the recipients Phone number. It needs to be "10 digits" long and "NO" country codes

3. isEmergencyContact: - This is where you tag someone as an emergency contact or not. Values to add are "only"
either yes or no. so yes means they would be tagged as an emergency contact and therefore get a message if you say to 
ALice, "Help I've fallen".

4. smsGateway: - This is the sms gateway your recipient uses. You'll need to ask your contact who their 
mobile carrier is and then look up what the sms gateway for that carrier is. A list can be found here
   [Wikipedia Sms Gateways](https://en.wikipedia.org/wiki/SMS_gateway)

The Gateway you enter must have the @ at the start of it such as @vtext.com


### <u>*For Telegram Feature*</u>

For the Telegram Recipient Details field - YourFirstName/TheirFirsName/TheirChatId/isEmergencyContact 
- Example: larry/Mary/12345/yes

This follows the same principle as sms recipient, use yes or no for isEmergencyContact and the contacts 
telegramId for the "thierChatId" 

#### <u>*Alice location Id*</u>

Enter an identifiable location that alice is for other people to understand. When an emergency message is 
sent and Alice doesn't recognised who has yelled out the request, this location name will be used for helping
clarify the message to the recipient .

Example: - "Hi emergency contact, someone at "mike Pratts house" has fallen and needs help immediately"

Where "mike Pratts house" could be "bobs farm", "susans Caravan" ""jacks place on 2nd street" etc

#### <u>*Confirm Emergency call*</u>

Enable this to be prompted if you want to send a help message before sending it. 
Disabling this may send help messages to you emergency contacts if Alice missunderstands you one day 
asking for help on something entirely un related :)
