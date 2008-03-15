#
#  SceneryLoader.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

class SceneryLoader:
	""" Manage the loading of scenery objects """

	def __init__(self, XPRootPath):
		""" Constructor """
		# The path to the root X-Plane folder
		self.XPRootPath = XPRootPath
		

	def loadAirport(self, airportID):
		""" Load an airport's data """
