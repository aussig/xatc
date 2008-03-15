#
#  CenterZone.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.zones import Zone
from XATC.atc import CenterATC

class CenterZone(Zone.Zone):
	""" Handles a Center / ARTCC zone """
	
	def __init__(self, id, name, frequency, XATC):
		""" Constructor """
		# Call superclass constructor, passing in None for associated airport zone (Centers don't control an airport)
		Zone.Zone.__init__(self, id, name, XATC)
		# Create our ATC
		self.atc = CenterATC.CenterATC(self, name, frequency, XATC)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Call superclass method
		Zone.Zone.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
