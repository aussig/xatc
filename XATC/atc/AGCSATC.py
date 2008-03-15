#
#  CenterATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.atc import ATC
from XATC.aircraft import Aircraft
from XATC.communication import MenuItem
from XATC.communication import CommunicationConstants

# The available actions that this ATC responds to
ACTIONS = {"REQUEST_INFO_GROUND": 1000, "READBACK_INFO_GROUND": 1001, "NOTIFY_TAXYING_ACTIVE": 1002, "NOTIFY_HOLDING_ON_GROUND": 1003,"NOTIFY_READY_FOR_DEPARTURE": 1004, "NOTIFY_TAKING_OFF": 1005, "NOTIFY_LINING_UP_TAKING_OFF": 1006, "NOTIFY_LEAVING_CIRCUIT": 1007, "NOTIFY_DOWNWIND": 1008, "NOTIFY_FINAL": 1009, "NOTIFY_GOING_AROUND": 1010, "NOTIFY_CLEAR_ACTIVE": 1011, "INITIAL_CONTACT_AIRBORNE": 1020,"REQUEST_INFO_AIRBORNE": 1021, "NOTIFY_INTENTION_TRANSIT": 1022, "READBACK_INFO_AIRBORNE": 1023, "NOTIFY_OVERHEAD_DESCENDING_DEADSIDE": 1024, "READBACK_INFO_TRANSIT": 1025, "NOTIFY_OVERHEAD_TRANSIT": 1026, "NOTIFY_LEAVING_ATZ": 1027}

# The communication states available across all ATCs, stored in instances of AircraftATCStateData
COMMUNICATION_STATES = {"READBACK_INFO_GROUND": 1000, "NOTIFIED_TAXYING_ACTIVE": 1001, "NOTIFIED_HOLDING_ON_GROUND": 1002, "NOTIFIED_READY_FOR_DEPARTURE": 1003, "NOTIFIED_TAKING_OFF": 1004, "NOTIFIED_DOWNWIND": 1005, "NOTIFIED_FINAL": 1006, "NOTIFIED_FINAL_LANDED": 1007, "NOTIFIED_TRANSIT": 1008, "RECEIVED_INFO_AIRBORNE": 1020, "READBACK_INFO_AIRBORNE": 1021, "READBACK_INFO_TRANSIT": 1022, "NOTIFIED_OVERHEAD_TRANSIT": 1023}

# The callsign suffix for this ATC
CALLSIGN_SUFFIX = "Radio"

class AGCSATC(ATC.ATC):
	""" Air/Ground Communications Service ATC (UK 'Radio', US 'CTAS') """

	def __init__(self, zone, name, frequency, XATC):
		""" Constructor """
		# Call superclass constructor
		ATC.ATC.__init__(self, zone, name + " " + CALLSIGN_SUFFIX, frequency, XATC)
		

	def getMenu(self, aircraft):
		""" Get a menu of actions appropriate to the current circumstances """
		menu = []
		aircraftATCState = self.getAircraftATCState(aircraft)

		if (aircraftATCState.getState() == ATC.COMMUNICATION_STATES["NO_CONTACT"]):
			if (aircraft.currentState == Aircraft.STATES["NOT_MOVED"] or aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addRequestInfoMenuItem(menu)
			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addInitialAirborneContactMenuItem(menu)

		elif (aircraftATCState.getState() == ATC.COMMUNICATION_STATES["INITIAL_CONTACT"]):
			if (aircraft.currentState == Aircraft.STATES["NOT_MOVED"] or aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addReadbackInfoGroundMenuItem(menu)
				self.addReadbackInfoAndTaxyingToActiveMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addAirborneRequestInfoMenuItem(menu)
				self.addAirborneTransitMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["READBACK_INFO_GROUND"]):
			if (aircraft.currentState == Aircraft.STATES["NOT_MOVED"] or aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addTaxyingToActiveMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_TAXYING_ACTIVE"]):
			if (aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addReadyForDepartureMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_READY_FOR_DEPARTURE"]):
			if (aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addHoldingOnGroundMenuItem(menu)
				self.addTakingOffMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_HOLDING_ON_GROUND"]):
			if (aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addLiningUpAndTakingOffMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_TAKING_OFF"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_DOWNWIND"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addFinalMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_FINAL"]):
			if (aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addClearActiveMenuItem(menu)
				# Once landed, put us in the notified final landed state
				aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_FINAL_LANDED"])

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addGoAroundMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_FINAL_LANDED"]):
			if (aircraft.currentState == Aircraft.STATES["TAXYING"] or aircraft.currentState == Aircraft.STATES["STOPPED"]):
				self.addClearActiveMenuItem(menu)

			elif (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addDownwindMenuItem(menu)
				self.addLeavingCircuitNorthMenuItem(menu)
				self.addLeavingCircuitSouthMenuItem(menu)
				self.addLeavingCircuitEastMenuItem(menu)
				self.addLeavingCircuitWestMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["RECEIVED_INFO_AIRBORNE"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addReadbackInfoAirborneMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["READBACK_INFO_AIRBORNE"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addOverheadDescendingDeadsideMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_TRANSIT"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addReadbackInfoTransitMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["READBACK_INFO_TRANSIT"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				self.addReportOverheadMenuItem(menu)

		elif (aircraftATCState.getState() == COMMUNICATION_STATES["NOTIFIED_OVERHEAD_TRANSIT"]):
			if (aircraft.currentState == Aircraft.STATES["AIRBORNE"]):
				addReportLeavingATZ(menu)

		self.addResetMenuItem(menu)

		return menu


	#
	# Utility functions for adding information lines to a menu
	#
	
	def addRequestInfoMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Request radio check and airfield information", ACTIONS["REQUEST_INFO_GROUND"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " requesting radio check " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["FREQUENCY"] + " and airfield information."))

	def addReadbackInfoGroundMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Readback", ACTIONS["READBACK_INFO_GROUND"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " readability 5 also, runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand, QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"] + "."))

	def addReadbackInfoAndTaxyingToActiveMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Readback and report taxying to active", ACTIONS["NOTIFY_TAXYING_ACTIVE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " readability 5 also, taxying for runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand, QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"] + "."))

	def addTaxyingToActiveMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report taxying to active", ACTIONS["NOTIFY_TAXYING_ACTIVE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " taxying to active."))

	def addReadyForDepartureMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report ready for departure", ACTIONS["NOTIFY_READY_FOR_DEPARTURE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " ready for departure."))

	def addHoldingOnGroundMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report holding position", ACTIONS["NOTIFY_HOLDING_ON_GROUND"], "Roger holding position " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + "."))

	def addTakingOffMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report taking off", ACTIONS["NOTIFY_TAKING_OFF"], "Roger taking off " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + "."))

	def addLiningUpAndTakingOffMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report lining up and taking off", ACTIONS["NOTIFY_LINING_UP_TAKING_OFF"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " lining up and taking off."))

	def addLeavingCircuitNorthMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report leaving circuit to the north", ACTIONS["NOTIFY_LEAVING_CIRCUIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " leaving circuit to the north."))

	def addLeavingCircuitSouthMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report leaving circuit to the south", ACTIONS["NOTIFY_LEAVING_CIRCUIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " leaving circuit to the south."))

	def addLeavingCircuitEastMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report leaving circuit to the east", ACTIONS["NOTIFY_LEAVING_CIRCUIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " leaving circuit to the east."))

	def addLeavingCircuitWestMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report leaving circuit to the west", ACTIONS["NOTIFY_LEAVING_CIRCUIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " leaving circuit to the west."))

	def addDownwindMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report downwind", ACTIONS["NOTIFY_DOWNWIND"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " downwind."))

	def addFinalMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report established on final", ACTIONS["NOTIFY_FINAL"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " on final."))

	def addGoAroundMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report going around", ACTIONS["NOTIFY_GOING_AROUND"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " going around."))

	def addClearActiveMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report clear active", ACTIONS["NOTIFY_CLEAR_ACTIVE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " clear active, taxying to parking."))

	def addInitialAirborneContactMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Make initial contact", ACTIONS["INITIAL_CONTACT_AIRBORNE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " this is " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + "."))

	def addAirborneRequestInfoMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Request airfield information", ACTIONS["REQUEST_INFO_AIRBORNE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["LOCATION_RELATIVE_TO_AIRFIELD"] + " of the airfield, request airfield information."))

	def addAirborneTransitMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("State intention to transit ATZ", ACTIONS["NOTIFY_INTENTION_TRANSIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " is a " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRCRAFT_TYPE"] + " from " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["ORIGINATING_AIRPORT"] + " to " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["DESTINATION_AIRPORT"] + " position " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["LOCATION_RELATIVE_TO_AIRFIELD"] + ", heading " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["HEADING"] + " degrees, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["ALTITUDE_FEET"] + " feet on QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRCRAFT_QNH"] + ", request traffic information."))

	def addReadbackInfoAirborneMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Readback", ACTIONS["READBACK_INFO_AIRBORNE"], "Roger, runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand, QFE " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QFE"] + ", " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + "."))

	def addOverheadDescendingDeadsideMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report overhead, descending deadside", ACTIONS["NOTIFY_OVERHEAD_DESCENDING_DEADSIDE"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " overhead, descending deadside for runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + "."))

	def addReadbackInfoTransitMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Readback", ACTIONS["READBACK_INFO_TRANSIT"], "Roger, QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"] + ", I will report overhead, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + "."))

	def addReportOverheadMenuItem(self, menu):
		menu.append(MenuItem.MenuItem("Report overhead", ACTIONS["NOTIFY_OVERHEAD_TRANSIT"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " overhead at " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["ALTITUDE_FEET"] + " feet, will report when leaving frequency."))

	def addReportLeavingATZ(self, menu):
		menu.append(MenuItem.MenuItem("Report leaving ATZ", ACTIONS["NOTIFY_LEAVING_ATZ"], CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " now clear of your ATZ, changing to en-route frequency, good day."))

	def work(self):
		ATC.ATC.work(self)


	def handleClearRadioTransmission(self, sender, data):
		""" Handle a properly received incoming radio transmission """
		# Call superclass
		ATC.ATC.handleClearRadioTransmission(self, sender, data)

		aircraftATCState = self.getAircraftATCState(sender)

		if (data.actions[0] == ACTIONS["REQUEST_INFO_GROUND"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " readability 5, runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand circuit, QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"], [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(ATC.COMMUNICATION_STATES["INITIAL_CONTACT"])

		elif (data.actions[0] == ACTIONS["READBACK_INFO_GROUND"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["READBACK_INFO_GROUND"])

		elif (data.actions[0] == ACTIONS["NOTIFY_TAXYING_ACTIVE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TAXYING_ACTIVE"])

		elif (data.actions[0] == ACTIONS["NOTIFY_READY_FOR_DEPARTURE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"] + ", surface wind " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_DIRECTION"] + " degrees " +CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_SPEED"] + " knots", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_READY_FOR_DEPARTURE"])

		elif (data.actions[0] == ACTIONS["NOTIFY_HOLDING_ON_GROUND"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_HOLDING_ON_GROUND"])

		elif (data.actions[0] == ACTIONS["NOTIFY_LINING_UP_TAKING_OFF"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"] + ", surface wind " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_DIRECTION"] + " degrees " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_SPEED"] + " knots", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TAKING_OFF"])

		elif (data.actions[0] == ACTIONS["NOTIFY_TAKING_OFF"]):
			# No reply
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TAKING_OFF"])

		elif (data.actions[0] == ACTIONS["NOTIFY_DOWNWIND"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_DOWNWIND"])

		elif (data.actions[0] == ACTIONS["NOTIFY_FINAL"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"] + ", surface wind " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_DIRECTION"] + " degrees " +CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_WIND_SPEED"] + " knots", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_FINAL"])

		elif (data.actions[0] == ACTIONS["NOTIFY_GOING_AROUND"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TAKING_OFF"])

		elif (data.actions[0] == ACTIONS["NOTIFY_CLEAR_ACTIVE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(ATC.COMMUNICATION_STATES["NO_CONTACT"])

		elif (data.actions[0] == ACTIONS["NOTIFY_LEAVING_CIRCUIT"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(ATC.COMMUNICATION_STATES["NO_CONTACT"])

		elif (data.actions[0] == ACTIONS["INITIAL_CONTACT_AIRBORNE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " pass your message", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(ATC.COMMUNICATION_STATES["INITIAL_CONTACT"])

		elif (data.actions[0] == ACTIONS["NOTIFY_INTENTION_TRANSIT"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " roger, runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " is active " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_NAME"] + " QNH " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QNH"] + ", " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"], [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TRANSIT"])

		elif (data.actions[0] == ACTIONS["REQUEST_INFO_AIRBORNE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " runway " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["VFR_RUNWAY"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["CIRCUIT_DIRECTION"] + " hand, QFE " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_QFE"] + ". " +CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"], [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["RECEIVED_INFO_AIRBORNE"])

		elif (data.actions[0] == ACTIONS["READBACK_INFO_AIRBORNE"]):
			# No reply
			aircraftATCState.setState(COMMUNICATION_STATES["READBACK_INFO_AIRBORNE"])

		elif (data.actions[0] == ACTIONS["NOTIFY_OVERHEAD_DESCENDING_DEADSIDE"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " roger, " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["AIRFIELD_TRAFFIC"], [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_TAKING_OFF"])

		elif (data.actions[0] == ACTIONS["READBACK_INFO_TRANSIT"]):
			# No reply
			aircraftATCState.setState(COMMUNICATION_STATES["READBACK_INFO_TRANSIT"])

		elif (data.actions[0] == ACTIONS["NOTIFY_OVERHEAD_TRANSIT"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " roger", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(COMMUNICATION_STATES["NOTIFIED_OVERHEAD_TRANSIT"])

		elif (data.actions[0] == ACTIONS["NOTIFY_LEAVING_ATZ"]):
			self.queueTransmission(CommunicationConstants.RADIO_MESSAGE_PARAMETERS["RECIPIENTCALLSIGN"] + " " + CommunicationConstants.RADIO_MESSAGE_PARAMETERS["SENDERCALLSIGN"] + " roger, good day", [ATC.ACTIONS["ACKNOWLEDGED"]], sender)
			aircraftATCState.setState(ATC.COMMUNICATION_STATES["NO_CONTACT"])



	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this ATC """
		# Call superclass method
		ATC.ATC.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
