#
#  ControlledAirportZone.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.zones import AirportZone
from XATC.atc import AGCSATC

class UncontrolledAirportZone(AirportZone.AirportZone):
	""" A zone representing an uncontrolled airport """
	
	def __init__(self, id, name, AGCSFrequency, XATC):
		""" Constructor """
		# Call superclass constructor
		AirportZone.AirportZone.__init__(self, id, name, XATC)

		# The airport radio / CTAS ATC
		if (AGCSFrequency != None): self.AGCSATC = AGCSATC.AGCSATC(self, name, AGCSFrequency, XATC)
		else: self.AGCSATC = None


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Call superclass method
		AirportZone.AirportZone.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
