#
#  ControlledAirportZone.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XATC.zones import AirportZone
from XATC.atc import TowerATC, ApproachATC, DepartureATC, GroundATC, ClearanceDeliveryATC, ATISATC, ArrivalATISATC, DepartureATISATC

class ControlledAirportZone(AirportZone.AirportZone):
	""" A zone representing a controlled airport """
	 
	def __init__(self, id, name, towerFrequency, approachFreqency, departureFrequency, groundFrequency, clearanceDeliveryFrequency, arrivalAtisFrequency, departureAtisFrequency, XATC):
		""" Constructor """
		# Call superclass constructor
		AirportZone.AirportZone.__init__(self, id, name, XATC)
		
		# The tower atc
		if (towerFrequency != None): self.towerATC = TowerATC.TowerATC(self, name, towerFrequency, XATC)
		else: self.towerATC = None
		# The approach atc
		if (approachFreqency != None): self.approachATC = ApproachATC.ApproachATC(self, name, approachFreqency, XATC)
		else: self.approachATC = None
		# The departure atc
		if (departureFrequency != None): self.departureATC = DepartureATC.DepartureATC(self, name, departureFrequency, XATC)
		else: self.departureATC = None
		# The ground atc
		if (groundFrequency != None): self.groundATC = GroundATC.GroundATC(self, name, groundFrequency, XATC)
		else: self.groundATC = None
		# The clearance atc
		if (clearanceDeliveryFrequency != None): self.clearanceDeliveryATC = ClearanceDeliveryATC.ClearanceDeliveryATC(self, name, clearanceDeliveryFrequency, XATC)
		else: self.clearanceDeliveryATC = None

		# The ATIS atc (note: if there is a combined arrival / departure ATIS, this is stored in arrivalAtisATC
		self.arrivalAtisATC = None
		self.departureAtisATC = None

		if (departureAtisFrequency == None):
			if (arrivalAtisFrequency != None):
				# No departure ATIS, set up a general ATIS on the arrival frequency
				self.arrivalAtisATC = ATISATC.ATISATC(self, name, arrivalAtisFrequency, XATC)
		else:
			if (arrivalAtisFrequency != None):
				# Arrival and departure ATISs specified
				self.arrivalAtisATC = ArrivalATISATC.ArrivalATISATC(self, name, arrivalAtisFrequency, XATC)
				self.departureAtisATC = DepartureATISATC.DepartureATISATC(self, name, departureAtisFrequency, XATC)
			else:
				# Only departure ATIS specified (strictly an error condition), fudge by setting up general ATIS on departure frequency
				self.arrivalAtisATC = ATISATC.ATISATC(self, name, departureAtisFrequency, XATC)


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Call superclass method
		AirportZone.AirportZone.replaceParameters(self, message)
		# Nothing else to do here yet
		pass
