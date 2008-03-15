#
#  AIAircraft.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XPLMProcessing import *

class AIAircraft(Aircraft.Aircraft):

	def __init__(self, callsign, XATC):
		""" Constructor """
		Aircraft.Aircraft.__init__(self, callsign, XATC)


	def getGroundspeed(self):
		""" Get the groundSpeed of the aircraft in meters/s """
		return 0
		
		
	def getAGL(self):
		""" Get the height AGL of the aircraft in meters """
		return 0


	def handleMessage(self, message):
		""" Message handler """
		return None


	def stateChanged(self):
		""" Called when the aircraft state is changed """
		return None


	def work(self):
		""" This is the main work method for the Aircraft. """
		# Call superclass work method
		Aircraft.Aircraft.work(self)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this Aircraft """
		# Call superclass method
		Aircraft.Aircraft.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
