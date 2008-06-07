#
#  Aircraft.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XPLMProcessing import *

# The states an aircraft can be in
STATES = {"NOT_MOVED" : 0, "TAXYING": 1, "STOPPED": 2, "AIRBORNE": 3}

# FlightLoop callback frequency (1 second)
FLIGHTLOOP_CALLBACK_FREQUENCY = 1

class Aircraft:
	""" Superclass for all aircraft types """
	
	def __init__(self, callsign, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC
		# The callsign of this aircraft
		self.callsign = callsign
		# The current active frequency
		self.currentFrequency = ""
		# The current active ATC
		self.currentATC = None
		# The current state
		self.currentState = STATES["NOT_MOVED"]

		# Register our flight loop callback
		self.flightLoopCB = self.flightLoopCallback
		XPLMRegisterFlightLoopCallback(self.XATC, self.flightLoopCB, FLIGHTLOOP_CALLBACK_FREQUENCY, 0)

		
	def __str__(self):
		""" Convenience toString method """
		return "Aircraft " + self.callsign


	def flightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		""" Flight loop callback """
		self.work()
		return FLIGHTLOOP_CALLBACK_FREQUENCY
		

	def getID(self):
		""" MessageHandler required method """
		return self.callsign


	def getGroundspeed(self):
		""" Get the groundSpeed of the aircraft in meters/s, subclasses should override """
		return 0
		
		
	def getAGL(self):
		""" Get the height AGL of the aircraft in meters, subclasses should override """
		return 0


	def handleMessage(self, message):
		""" Message handler """
		return None


	def stateChanged(self):
		""" Called when the aircraft state is changed """
		return None


	def work(self):
		""" This is the main work method for the Aircraft. Subclasses must implement this method to do their stuff periodically. """
		# We need to update the state we are in, based on what the aircraft is currently doing
		newState = self.currentState

		if (self.getAGL() > 1): newState = STATES["AIRBORNE"]
		elif (self.getGroundspeed() > 3): newState = STATES["TAXYING"]
		elif (self.currentState != STATES["NOT_MOVED"]): newState = STATES["STOPPED"]

		if (newState != self.currentState):
			self.currentState = newState
			self.stateChanged()

		return None



	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this Aircraft """
		# Default method does nothing, implement in subclasses
		pass