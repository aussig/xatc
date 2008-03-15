#
#  Message.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

# Possible message types
TYPES = {"NONE": 0, "ACTION": 1, "INCOMING_RADIO_TRANSMISSION_STARTED": 100, "INCOMING_RADIO_TRANSMISSION_COMPLETED": 101, "RADIO_TRANSMISSION_INTERRUPTED": 102, "OUTGOING_RADIO_TRANSMISSION_COMPLETED": 103}

class Message:
	""" A class for encapsulating a message """

	def __init__(self, type, sender, receiver, data):
		""" Constructor """
		# This message's type
		self.type = type
		# The message sender
		self.sender = sender
		# The message receiver
		self.receiver = receiver
		# Additional attached data
		self.data = data


	def __str__(self):
		""" Convenience method for debugging """
		result = "Message: type=" + str(self.type)
		if (self.data != None): result += ", data=" + str(self.data)
		return result

