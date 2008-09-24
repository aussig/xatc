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
	""" Manages an airport zone """

	def __init__(self, id, name, XATC):
		""" Constructor """
		# Call superclass constructor
		Zone.Zone.__init__(self, id, name, XATC)

		# The current information identifier (Alpha, Bravo etc.)
		self.currentATISInfoID = int((random.random() * (CommunicationConstants.ALPHA_ID_MAX - CommunicationConstants.ALPHA_ID_MIN))) + CommunicationConstants.ALPHA_ID_MIN
		# The current weather data
		self.currentWeatherDataStr = None
		# The current METAR object
		self.currentMetar = None
		# The VFR landing runway
		self.vfrLandingRunway = "10"
		# The VFR departing runway
		self.vfrDepartingRunway = "10"
		# The IFR landing runway
		self.ifrLandingRunway = "24 L"
		# The IFR departing runway
		self.ifrDepartingRunway = "24 R"
		# The location of this AirportZone (for purposes of calculating weather, etc.)
		self.location = {"latitude": 0, "longitude": 0}
		# The field elevation in feet
		self.fieldElevation = 0
		# The QNH in mb
		self.qnh = 1013
		# The QFE in mb
		self.qfe = self.qnh - self.fieldElevation / 27.7   # This calculation works ok at around 1000ft elevation
		# The wind direction
		self.windDirection = 0
		# The wind speed in knots
		self.windSpeed = 0
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
		newMetar = WeatherServices.getWeatherData(self.id)
		newWeatherData = WeatherServices.getHumanReadableMetar(newMetar)
		
		# Check whether the information needs incrementing
		if (self.currentWeatherDataStr == None or newWeatherData != self.currentWeatherDataStr):
			# Increment the identifier
			self.currentATISInfoID = self.currentATISInfoID + 1
			if (self.currentATISInfoID > CommunicationConstants.ALPHA_ID_MAX): self.currentATISInfoID = CommunicationConstants.ALPHA_ID_MIN
			# Set the weather data
			self.currentMetar = newMetar
			self.currentWeatherDataStr = newWeatherData
			self.processMetar()
			print self.id + " new Metar loaded: (information " + CommunicationConstants.ALPHANUMERIC_STRING[self.currentATISInfoID] + ")"
			print self.currentWeatherDataStr


	def processMetar(self):
		if self.currentMetar == None: return
		
		if self.currentMetar.press != None:
			self.qnh = self.currentMetar.press.value("MB")
			self.qfe = self.qnh - self.fieldElevation / 27.7
		if self.currentMetar.wind_dir != None: self.windDirection = self.currentMetar.wind_dir.value()
		if self.currentMetar.wind_speed != None: self.windSpeed = self.currentMetar.wind_speed.value("KT")
		
		
	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Call superclass method
		Zone.Zone.replaceParameters(self, message)
		
		if (message.data != None):
			# VFR Runway, default to landing
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"], self.vfrLandingRunway)
			# VFR Landing Runway
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_LANDING_RUNWAY"], self.vfrLandingRunway)
			# VFR Departing Runway
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_DEPARTING_RUNWAY"], self.vfrDepartingRunway)
			# IFR Runway, default to landing
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["IFR_RUNWAY"], self.ifrLandingRunway)
			# IFR Landing Runway
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["IFR_LANDING_RUNWAY"], self.ifrLandingRunway)
			# IFR Departing Runway
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["IFR_DEPARTING_RUNWAY"], self.ifrDepartingRunway)
			# Circuit direction
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"], self.circuitDirection)
			# Airfield QNH
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"], str(self.qnh))
			# Airfield QFE
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QFE"], str(self.qfe))
			# Airfield wind direction
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_DIRECTION"], str(self.windDirection))
			# Airfield wind speed
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_SPEED"], str(self.windSpeed))
			# Airfield wind speed
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_NAME"], self.name)
			
			# Traffic is going to be complicated, I anticipate leaving it until last, and once we've got AI aircraft implemented too.
			# Traffic may also need to be inserted into the radio message by the ATC, not the zone, so this may need to be moved to the ATC replaceParameters() method
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"], "no known traffic")
