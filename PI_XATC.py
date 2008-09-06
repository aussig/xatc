#
#  PI_XATC.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

from XPLMDisplay import *
from XPLMProcessing import *

from XATC.managers import CommunicationManager
from XATC.managers import ZoneManager
from XATC.managers import UIManager
from XATC.aircraft import UserAircraft


class PythonInterface:
	""" Implements an Air Traffic Control plugin """
	
	def XPluginStart(self):
		# First we must fill in the passed in buffers to describe our plugin to the plugin-system.
		self.Name = "XATC"
		self.Sig =  "AustinGoudge.Python.XATC"
		self.Desc = "Air Traffic Control plugin."
		
		return self.Name, self.Sig, self.Desc
	
	
	def XPluginStop(self):
		""" Cleanup routine """
		pass
	
	
	def XPluginEnable(self):
		""" Specific processing when this plugin is enabled """
		# Initialise the communication manager, done first because ATCs depend on it
		self.communicationManager = CommunicationManager.CommunicationManager(self)
		# Initialise the current region
		self.zoneManager = ZoneManager.ZoneManager(self)
		# Initialise the UI manager
		self.uiManager = UIManager.UIManager(self)
		# Initialise the user aircraft, naturally the callsign must go here
		self.userAircraft = UserAircraft.UserAircraft("G-ASRG", self)
		
		# Register the user's aircraft with the communication manager
		self.communicationManager.registerAircraft(self.userAircraft)
		
		# TEMPORARY, JUST GET SOMETHING LOADED FOR TESTING
		self.zoneManager.loadUncontrolledAirport("EGCV", "Sleap", "12245");
		#self.zoneManager.loadCenter("EGTT", "London", "12150")
		#self.zoneManager.loadControlledAirport("EGAA", "Belfast Aldergrove", "11830", None, None, "12175", None, "12820", None)
		#self.zoneManager.loadControlledAirport("EGBB", "Birmingham", "11830", None, None, "12180", None, "12627", None)
		#self.zoneManager.loadControlledAirport("EGCC", "Manchester", "11862", None, None, "12185", "12170", "12817", "12197")
		#self.zoneManager.loadControlledAirport("EGGD", "Bristol", "13385", None, None, None, None, "12602", None)
		#self.zoneManager.loadControlledAirport("EGJJ", "Jersey", "11945", None, None, "12190", None, "11220", "12972")
		#self.zoneManager.loadControlledAirport("EGPF", "Glasgow", "11880", None, None, "12170", None, "12957", None)

		# Temporary, until zones are loaded
		# Update the frequency menu
		self.uiManager.showMenu(None)
		"""
			callbackManager.registerFlightLoopCallback(1f, zoneManager);
			callbackManager.registerHotKey(XPLM.VK_1, XPLM.DownFlag, "Menu item 1", uiManager);
			callbackManager.registerHotKey(XPLM.VK_2, XPLM.DownFlag, "Menu item 2", uiManager);
			callbackManager.registerHotKey(XPLM.VK_3, XPLM.DownFlag, "Menu item 3", uiManager);
			callbackManager.registerHotKey(XPLM.VK_4, XPLM.DownFlag, "Menu item 4", uiManager);
			callbackManager.registerHotKey(XPLM.VK_5, XPLM.DownFlag, "Menu item 5", uiManager);
			callbackManager.registerHotKey(XPLM.VK_6, XPLM.DownFlag, "Menu item 6", uiManager);
			callbackManager.registerHotKey(XPLM.VK_7, XPLM.DownFlag, "Menu item 7", uiManager);
			callbackManager.registerHotKey(XPLM.VK_8, XPLM.DownFlag, "Menu item 8", uiManager);
			callbackManager.registerHotKey(XPLM.VK_9, XPLM.DownFlag, "Menu item 9", uiManager);
			callbackManager.registerHotKey(XPLM.VK_0, XPLM.DownFlag, "Menu item 10", uiManager);
		"""
		return 1
					

	def XPluginDisable(self):
		""" We do not need to do anything when we are disabled, but we must provide the handler """
		pass
	
	
	def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
		""" We don't have to do anything in our receive message handler, but we must provide one """
		pass
