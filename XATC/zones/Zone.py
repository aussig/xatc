#
#  Zone.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

class Zone:
	""" Superclass for all zones """

	def __init__(self, id, name, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC
		# The zone identifier
		self.id = id
		# The zone name
		self.name = name


	def __str__():
		""" Convenience toString method """
		return "Zone " + self.name


	def replaceParameters(self, message):
		""" Replace parameters in a Message object relevant to this zone """
		# Default method does nothing, implement in subclasses
		pass