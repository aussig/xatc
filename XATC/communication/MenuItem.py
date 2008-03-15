#
#  MenuItem.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

class MenuItem:
	""" Encapsulates information about a menu item """

	def __init__(self, menuText, action, spokenText):
		""" Constructor """
		# The text as presented in the menu
		self.menuText = menuText
		# The action code associated with this menu item
		self.action = action
		# The text spoken if the menu item is selected
		self.spokenText = spokenText
