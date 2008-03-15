#
#  CenterATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

import re

from XPLMProcessing import *

from XATC.communication import Message
from XATC.data import RadioMessageData
from XATC.data import AircraftATCStateData
from XATC.communication import MenuItem
from XATC.communication import CommunicationConstants

# The ATC actions available for all ATCs
ACTIONS = {"NOOP": 0, "BROADCAST": 1, "ACKNOWLEDGED": 2, "RESET": 3}
# The communication states available across all ATCs, stored in instances of AircraftATCStateData
COMMUNICATION_STATES = {"NO_CONTACT": 0, "INITIAL_CONTACT": 1}

# FlightLoop callback frequency (1 second)
FLIGHTLOOP_CALLBACK_FREQUENCY = 1

class ATC:
	""" Superclass for all ATC types """
 
	def __init__(self, zone, name, frequencyStr, XATC):
		""" Constructor """
		# The parent plugin */
		self.XATC = XATC
		# The frequency this ATC unit communicates on
		self.frequencyStr = frequencyStr
		# The name of this ATC unit
		self.name = name
		# The zone this ATC unit controls
		self.zone = zone
		# The communication queue
		self.transmitQueue = []
		# The current transmission end time
		self.transmissionEndTime = -1
		# The aircraft this ATC currently knows about, key is aircraft callsign, value is AircraftATCStateData object
		self.aircraftStates = {}

		# Register with the communicationManager
		XATC.communicationManager.registerATC(self)
		XATC.communicationManager.joinFrequency(self, self.frequencyStr)

		# Register our flight loop callback
		self.flightLoopCB = self.flightLoopCallback
		XPLMRegisterFlightLoopCallback(self.XATC, self.flightLoopCB, FLIGHTLOOP_CALLBACK_FREQUENCY, 0)


	def __str__(self):
		""" Convenience toString method """
		return "ATC " + self.name + ": " + self.frequencyStr


	def flightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		""" Flight loop callback """
		self.work()
		return FLIGHTLOOP_CALLBACK_FREQUENCY


	def work(self):
		""" This is the main work method for the ATC unit. Subclasses should implement this method to do their stuff periodically """
		if (self.XATC.communicationManager.getFrequency(self.frequencyStr).transmissionUnderway()):
			# Haven't finished current transmission yet, do nothing
			pass
		elif (self.transmissionPending()):
			# Another message pending, start it
			self.XATC.communicationManager.transmit(self, self.frequencyStr, self.getTopTransmission())


	def getID(self):
		""" Get this ATC's ID """
		return self.name;


	def addResetMenuItem(self, menu):
		""" Utility function for adding information lines to a menu """
		menu.append(MenuItem.MenuItem("[Reset communication with this ATC]", ACTIONS["RESET"], "Communication reset."))


	def handleMessage(self, message):
		""" Handle various incoming messages from other sources """
		if (message.type == Message.TYPES["INCOMING_RADIO_TRANSMISSION_COMPLETED"]):
			# We have received a completed radio transmission, call the subclass method to handle the transmission if it's from someone else, otherwise
			# remove the top transmission from the queue (we get one of these when one of our transmissions has completed too)
			if (message.sender != self):
				self.handleClearRadioTransmission(message.sender, message.data)
			else:
				self.popTopTransmission()

		elif (message.type == Message.TYPES["RADIO_TRANSMISSION_INTERRUPTED"]):
			# We have received a garbled radio transmission
			self.handleConflictingRadioTransmission(message.sender, message.data)


	def queueTransmission(self, messageString, actions, receiver):
		""" Add a transmission to our transmission queue """
		# Split on dot space
		sentences = re.split(r'[\.|,]\s', messageString)
		for sentence in sentences:
			if sentence != "" and sentence != " ":
				message = Message.Message(Message.TYPES["INCOMING_RADIO_TRANSMISSION_STARTED"], self, receiver, RadioMessageData.RadioMessageData(actions, sentence))
				self.replaceParameters(message)
				self.transmitQueue.append(message)


	def popTopTransmission(self):
		""" Pop the first transmission off the transmit queue and return it """
		return self.transmitQueue.pop(0)
	
	
	def getTopTransmission(self):
		""" Get the first transmission off the transmit queue """
		return self.transmitQueue[0]
		

	def transmissionPending(self):
		""" Return true if a transmission is pending """
		return len(self.transmitQueue) > 0


	def getMenu(self, aircraft):
		""" Get a menu of available choices for a given aircaft, subclasses should override this """
		# Default case is to return no menu
		return None


	def getAircraftATCState(self, aircraft):
		""" Get the state data for an aircraft, create a new one if no contact yet """
		stateData = self.aircraftStates.get(aircraft.callsign)
		if (stateData == None):
			stateData = AircraftATCStateData.AircraftATCStateData(aircraft, COMMUNICATION_STATES["NO_CONTACT"])
			self.aircraftStates[aircraft.callsign] = stateData

		return stateData


	def handleClearRadioTransmission(self, sender, data):
		""" Handle a properly received incoming radio transmission """
		aircraftATCState = self.getAircraftATCState(sender)

		if (data.actions[0] == ACTIONS["RESET"]):
			aircraftATCState.setState(COMMUNICATION_STATES["NO_CONTACT"])


	def handleConflictingRadioTransmission(self, sender, data):
		""" Handle an improperly received incoming radio transmission. Default is to request 'say again' """
		self.queueTransmission("Station calling " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " please say again", [], sender)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this ATC """
		# Default method calls replaceParameters on our associated zone.  Implement additional parameters in subclasses.
		self.zone.replaceParameters(message)
		