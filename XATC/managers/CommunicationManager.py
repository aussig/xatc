#
#  CommunicationManager.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XPLMProcessing import *

from XATC.communication import Frequency
from XATC.communication import CommunicationConstants

# FlightLoop callback frequency (1 second)
FLIGHTLOOP_CALLBACK_FREQUENCY = 1

class CommunicationManager:
	""" Handles communication between aircraft and the ground """
	
	def __init__(self, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC
		# Currently active ATCs, by frequency
		self.currentATCs = {}
		# Currently active Aircraft, by callsign
		self.currentAircraft = {}
		# Currently active frequencies
		self.currentFrequencies = {}

		# Register our flightloop callback
		self.flightLoopCB = self.flightLoopCallback
		XPLMRegisterFlightLoopCallback(self.XATC, self.flightLoopCB, FLIGHTLOOP_CALLBACK_FREQUENCY, 0)


	def flightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		""" Flight loop callback """
		self.work()
		return FLIGHTLOOP_CALLBACK_FREQUENCY
		

	def work(self):
		""" Perform regular actions """
		for frequency in self.getCurrentFrequencies():
			frequency.work()


	#
	# ATC Methods
	#
	
	def registerATC(self, atc):
		""" Register an ATC as listening on a frequency """
		self.currentATCs[atc.frequencyStr] = atc
	
	
	def unregisterATC(self, atc):
		""" Unregister an ATC """
		del self.currentATCs[atc.frequencyStr]
	
	
	def getATC(self, frequency):
		""" Get an ATC by its frequency """
		if (frequency == CommunicationConstants.NO_ID): return None
		return self.currentATCs.get(frequency)
	
	
	def getFrequency(self, frequency):
		""" Get a Frequency """
		return self.currentFrequencies.get(frequency)
	
	
	def getCurrentFrequencies(self):
		""" Get the list of current frequencies """
		return self.currentFrequencies.values()
	
	
	def getCurrentATCs(self):
		""" Get the list of current ATCs """
		return self.currentATCs.values()


	#
	# Aircraft Methods
	#

	def registerAircraft(self, aircraft):
		""" Register an Aircraft """
		self.currentAircraft[aircraft.callsign] = aircraft


	def unregisterAircraft(self, aircraft):
		""" Unregister an Aircraft """
		del self.currentAircraft[aircraft.callsign]

	def getAircraft(self, callsign):
		""" Get an Aircraft by its frequency """
		if (callsign == CommunicationConstants.NO_ID): return None
		return self.currentAircraft[callsign]

	def getCurrentAircraft(self):
		""" Get the list of current Aircraft """
		return self.currentAircraft.values()

	def leaveFrequency(self, receiver, frequencyStr):
		""" Remove a receiver from a frequency. Also remove the frequency if the last receiver has left """
		frequency = self.currentFrequencies.get(frequencyStr)
		if (frequency != None):
			if (frequency.removeReceiver(receiver)):
				del self.currentFrequencies[frequencyStr]


	def joinFrequency(self, receiver, frequencyStr):
		""" Add a receiver to a frequency """
		frequency = self.currentFrequencies.get(frequencyStr)
		if (frequency == None):
			frequency = Frequency.Frequency(frequencyStr, self.XATC)
			self.currentFrequencies[frequencyStr] = frequency
		frequency.addReceiver(receiver)


	def transmit(self, sender, frequencyStr, message):
		""" Transmit a message on a frequency """
		frequency = self.currentFrequencies.get(frequencyStr)
		if (frequency != None):
			frequency.transmit(sender, message)
		else:
			# This is an error condition, someone is trying to transmit on a frequency that hasn't been initialised.
			print "ERROR in CommunicationManager: " + sender + " is trying to communicate on frequency " + frequencyStr + " that doesn't exist"
			
