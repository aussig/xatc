#
#  TowerATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.atc import ATC
from XATC.communication import CommunicationConstants
from XATC.communication import MenuItem

# The callsign suffix for this ATC
CALLSIGN_SUFFIX = "Ground"

# The available actions that this ATC responds to
ACTIONS = {"REQUEST_TAXI_REMAIN": 2000, "REQUEST_TAXI_NORTH": 2001, "REQUEST_TAXI_SOUTH": 2002, "REQUEST_TAXI_EAST": 2003,"REQUEST_TAXI_WEST": 2004}

class GroundATC(ATC.ATC):
	""" Handles a ground ATC """
 
	def __init__(self, zone, name, frequencyStr, XATC):
		""" Constructor """
		# Call the superclass constructor
		ATC.ATC.__init__(self, zone, name + " " + CALLSIGN_SUFFIX, frequencyStr, XATC)


	def getMenu(self, aircraft):
		menu = []
		
		menu.append(MenuItem.MenuItem("Request taxi to active - Remain in pattern", ACTIONS["REQUEST_TAXI_REMAIN"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting taxi to active, indending to remain in pattern"))
		menu.append(MenuItem.MenuItem("Request taxi to active - Depart North", ACTIONS["REQUEST_TAXI_NORTH"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting taxi to active, indending to depart to the North"))
		menu.append(MenuItem.MenuItem("Request taxi to active - Depart South", ACTIONS["REQUEST_TAXI_SOUTH"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting taxi to active, indending to depart to the South"))
		menu.append(MenuItem.MenuItem("Request taxi to active - Depart East", ACTIONS["REQUEST_TAXI_EAST"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting taxi to active, indending to depart to the East"))
		menu.append(MenuItem.MenuItem("Request taxi to active - Depart West", ACTIONS["REQUEST_TAXI_WEST"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting taxi to active, indending to depart to the West"))
		
		return menu;


	def work(self):
		""" Perform regular actions """
		# Call the superclass work method
		ATC.ATC.work(self)


	def handleClearRadioTransmission(self, sender, data):
		""" Handle a properly received incoming radio transmission """
		# Call the superclass handleClearRadioTransmission method
		ATC.ATC.handleClearRadioTransmission(self, sender, data)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this ATC """
		# Call superclass method
		ATC.ATC.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
