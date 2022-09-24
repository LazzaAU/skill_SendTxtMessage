import smtplib

from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler
from core.base.model.Intent import Intent
from pathlib import Path

class SendTxtMessage(AliceSkill):
	"""
	Author: Lazza
	Description: Send a text message or a telegram message using Alice
	"""

	# Setup database tables
	_SMSRECIPIENT = 'SendAText'
	_TELEGRAMRECIPIENTS = 'SendTelegram'
	_SENDERDETAILS = 'SenderDetails'
	_DATABASE = {
		_SMSRECIPIENT: [
			#'id INTEGER PRIMARY KEY',
			'recipientPhoneNumber TEXT UNIQUE',
			'recipientName TEXT NOT NULL',
			'isEmergencyContact TEXT NOT NULL',
			'smsGateway TEXT NOT NULL',
			'noteSent INTEGER NOT NULL DEFAULT 0 '
		],
		_TELEGRAMRECIPIENTS: [
			#'id INTEGER PRIMARY KEY'
			'recipientChatId integer UNIQUE',
			'senderFirstName TEXT NOT NULL',
			'recipientName TEXT NOT NULL',
			'isEmergencyContact TEXT NOT NULL',
			'noteSent INTEGER NOT NULL DEFAULT 0 '
		],
		_SENDERDETAILS: [
			#'id TEXT PRIMARY KEY'
			'email TEXT UNIQUE',
			'senderFirstName TEXT NOT NULL',
			'password TEXT NOT NULL',
		]
	}

	_INTENT_USER_RANDOM_ANSWER = Intent('UserRandomAnswer')
	_INTENT_ANSWER_YES_OR_NO = Intent('AnswerYesOrNo')

	def __init__(self):

		self._INTENTS = [
			self._INTENT_ANSWER_YES_OR_NO,
			self._INTENT_USER_RANDOM_ANSWER
		]

		self._INTENT_ANSWER_YES_OR_NO.dialogMapping = {
			'sendEmergencyContact' : self.emergencyConfirmationAction
		}
		self._INTENT_USER_RANDOM_ANSWER.dialogMapping = {
			'addMessageToTxt': self.getMessageFromUser
		}
		self._telegramContacts = False
		self._dbTrigger = False

		super().__init__(self._INTENTS, databaseSchema=self._DATABASE)

	def onStart(self):
		"""
		Check if Telegram is installed. If not, Install it 'ONLY' if the user wants it, to prevent missing Telegram
		token errors on start up if it was to get installed as a dependancy.
		:return:
		"""
		super().onStart()
		telegramPath = Path(f"{str(Path.home())}/ProjectAlice/skills/Telegram/Telegram.install")
		if not telegramPath.exists() and self.getConfig(key='telegramRecipientDetails'):
			self.SkillManager.downloadSkills(skills='Telegram')


	### - ### - ### EMERGENCY CALL SECTION ### _### _ ####
	@IntentHandler('emergencyCall')
	def messageEmergencyContacts(self, session: DialogSession):
		"""
		This intent handles emergency contact messages. We first check if a confirmation is needed
		:param session: The dialog session
		"""

		if self.getConfig("confirmEmergencyCall"):
			self.continueDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="askToSendEmergencyBroadcast"),
				intentFilter=[self._INTENT_ANSWER_YES_OR_NO],
				currentDialogState='sendEmergencyContact',
				probabilityThreshold=0.1
			)
		else:
			self.sendTheActualEmergencyMessage(session=session)

	def emergencyConfirmationAction(self, session):
		"""
		Either send or don't send the Emergency message depending on user reply
		:param session: the dialog session
		:return:
		"""

		if self.Commons.isYes(session):
			self.sendTheActualEmergencyMessage(session=session)
		else:
			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="notSendingMessage"),
				deviceUid=session.deviceUid
			)

	def sendTheActualEmergencyMessage(self, session):
		"""
		This method sends the message. It locates both sms emergency contacts and telegram emergency contacts
		and sends the emergency message to all those contacts.
		:param: session: The dialog session
		:return:
		"""

		telegramContacts = self.fetchDbContacts(table=self._TELEGRAMRECIPIENTS)

		senderName = self.fetchSenderDetail(session=session, onlyName=True)

		if senderName:
			message = f"{self.randomTalk(text='emergencyIfSenderName', replace=[senderName[0]])}"
		else:
			message = f"{self.randomTalk(text='emergencyIfNoSenderName', replace=[self.getConfig('alicelocationId')])}"

		numberofEmergencyContacts = list()

		# If there are Telegram emergency contacts
		for contact in telegramContacts:

			if "yes" in contact['isEmergencyContact']:
				self.sendTelegram(recipientName=contact['recipientName'], message=message, noteSent=contact['noteSent'], chatID=contact['recipientChatId'])
				numberofEmergencyContacts.append(contact['recipientName'])

		if numberofEmergencyContacts:
			self._telegramContacts = True
			self.say(
				text=self.randomTalk(text="justSentEmergencyTelegram", replace=[len(numberofEmergencyContacts)]),
				deviceUid=session.deviceUid
			)

		#Check for SMS Emergency contacts
		self.processSmsDetails(session=session, message=message, isEmergency=True)


	### - ### - ### GENERAL SEND A MESSAGE SECTION ### _### _ ####
	@IntentHandler('SendTxt')
	def sendTextMessage(self, session: DialogSession):
		"""
		This handles general outgoing texts
		:param session: The dialog session
		:return:
		"""

		slotText = session.slotValue('textMessage')
		slotTelegram = session.slotValue('telegramMessage')
		name = session.slotValue('Alice/Name')

		self.continueDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text="whatMessageToSend"),
			intentFilter=[self._INTENT_USER_RANDOM_ANSWER],
			currentDialogState='addMessageToTxt',
			customData={
				"textMessage" : slotText,
				"telegramMessage" :  slotTelegram,
				"name" : name
				}
			)


	def getMessageFromUser(self, session: DialogSession):
		"""
		This method triggers when the user provides a message that they want to send to the contact.
		It, then processes who and how to send it
		:param session: Dialog session containing the user message
		:return
		"""
		# set these vars because we can't iterate a type None value in the next two blocks
		requestedText = session.customData['textMessage']
		requestedTelegram = session.customData['telegramMessage']

		if requestedText:
			message = session.payload['input']
			self.processSmsDetails(session=session, message=message)


		elif requestedTelegram:
			listOfContacts = self.fetchDbContacts(table=self._TELEGRAMRECIPIENTS)

		#	self.Commons.getMethodCaller(listOfContacts=listOfContacts, recipientsname=session.customData['name'])

			if session.customData['name']: # the name of the user to send to
				for contact in listOfContacts:

					# If the requested name is in the list of contacts
					if session.customData['name'].capitalize() in str(contact['recipientName']).capitalize():
						self.sendTelegram(recipientName=contact['recipientName'], message=session.payload['input'], noteSent=contact['noteSent'], chatID=contact['recipientChatId'])

						self.endDialog(
							sessionId=session.sessionId,
							text=self.randomTalk(text="sendingMessageToContact", replace=[contact['recipientName'], "telegram"]),
							deviceUid=session.deviceUid
						)
						return
				# If we can't find a contact
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="couldntFindContact", replace=[session.customData['name'].capitalize()]),
					deviceUid=session.deviceUid
				)

			# If no name was given in the intent
			else:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="noRecipientNameSpecified"),
					deviceUid=session.deviceUid
				)


	def processSmsDetails(self, session, message, isEmergency = False):
		"""
		Sort through all the required sms details and prepare them to be sent for sending.
		if it's an emergency request, by pass some text message checks
		:param session: The dialog session
		:param message: The messagae to be sent to the contact
		:param isEmergency: True if it's an emergency call, else False
		:return:
		"""

		email, pwd, port = self.setEmailProperties(session)

		if not email:
			if not self._telegramContacts and isEmergency:
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="noEmergencyContacts"),
					deviceUid=session.deviceUid
				)
				self._telegramContacts = False
			else:
				self.endSession(sessionId=session.sessionId)

			return

		outgoingSMTP = email.split('@')[1]
		recipientList = self.fetchDbContacts(table=self._SMSRECIPIENT)
		tempList = list()
		numberOfEmergencyContacts = int
		name = ""

		self.logInfo(self.randomTalk(text="systemSettingUpSmsDetails"))

		if not 'sendEmergencyContact' in session.currentState:
			name = str(session.customData['name']).capitalize()

		if isEmergency:
			for contact in recipientList:
				if "yes" in contact['isEmergencyContact']:
					tempList.append(contact)
			recipientList = tempList
			numberOfEmergencyContacts = len(recipientList)

		# If there's no SMS recipients then stop
		if not recipientList:
			self.logInfo(self.randomTalk(text="systemMessageNoRecipientStored"))
			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="systemMessageNoRecipientStored"),
				deviceUid=session.deviceUid
			)
			return

		if name or isEmergency:
			for contact in recipientList:
				if name in str(contact['recipientName']).capitalize().replace(' ','') or isEmergency :
					recipientName = contact['recipientName']
					note = ""
					if contact['noteSent'] == 0:
						note = self.randomTalk(text="smsNote")
						self.updateNoteSent(table=self._SMSRECIPIENT, chatID=contact['recipientPhoneNumber'], noteSent=1)

					self.sendTxt(
						email=email,
						pwd=pwd,
						outgoingSmtp=outgoingSMTP,
						port=port,
						recipientPhoneNumber=contact['recipientPhoneNumber'],
						recievingGateway=contact['smsGateway'],
						message=message,
						note=note
					)

					if not isEmergency:
						self.endDialog(
							sessionId=session.sessionId,
							text=self.randomTalk(text="sendingMessageToContact", replace=[recipientName, 'Text']),
							deviceUid=session.deviceUid
						)
						return
					else:
						self.endDialog(
							sessionId=session.sessionId,
							text=self.randomTalk(text="sentMessageToXcontacts", replace=[numberOfEmergencyContacts]),
							deviceUid=session.deviceUid
						)
						return
			else:
				self.logWarning(self.randomTalk(text="systemCouldntLocateSMSContact", replace=[session.customData['name'].capitalize()]))
				self.endDialog(
					sessionId=session.sessionId,
					text=self.randomTalk(text="cantLocateSMSContact", replace=[session.customData['name'].capitalize()]),
					deviceUid=session.deviceUid
				 )
				return

		self.endDialog(
			sessionId=session.sessionId,
			text=self.randomTalk(text="noSMSContactFound"),
			deviceUid=session.deviceUid
		)

	def sendTelegram(self, recipientName: str, message: str, noteSent = 0, chatID: str = None):
		"""
		Sends the telegram message to a listed recipient
		:param  recipientName: The recipients name configured in the skill settings
		:param  message: The message to send to the user
		:param noteSent: If 0, a note is also sent, if 1 the note is not sent again
		:param  chatID: The recipients telegram id, If not provided directly, it will be searched for in the skill settings
		:return:
		"""

		# Check if Telegram Skill is installed. Stop here if it's not installed.
		if not Path(f"{str(Path.home())}/ProjectAlice/skills/Telegram/Telegram.install").exists():
			if self.getConfig('telegramRecipientDetails'):
				self.logInfo(self.randomTalk(text="systeminstallTelegram"))
				return
			else:
				self.logInfo(self.randomTalk(text="systemmanuallyInstallTelegram"))
				return

		# Import the Telegram module here so those that don't use telegram don't get token errors if its installed as a dependency
		from skills.Telegram import Telegram

		if not chatID:
			listOfContacts = self.fetchDbContacts(table=self._TELEGRAMRECIPIENTS)
			for contact in listOfContacts:
				if recipientName.lower() in str(contact['recipientName']).lower():
					chatID = contact['recipientChatId']
		try:
			if not self.getConfig("xTestMode"):
				tMessage = Telegram.Telegram()
				tMessage.sendMessage(chatId=chatID, message=f"Hi {recipientName}, {message}")
				if noteSent == 0 :
					tMessage.sendMessage(chatId=chatID, message=f"{self.randomTalk(text='telegramNote', replace=[recipientName])}")
					self.updateNoteSent(table=self._TELEGRAMRECIPIENTS, chatID=chatID, noteSent=1)
			else:
				self.logWarning(f"You're in Test Mode. However I would of sent a telegram message in normal mode")
				self.logDebug(f"\n ChatId is : {chatID} \n Recipient Name is : {recipientName} \n message would be : {message}")
				if noteSent == 0 :
					self.logDebug(self.randomTalk(text='telegramNote', replace=[recipientName]))

		except Exception as e:
			self.logWarning(self.randomTalk(text="systemErrorSendingTelegram", replace=[e]))
			self.say(
				text=self.randomTalk(text="failedToSendTelegram")
			)
	def sendTxt(self, email: str, pwd: str, outgoingSmtp: str, port: int, recipientPhoneNumber: int, recievingGateway: str, message : str, note: str ):
		"""
		Allows for internal and external use of sending a Txt message to a listed recipient via SMTP
		:param email: The senders email address
		:param pwd: The senders email password
		:param outgoingSmtp: The senders SMPT server eg: @gmail.com
		:param port: The senders email port to use
		:param recipientPhoneNumber: The phone number of the recipient (without country code and 10 digits long)
		:param recievingGateway: The recipients mobile carrier gateway EG: @vtext.com
		:param message: The message to send
		:param note: A one time note sent to user
		:return:
		"""

		self.logInfo(self.randomTalk(text="systemSetupSmsServer"))
		server = smtplib.SMTP(f"smtp.{outgoingSmtp}",port)
		recipient = f"{recipientPhoneNumber}{recievingGateway}"
		header = f"""
		From: {email}
		To: {recipient}
		Subject: text-message
		{message}
		{note}"""

		try:
			if not self.getConfig("xTestMode"):
				server.starttls()
				server.login(email,pwd)
				server.sendmail(email, recipient, header)
				server.quit()
				self.logInfo(self.randomTalk(text="systemSMSsent", replace=[recipient]))

			else:
				self.logDebug(f"You're in Test Mode. However I would of sent a SMS message in normal mode")
				self.logDebug(f"Details are : \n {header}")
				self.logInfo(self.randomTalk(text="systemSMSsent", replace=[recipient]))

		except Exception as e:
			self.logInfo(self.randomTalk(text="systemErrorSendingSMS", replace=[e]))

	def updateNoteSent(self, table :str, chatID, noteSent: int):
		"""
		Updates the noteSent value in the database table
		:param table: The Table name
		:param chatID: Either the recipients Phone Number or the recipients ChatId
		:param noteSent: value ofNote Sent. Usually 1
		:return:
		"""

		if 'SendAText' in table:
			field = 'recipientPhoneNumber'
		else :
			field = 'recipientChatId'

		self.DatabaseManager.update(
			tableName=table,
			callerName=self.name,
			values={
				'noteSent': noteSent
			},
			row=(field, chatID)

		)
	def addToSenderTable(self, senderFirstName : str, email : str, password : str):
		"""
		Inserts the sender details to the Sender table in the database. Details retrieved from the config
		:param senderFirstName: Senders first name
		:param email: sender email address
		:param password: senders email Password
		:return:
		"""
		self.databaseInsert(
			tableName=self._SENDERDETAILS,
			values={
				'senderFirstName': senderFirstName,
				'email': email,
				'password': password
			}
		)
	def addToSmsTable(self, recipientName : str, recipientPhoneNumber :str, smsGateway :str, emergencyContact :str ):
		"""
		Inserts the recipients details to the sms table in the database
		:param recipientName: Recipients first name
		:param recipientPhoneNumber: Recipients phone number
		:param smsGateway: The sms gateway of the recipient
		:param emergencyContact: Tags the contact as an emergency contact or not
		:return:
		"""

		self.databaseInsert(
			tableName=self._SMSRECIPIENT,
			values={
				'recipientName': recipientName,
				'recipientPhoneNumber': recipientPhoneNumber,
				'isEmergencyContact' : emergencyContact,
				'smsGateway' : smsGateway
			}
		)
	def addToTelegramTable(self, senderFirstName : str, recipientName : str, recipientChatId :int, emergencyContact :str):
		"""
		Adds a telegram contact to the telegram table in the database
		:param senderFirstName: The senders first name
		:param recipientName: The recipients first name
		:param recipientChatId: The recipients telegram chatID
		:param emergencyContact: Tags the contact as an emergency contact or not
		:return:
		"""
		self.databaseInsert(
			tableName=self._TELEGRAMRECIPIENTS,
			values={
				'senderFirstName': senderFirstName,
				'recipientName': recipientName,
				'recipientChatId': recipientChatId,
				'isEmergencyContact' : emergencyContact
			}
		)

	def fetchSenderDetail(self, session, onlyName = False):
		"""
		Retrieves the list of senders from the database, it looks for sender details that match the (session.user)
		if it can't find a match, it uses the first sender details in the list
		:param session: The dialog session
		:param	onlyName: If set to True, will return only the sender name, else the entire sender dict
		:return: returns either the sender details that matches Alice's (session.user) or the furst sender
		in the list. all returns are a list for compatibilty reasons
		"""
		senderDetails = list()
		senderName = list()
		defaultSender = list()
		defaultName = list()

		for row in self.databaseFetch(tableName=self._SENDERDETAILS, query='SELECT * FROM :__table__ '):
			# store the first sender in the list only
			if not defaultSender:
				defaultSender.append(row)
				defaultName = [row['senderFirstName']]
			# If the username of the session is listed in the "sender" database return just those sender details:
			if str(session.user).lower() in str(row['senderFirstName']).lower():
				senderDetails.append(row)
				senderName = [row['senderFirstName']]

		if not defaultSender:
			self.logWarning(self.randomTalk(text="systemErrorNoSender"))
			return
		if senderDetails:
			if onlyName:
				return senderName
			else:
				return senderDetails
		else:
			if onlyName:
				return defaultName
			else:
				return defaultSender

	def fetchDbContacts(self, table: str):
		"""
		Retrieves the list of contacts from the database
		:param table: The table to retrieve from
		:return:
		"""
		contacts = list()
		for row in self.databaseFetch(tableName=table, query='SELECT * FROM :__table__ '):
			contacts.append(row)
		return contacts

	def deleteTable(self, tableName: str):
		"""
		Deletes entire table ready for new additions
		:param tableName: the table to delete
		:return:
		"""
		self.DatabaseManager.delete(
			tableName=tableName,
			query='DELETE FROM :__table__ ',
			callerName=self.name)



### - ### - ### PROCESS CONFIG DETAILS ### - ### - ###
	def updateDatabaseDetails(self, _):
		"""
		Triggered by clicking confirm button after making changes in the skill settings
		Give the config file time to update then run through the database update procedure
		:return: true
		"""

		self.ThreadManager.doLater(
			interval=4,
			func=self.smsSenderDetails
		)
		return True

	def smsSenderDetails(self):
		if self.getConfig('smsSenderDetails'):
			self.deleteTable(tableName=self._SENDERDETAILS)
			self.seperateStringValues(value=self.getConfig('smsSenderDetails'), caller='smsSenderDetails')

		self.smsRecipientDetails()

	def smsRecipientDetails(self):
		if self.getConfig('smsRecipientDetails'):
			self.deleteTable(tableName=self._SMSRECIPIENT)
			self.seperateStringValues(value=self.getConfig('smsRecipientDetails'), caller='smsRecipientDetails')
		self.telegramRecipientDetails()

	def telegramRecipientDetails(self):
		self._dbTrigger =True
		if self.getConfig('telegramRecipientDetails'):
			self.deleteTable(tableName=self._TELEGRAMRECIPIENTS)
			self.seperateStringValues(value=self.getConfig('telegramRecipientDetails'), caller='telegramRecipientDetails')

	def errorCheckForPeopleThatDontRead(self, data, caller) -> bool:
		error = False
		if not self.getConfig('smsSenderDetails') and self.getConfig('smsRecipientDetails') or not self.getConfig('smsRecipientDetails') and self.getConfig('smsSenderDetails'):
			self.logWarning(self.randomTalk(text="systemConfigWarning1"))
			error = True

		if "smsSenderDetails" in caller :
			if not len(data.split('/')) == 3:
				self.logWarning(self.randomTalk(text="systemConfigWarning2", replace=[len(data.split('/'))]))
				error = True
			if not '@' in data.split('/')[1]:
				self.logWarning(self.randomTalk(text="systemConfigWarning3", replace=[data.split('/')[1]]))
				error = True
			return error

		elif 'smsRecipientDetails' in caller :
			if not len(data.split('/')) == 4 :
				self.logWarning(self.randomTalk(text="systemConfigWarning4", replace=[len(data.split('/'))]))
				self.logInfo(f" example : Mike/0800123456/yes/@txt.att.net")
				error = True
			if not len(data.split('/')[1]) == 10:
				self.logWarning(self.randomTalk(text="systemConfigWarning5", replace=[len(data.split('/')[1])]))
				error = True
			if not 'yes' in data.split('/')[2] and not 'no' in data.split('/')[2]:
				self.logWarning(self.randomTalk(text="systemConfigWarning6", replace=[data.split('/')[2]]))
				error = True
			if not '@' in data.split('/')[3]:
				self.logWarning(self.randomTalk(text="systemConfigWarning7", replace=[data.split('/')[3]]))
				error = True
			return error
		if 'telegramRecipientDetails' in caller:
			if not len(data.split('/')) == 4 :
				self.logWarning(self.randomTalk(text="systemConfigWarning8", replace=[len(data.split('/'))]))
				self.logInfo(f"Example : Mike/lisa/123456/no")
				error = True
			if not 'yes' in data.split('/')[3] and not 'no' in data.split('/')[3]:
				self.logWarning(self.randomTalk(text="systemConfigWarning9", replace=[data.split('/')[3]]))
				error = True
			return error

	def seperateStringValues(self, value : str, caller : str):
		"""
		Used for seperating the config strings and add the right values in the database
		:param value: The config values
		:param caller: The db table to send to
		:return:
		"""

		for data in value.split(','):
			try:
				if self.errorCheckForPeopleThatDontRead(data=data, caller=caller):
					self.say(
						text="You've made a mistake in the skill settings. Please check my logs"
					)
					return

				if 'smsSenderDetails' in caller :
					firstName = data.split('/')[0]
					email = data.split('/')[1]
					pwd = data.split('/')[2]

					self.addToSenderTable(senderFirstName=firstName, email=email, password=pwd)

				elif 'smsRecipientDetails' in caller :
					firstName = data.split('/')[0]
					phoneNumber = data.split('/')[1]
					eContact = data.split('/')[2]
					smsGateway = data.split('/')[3]

					self.addToSmsTable(recipientName=firstName, recipientPhoneNumber=phoneNumber, emergencyContact=eContact, smsGateway=smsGateway)
				else:

					yourFirstName = data.split('/')[0]
					theirFirstName = data.split('/')[1]
					thierChatId = data.split('/')[2]
					eContact = data.split('/')[3]

					self.addToTelegramTable(senderFirstName=yourFirstName.lstrip(" "), recipientName=theirFirstName, recipientChatId=int(thierChatId), emergencyContact=eContact.lower())


			except Exception as e:
					self.logInfo(self.randomTalk(text="systemIssueUpdatingDatabase", replace=[e]))
					continue

		if self._dbTrigger:
			self.logInfo(self.randomTalk(text="systemFinishedDatabaseUpdate"))
			self._dbTrigger = False

	def setEmailProperties(self, session = None):
		"""
		Set the properties of email configuration items.
		added to allow autoconfiguration if skill expands in features... perhaps
		:param session: The dialog session
		:return: Senders email, Senders email password, SMTP port number
		"""
		if session:
			senderDetails = self.fetchSenderDetail(session=session)
		else:
			senderDetails = self.fetchDbContacts(table=self._SENDERDETAILS)

		if not senderDetails:
			self.endDialog(
				sessionId=session.sessionId,
				text=self.randomTalk(text="fillInSenderDetails"),
				deviceUid=session.deviceUid
			)

		for contacts in senderDetails:
			pwd = contacts['password']
			email :str = contacts['email']
			port = 587

			# The below is preperation for future additions
			if "gmail.com" in email.split('@')[1]:
				port = 587

			return email, pwd, port

