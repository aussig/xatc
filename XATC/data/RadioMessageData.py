#
#  RadioMessageData.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

class RadioMessageData:
	""" Encapsulates a radio message """
	
	def __init__(self, actions, text):
		""" Constructor """
		# The actions attached to the transmission
		self.actions = actions
		# The text of the transmission
		self.text = text

	def __str__(self):
		""" Convenience method for debugging """
		return "RadioMessageData: actions=" + str(self.actions) + ", text=" + self.text