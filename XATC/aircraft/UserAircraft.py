#
#  UserAircraft.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XPLMDataAccess import *

from XATC.aircraft import Aircraft
from XATC.communication import CommunicationConstants
from XATC.communication import Message
from XATC.atc import ATC

# The COM1 Radio data ref
DATAREF_COM1 = XPLMFindDataRef("sim/cockpit/radios/com1_freq_hz")
# The COM2 Radio data ref
DATAREF_COM2 = XPLMFindDataRef("sim/cockpit/radios/com2_freq_hz")
# The Selected COM radio data ref
DATAREF_SELECTEDCOM = XPLMFindDataRef("sim/cockpit2/radios/actuators/audio_com_selection")
# The Battery switch position data ref
DATAREF_BATTERY_STATE = XPLMFindDataRef("sim/cockpit/electrical/battery_on")
# The Avionics switch position data ref
DATAREF_AVIONICS_STATE = XPLMFindDataRef("sim/cockpit/electrical/avionics_on")
# The ground speed data ref
DATAREF_GROUND_SPEED = XPLMFindDataRef("sim/flightmodel/position/groundspeed")
# The height above ground level
DATAREF_AGL = XPLMFindDataRef("sim/flightmodel/position/y_agl")
# The aircraft latitude
DATAREF_LATITUDE = XPLMFindDataRef("sim/flightmodel/position/latitude")
# The aircraft longitude
DATAREF_LONGITUDE = XPLMFindDataRef("sim/flightmodel/position/longitude")
# The aircraft indicated altitude
DATAREF_INDICATED_ALTITUDE = XPLMFindDataRef("sim/flightmodel/misc/h_ind")
# The aircraft barometric pressure
DATAREF_BAROMETER_SEALEVEL = XPLMFindDataRef("sim/weather/barometer_sealevel_inhg")
# The aircraft indicated compass heading
DATAREF_INDICATED_COMPASS = XPLMFindDataRef("sim/cockpit/misc/compass_indicated")

# Dataref constants
SELECTED_COM1 = 6
SELECTED_COM2 = 7
BATTERY_ON = 1
AVIONICS_ON = 1



class UserAircraft(Aircraft.Aircraft):
	""" Manages the user's aircraft """

	def __init__(self, callsign, XATC):
		""" Constructor """
		Aircraft.Aircraft.__init__(self, callsign, XATC)


	def handleMessage(self, message):
		""" Message handler """
		Aircraft.Aircraft.handleMessage(self, message)

		if (message.type == Message.TYPES["INCOMING_RADIO_TRANSMISSION_STARTED"]):
			# Incoming radio transmission started (probably from an ATC), speak it
			self.XATC.uiManager.displayMessageToUser(message)

		elif (message.type == Message.TYPES["INCOMING_RADIO_TRANSMISSION_COMPLETED"]):
			# Incoming radio transmission completed (probably from an ATC)
			print "data: " + str(message.data)
			
			if (message.data == None or len(message.data.actions) == 0):
				# Nothing to do, ignore
				pass
				
			elif (message.data.actions[0] == ATC.ACTIONS["ACKNOWLEDGED"]):
				# Simple acknowledgement, ignore
				pass

		elif (message.type == Message.TYPES["RADIO_TRANSMISSION_INTERRUPTED"]):
			# Garbled message received, do nothing (aircraft shouldn't respond, it's the ATCs job)
			pass


	def work(self):
		""" Perform regular actions """
		# Call superclass work method
		Aircraft.Aircraft.work(self)

		# Check the state of battery / avionics and selected com frequency 
		frequency = CommunicationConstants.NO_ID		
		if (XPLMGetDatai(DATAREF_BATTERY_STATE) == BATTERY_ON and XPLMGetDatai(DATAREF_AVIONICS_STATE) == AVIONICS_ON):
			if (XPLMGetDatai(DATAREF_SELECTEDCOM) == SELECTED_COM1): frequency = str(XPLMGetDatai(DATAREF_COM1))
			elif (XPLMGetDatai(DATAREF_SELECTEDCOM) == SELECTED_COM2): frequency = str(XPLMGetDatai(DATAREF_COM2))
		if (not frequency == self.currentFrequency): self.frequencyChanged(frequency)


	def frequencyChanged(self, newFrequency):
		""" Currently tuned frequency changed """
		self.XATC.communicationManager.leaveFrequency(self, self.currentFrequency)
		self.currentFrequency = newFrequency
		self.XATC.communicationManager.joinFrequency(self, self.currentFrequency)
		self.currentATC = self.XATC.communicationManager.getATC(self.currentFrequency)

		# Clear any current speaking
		self.XATC.uiManager.stopSpeaking()

		if (self.currentATC == None):
			# Clear any current menu
			self.XATC.uiManager.showMenu(None)
		else:
			# Display the appropriate menu for the ATC
			self.XATC.uiManager.showMenu(self.currentATC.getMenu(self))


	def changeFrequency(self, newFrequency):
		""" Set the X-Plane frequency """
		if (XPLMGetDatai(DATAREF_SELECTEDCOM) == SELECTED_COM1): XPLMSetDatai(DATAREF_COM1, int(newFrequency))
		elif (XPLMGetDatai(DATAREF_SELECTEDCOM) == SELECTED_COM2): XPLMSetDatai(DATAREF_COM2, int(newFrequency))


	def stateChanged(self):
		""" Called when the aircraft state changes """
		# Get the menu of options from the ATC
		print "USER AIRCRAFT STATE CHANGED: " + str(self.currentState)
		if (self.currentATC == None):
			# Clear any current menu
			self.XATC.uiManager.showMenu(None)
		else:
			# Display the appropriate menu for the ATC
			self.XATC.uiManager.showMenu(self.currentATC.getMenu(self))


	def getGroundspeed(self):
		""" Get the ground speed of the aircraft in meters/s """
		return XPLMGetDataf(DATAREF_GROUND_SPEED)
		
	def getAGL(self):
		""" Get the height above ground level of the aircraft in meters """
		return XPLMGetDataf(DATAREF_AGL)

	def getLatitude(self):
		""" Get the latitude of the aircraft in degrees """
		return XPLMGetDataf(DATAREF_LATITUDE)

	def getLongitude(self):
		""" Get the longitude of the aircraft in degrees """
		return XPLMGetDataf(DATAREF_LONGITUDE)

	def getQNH(self):
		""" Get the aircraft QNH """
		return XPLMGetDataf(DATAREF_BAROMETER_SEALEVEL)
		
	def getIndicatedAltitude(self):
		""" Get the indicated altitude in ??? """
		return XPLMGetDataf(DATAREF_INDICATED_ALTITUDE)

	def getIndicatedHeading(self):
		""" Get the aircraft indicated heading """
		XPLMGetDataf(DATAREF_INDICATED_COMPASS)
		
		
	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this Aircraft """
		# Call superclass method
		Aircraft.Aircraft.replaceParameters(self, message)

		if (message.data != None):
			# Altitude
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["ALTITUDE_FEET"], str(self.getIndicatedAltitude()))
			# Location relative to airfield
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["LOCATION_RELATIVE_TO_AIRFIELD"], "somewhere nearby")
			# Aircraft type
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRCRAFT_TYPE"], "Cessna 172")
			# Originating airport
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["ORIGINATING_AIRPORT"], "Bath")
			# Destination airport
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["DESTINATION_AIRPORT"], "Jersey")
			# Aircraft QNH
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRCRAFT_QNH"], str(self.getQNH()))
			# Aircraft Heading
			message.data.text = message.data.text.replace(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["HEADING"], str(self.getIndicatedHeading()))

