#
#  AirportZone.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

import random

from XPLMProcessing import *

from XATC.zones import Zone
from XATC.communication import CommunicationConstants
from XATC.services import WeatherServices

# FlightLoop callback frequency (1 hour)
FLIGHTLOOP_CALLBACK_FREQUENCY = 3600

class AirportZone(Zone.Zone):

	def __init__(self, id, name, XATC):
		""" Constructor """
		# Call superclass constructor
		Zone.Zone.__init__(self, id, name, XATC)

		# The current information identifier (Alpha, Bravo etc.)
		self.currentATISInfoID = int((random.random() * (CommunicationConstants.ALPHA_ID_MAX - CommunicationConstants.ALPHA_ID_MIN))) + CommunicationConstants.ALPHA_ID_MIN
		# The current weather data
		self.currentWeatherData = None
		# The VFR runway in use
		self.vfrRunway = "10"
		# The IFR landing runway
		self.ifrLandingRunway = "24L"
		# The IFR departing runway
		self.ifrDepartingRunway = "24R"
		# The location of this AirportZone (for purposes of calculating weather, etc.)
		self.location = {"latitude": 0, "longitude": 0}
		# The QNH
		self.qnh = "qnh_here"
		# The QFE
		self.qfe = "qfe_here"
		# The wind direction
		self.windDirection = "wind_dir_here"
		# The wind speed
		self.windSpeed = "wind_speed_here"
		# The circuit direction
		self.circuitDirection = "left"
		
		# Register our flight loop callback
		self.flightLoopCB = self.flightLoopCallback
		XPLMRegisterFlightLoopCallback(self.XATC, self.flightLoopCB, 1, 0)


	def flightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		""" Flight loop callback """
		self.work()
		return FLIGHTLOOP_CALLBACK_FREQUENCY


	def getID(self):
		""" Get this object's ID """
		return self.name


	def work(self):
		""" This is the main work method for the Airport Zone. Subclasses must implement this method to do their stuff periodically. """
		# Check whether the information needs incrementing
		newWeatherData = WeatherServices.getWeatherData(self.id)
		
		if (self.currentWeatherData == None or newWeatherData != self.currentWeatherData):
			# Increment the identifier
			self.currentATISInfoID = self.currentATISInfoID + 1
			if (self.currentATISInfoID > CommunicationConstants.ALPHA_ID_MAX): self.currentATISInfoID = CommunicationConstants.ALPHA_ID_MIN
			# Set the weather data
			self.currentWeatherData = newWeatherData

			print self.id + " new Metar loaded: (information " + CommunicationConstants.ALPHANUMERIC_STRING[self.currentATISInfoID] + ")"
			print self.currentWeatherData


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Call superclass method
		Zone.Zone.replaceParameters(self, message)
		
		if (message.data != None):
			# VFR Runway
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"], self.vfrRunway)
			# Circuit direction
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"], self.circuitDirection)
			# Airfield QNH
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"], self.qnh)
			# Airfield QFE
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QFE"], self.qfe)
			# Airfield wind direction
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_DIRECTION"], self.windDirection)
			# Airfield wind speed
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_SPEED"], self.windSpeed)
			# Airfield wind speed
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_NAME"], self.name)
			
			# Traffic is going to be complicated, I anticipate leaving it until last, and once we've got AI aircraft implemented too.
			# Traffic may also need to be inserted by the ATC, not the zone, so this may need to be moved to the ATC replaceParameters() method
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"], "no known traffic")
