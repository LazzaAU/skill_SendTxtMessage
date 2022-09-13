from core.base.model.AliceSkill import AliceSkill
from core.dialog.model.DialogSession import DialogSession
from core.util.Decorators import IntentHandler


class SendTxtMessage(AliceSkill):
	"""
Author: Lazza
Description: send a text message using alice
"""


	def __init__(self):

		super().__init__()


	@IntentHandler('ForceBackup')
	def dummyIntent(self, session: DialogSession):
		pass
