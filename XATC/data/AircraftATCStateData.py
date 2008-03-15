#
#  AircraftATCStateData.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

class AircraftATCStateData:
	""" Encapsulates an aircraft's ATC state """
	
	def __init__(self, aircraft, initialCommState):
		""" Constructor """
		# The aircraft object attached to this state
		self.aircraft = aircraft
		# The current communication state of this aircraft
		self.currentCommState = initialCommState


	def __str__(self):
		""" Convenience method for debugging """
		return "AircraftATCStateData: aircraft=" + self.aircraft + ", currentCommState=" + self.currentCommState
		

	def getState(self):
		""" Get the current state """
		return self.currentCommState


	def setState(self, newState):
		""" Change the state, tell the aircraft the state has changed """
		self.currentCommState = newState
		self.aircraft.stateChanged()
