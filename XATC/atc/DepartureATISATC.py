#
#  DepartureATISATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.atc import ATISATC

# The callsign suffix for this ATC
CALLSIGN_SUFFIX = "Departure"

class DepartureATISATC(ATISATC.ATISATC):
	""" Handles a departure ATIS ATC """

	def __init__(self, zone, name, frequencyStr, XATC):
		""" Constructor """
		# Call the superclass constructor
		ATISATC.ATISATC.__init__(self, zone, name + " " + CALLSIGN_SUFFIX, frequencyStr, XATC)


	def work(self):
		""" Perform regular actions """
		# Call the superclass work method
		ATISATC.ATISATC.work(self)


	def handleClearRadioTransmission(self, sender, data):
		""" Handle a properly received incoming radio transmission """
		# Call the superclass handleClearRadioTransmission method
		ATISATC.ATISATC.handleClearRadioTransmission(self, sender, data)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this ATC """
		# Call superclass method
		ATC.ATC.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
