#
#  ZoneManager.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.dataaccess import SceneryLoader

from XATC.zones import CenterZone
from XATC.zones import ControlledAirportZone
from XATC.zones import UncontrolledAirportZone


class ZoneManager:
	""" Handles loading and clearing zones as the user passes through them, loading is threaded to spread the load """

	def __init__(self, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC
		# The current center zones within user range
		self.centerZones = {}
		# The current airport zones within user range
		self.airportZones = {}
		# The object used to access scenery from disk
		self.sceneryLoader = SceneryLoader.SceneryLoader("C:/Program Files/X-System/")


	def handleMessage(message):
		""" Message handler """
		if (message.type == Message.TYPES["FLIGHT_LOOP_CALLBACK"]):
			# Create (load) zones as user comes in range, dispose of
			# out-of-range zones. This should be done on a thread

			# if (aCenterHasMovedInRange) loadIt();
			# if (anyCurrentCentersHaveMovedOutOfRange) disposeOfThem();

			# if (anAirportHasMovedInRange) loadIt();
			# if (anyCurrentAirportsHaveMovedOutOfRange) disposeOfThem();
			return None


	def getID(self):
		""" MessageHandler required method """
		return "Zone Manager"


	def loadCenter(self, id, name, frequency):
		""" Load a center zone """
		centerZone = CenterZone.CenterZone(id, name, frequency, self.XATC)
		self.centerZones[id] = centerZone


	def loadUncontrolledAirport(self, id, name, AGCSFrequency):
		""" Load an uncontrolled airport zone """
		airportZone = UncontrolledAirportZone.UncontrolledAirportZone(id, name, AGCSFrequency, self.XATC)
		self.airportZones[id] = airportZone


	def loadControlledAirport(self, id, name, towerFrequency, approachFreqency, departureFrequency, groundFrequency, clearanceDeliveryFrequency, arrivalAtisFrequency, departureAtisFrequency):
		""" Load a controlled airport zone """
		airportZone = ControlledAirportZone.ControlledAirportZone(id, name, towerFrequency, approachFreqency, departureFrequency, groundFrequency, clearanceDeliveryFrequency, arrivalAtisFrequency, departureAtisFrequency, self.XATC)
		self.airportZones[id] = airportZone
