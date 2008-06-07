#
#  ATISATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.atc import ATC
from XATC.communication import CommunicationConstants

# The callsign suffix for this ATC
CALLSIGN_SUFFIX = "ATIS"

class ATISATC(ATC.ATC):
	""" Handles an ATIS ATC """

	def __init__(self, zone, name, frequencyStr, XATC):
		""" Constructor """
		# Call the superclass constructor
		ATC.ATC.__init__(self, zone, name + " " + CALLSIGN_SUFFIX, frequencyStr, XATC)


	def work(self):
		""" Perform regular actions """
		# Call the superclass work method
		ATC.ATC.work(self)
		
		# Loop transmission
		if (not self.transmissionPending()):
			if (self.zone == None): return
			currentWeatherData = self.zone.currentWeatherData
			if (currentWeatherData == None): return

			# Station name and information ID
			content = self.zone.name + " information " + CommunicationConstants.ALPHANUMERIC_STRING[self.zone.currentATISInfoID] + " "
			content += currentWeatherData
			#content += "Visual runway 2 4 L and ILS runway 2 4 R in use. "
			content += "Landing and departing runway " + self.zone.currentRunwayID + ". " # "2 4 L and 2 4 R. "
			content += "VFR aircraft say direction of flight. "
			content += "All aircraft readback hold short instructions. "
			content += "Advise controller on initial contact you have " + CommunicationConstants.ALPHANUMERIC_STRING[self.zone.currentATISInfoID] + "."

			self.queueTransmission(content, [ATC.ACTIONS["BROADCAST"]], None)

	def handleClearRadioTransmission(self, sender, data):
		""" Handle a properly received incoming radio transmission. Do nothing, no response from automated recording. """
		pass

	def handleConflictingRadioTransmission(self, sender, data):
		""" Handle an improperly received incoming radio transmission. Do nothing, no response from automated recording. """
		pass


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this ATC """
		# Call superclass method
		ATC.ATC.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
