#
#  Frequency.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

import time

from XPLMProcessing import *

from XATC.communication import Message
from XATC.communication import CommunicationConstants

# Some constants for calculating how long it takes to say a phrase
SPOKEN_TEXT_MINIMUM_DURATION = 1500
SPOKEN_TEXT_WORD_DURATION = 400
SPOKEN_TEXT_COMMA_DURATION = 400

# The message to use if there is a garbled transmission */
MESSAGE_GARBLED = Message.Message(Message.TYPES["RADIO_TRANSMISSION_INTERRUPTED"], None, None, None)

class Frequency:
	""" A radio frequency """

	def __init__(self, frequencyStr, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC
		# The frequency as a String
		self.frequencyStr = frequencyStr
		# The communication queue
		self.currentMessage = None
		# The current transmission end time
		self.transmissionEndTime = -1
		# list of all ATCs and Aircraft on this frequency
		self.receivers = []


	def getID(self):
		""" MessageHandler required method """
		return self.frequencyStr


	def handleMessage(self, message):
		""" Handle an incoming message """
		pass


	def transmit(self, sender, message):
		""" Start transmission of a message """
		if (self.currentMessage != None):
			# There is a message already being broadcast, send a messageGarbled to everyone and clear the current message
			self.currentMessage = None
			self.doTransmit(sender, MESSAGE_GARBLED)
		else:
			# Set the current message
			self.currentMessage = message
			# Calculate how long it would take to say
			words = message.data.text.split()
			commas = message.data.text.split(",")
			self.transmissionEndTime = int(time.clock() * 1000) + len(words) * SPOKEN_TEXT_WORD_DURATION + (len(commas) - 1) * SPOKEN_TEXT_COMMA_DURATION + SPOKEN_TEXT_MINIMUM_DURATION;
			# Set type to transmission started
			message.type = Message.TYPES["INCOMING_RADIO_TRANSMISSION_STARTED"]

			self.doTransmit(sender, message)


	def doTransmit(self, sender, message):
		""" Send a Message to all our recipients """
		self.replaceParameters(message)

		for receiver in self.receivers:
			# Send message if data is null (broadcast) or original message receiver is null (broadcast), or receiver is intended recipient or receiver is original sender
			if (message.data == None or message.receiver == None or message.receiver == receiver or receiver == sender):
				receiver.handleMessage(message)


	def work(self):
		""" Perform regular actions """
		# If there is no current message then there is nothing to do
		if (self.currentMessage == None): return

		if (int(time.clock() * 1000) >= self.transmissionEndTime):
			# A transmission was in progress, it has now ended, send completed message using the same message data as the original message
			self.currentMessage.type = Message.TYPES["INCOMING_RADIO_TRANSMISSION_COMPLETED"]
			self.doTransmit(self.currentMessage.sender, self.currentMessage)
			self.currentMessage = None


	def transmissionUnderway(self):
		""" Return true if a transmission is underway """
		return self.currentMessage != None


	def addReceiver(self, receiver):
		""" Add a receiver to the list of receivers """
		if (receiver not in self.receivers): self.receivers.append(receiver)


	def removeReceiver(self, receiver):
		""" Remove a receiver from the list of receivers """
		self.receivers.remove(receiver)
		return (len(self.receivers) == 0)


	def replaceParameters(self, message):
		""" Replace parameters in a RadioMessageData object relevant to a frequency """
		if (message.data != None):
			# Get the sender and receiver to replace the parameters that they know about too.  In the case of ATC, the superclass also calls replaceParameters() for its associated Zone.

			# Recipient callsign. message.receiver may be None if the transmission is to all stations (e.g. ATIS)
			if (message.receiver != None):
				message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"], message.receiver.getID())
				message.receiver.replaceParameters(message)
				
			# Sender callsign. message.sender shouldn't be None
			if (message.sender != None):
				message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"], message.sender.getID())
				message.sender.replaceParameters(message)

			# Frequency
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["FREQUENCY"], formatFrequency(self.frequencyStr))
			
#
# Module methods
#

def formatFrequency(frequencyStr):
	""" Format a frequency nicely for display and spoken """
	if (len(frequencyStr) == 5):
		return frequencyStr[0:3] + '.' + frequencyStr[3:]
	else:
		return frequencyStr

