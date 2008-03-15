#
#  UIManager.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

import time

from XPLMDataAccess import *
from XPLMGraphics import *
from XPWidgetDefs import *
from XPWidgets import *
from XPStandardWidgets import *
from XPLMProcessing import *
from XPLMDisplay import *
from XPLMUtilities import *

from XATC.managers import CommunicationManager
from XATC.communication import Frequency
from XATC.communication import Message
from XATC.data import RadioMessageData

# Pronunciation mappings, applied in strict order as defined
PRONUNCIATION_MAPPINGS = [["[[]*[]]", ""], ["([0-9])[.]([0-9])", "$1 decimal $2"], ["\\b1/4\\b", "one fourth"], ["\\b2/4\\b", "two fourths"], ["\\b3/4\\b", "tree fourths"], ["\\b4/4\\b", "four fourths"], ["\\b0\\b", "zero"], ["\\b3\\b", "tree"], ["\\b5\\b", "fife"], ["\\b9\\b", "niner"], ["\\bthree\\b", "tree"], ["\\bfive\\b", "fife"], ["\\bnine\\b", "niner"], ["\\bC\\b", "celsius"], ["\\bF\\b", "fahrenheit"], ["\\bmb\\b", "millibars"], ["\\bL\\b", "left"], ["\\bR\\b", "right"], ["\\bkt\\b", "knots"], ["\\bkm\\b", "kilometers"], ["\\bILS\\b", "I L S"], ["\\bQFE\\b", "Q F E"], ["\\bQNH\\b", "Q N H"], ["\\bVFR\\b", "V F R"], ["\\breadback\\b", "reedback"]]

# Datarefs
DATAREF_TEXTATC = XPLMFindDataRef("sim/operation/prefs/text_out")
DATAREF_VIEWTYPE = XPLMFindDataRef("sim/graphics/view/view_type")

# The number of characters in the scrolling area
SCROLLING_AREA_CHARACTER_COUNT = 80
# The window border in pixels
WINDOW_BORDER = 5
# The line spacing in pixels
LINE_SPACING = 5
# Fetch character width and line height
_w = []; _h = []; XPLMGetFontDimensions(xplmFont_Basic, _w, _h, None)
# Character width
CHAR_WIDTH = _w[0]
# Line height
LINE_HEIGHT = _h[0]
# The title bar height
TITLEBAR_HEIGHT = LINE_HEIGHT + 2 * WINDOW_BORDER

# A user property inside menu button widgets used to identify the button
WIDGET_PROPERTY_MENUITEMID = xpProperty_UserStart

# Number of milliseconds per gross scroll tick (character)
MS_PER_SCROLL_TICK = 80.0
# Pixels per millisecond for smooth scrolling
PIXELS_PER_MS = CHAR_WIDTH / MS_PER_SCROLL_TICK

# FlightLoop callback frequency (1/100 second)
FLIGHTLOOP_CALLBACK_FREQUENCY = 0.01


class UIManager:
	""" Handles all interaction with the user """
	
	def __init__(self, XATC):
		""" Constructor """
		# Parent plugin
		self.XATC = XATC

		# The previous state of the text ATC setting
		self.savedTextATCDataRefSetting = XPLMGetDatai(DATAREF_TEXTATC)
		# Switch off normal drawing of text ATC
		XPLMSetDatai(DATAREF_TEXTATC, 0)
		# Set up the scrolling buffer
		self.scrollingMessageBuffer = " " * SCROLLING_AREA_CHARACTER_COUNT
		# The currently active menu
		self.currentMenu = []
		# The currently selected menu item
		self.currentMenuItem = 1
		# The currently active message
		self.currentMessage = ""
		# The pending items to be spoken
		self.currentSpokenString = None
		# The last scroll tick time
		self.lastScrollTime = -1
		# The current pixel offset of the scrolling text, for smooth scrolling
		self.currentPixelScrollPos = CHAR_WIDTH

		# The main window Rectangle
		self.mainWindowRect = {"x": 100, "y": 400, "width": WINDOW_BORDER * 2 + SCROLLING_AREA_CHARACTER_COUNT * CHAR_WIDTH, "height": WINDOW_BORDER + LINE_HEIGHT * 20 + TITLEBAR_HEIGHT}
		# The frequency window Rectangle
		self.frequencyWindowRect = {"x": 700, "y": 400, "width": WINDOW_BORDER * 2 + 200, "height": WINDOW_BORDER + LINE_HEIGHT * 20 + TITLEBAR_HEIGHT}
		# The scrolling message buffer Rectangle
		self.scrollingMessageFieldRect = {"x": self.mainWindowRect["x"] + WINDOW_BORDER, "y": self.mainWindowRect["y"] - TITLEBAR_HEIGHT, "width": SCROLLING_AREA_CHARACTER_COUNT * CHAR_WIDTH, "height": LINE_HEIGHT}

		# Set up the main window
		self.mainWindow = XPCreateWidget(self.mainWindowRect["x"], self.mainWindowRect["y"], self.mainWindowRect["x"] + self.mainWindowRect["width"], self.mainWindowRect["y"] - self.mainWindowRect["height"], 1, "XATC", 1,	0, xpWidgetClass_MainWindow)
		XPSetWidgetProperty(self.mainWindow, xpProperty_MainWindowType, xpMainWindowStyle_Translucent)
		self.mainMenuButtonsCB = self.mainMenuButtonsCallback
		XPAddWidgetCallback(self.XATC, self.mainWindow, self.mainMenuButtonsCB)

		# Set up the frequency window
		self.frequencyWindow = XPCreateWidget(self.frequencyWindowRect["x"], self.frequencyWindowRect["y"], self.frequencyWindowRect["x"] + self.frequencyWindowRect["width"], self.frequencyWindowRect["y"] - self.frequencyWindowRect["height"], 1, "Available Frequencies", 1, 0, xpWidgetClass_MainWindow)
		XPSetWidgetProperty(self.frequencyWindow, xpProperty_MainWindowType, xpMainWindowStyle_Translucent)
		self.frequencyMenuButtonsCB = self.frequencyMenuButtonsCallback
		XPAddWidgetCallback(self.XATC, self.frequencyWindow, self.frequencyMenuButtonsCB)

		# Create a text field for the scrolling message
		self.messageTextField = XPCreateWidget(self.scrollingMessageFieldRect["x"], self.scrollingMessageFieldRect["y"], self.scrollingMessageFieldRect["x"] + self.scrollingMessageFieldRect["width"], self.scrollingMessageFieldRect["y"] - self.scrollingMessageFieldRect["height"], 1, "wibble wobble woo", 0, self.mainWindow, xpWidgetClass_TextField)
		XPSetWidgetProperty(self.messageTextField, xpProperty_TextFieldType, xpTextTranslucent)

		# Create a countainer for our main menu pushbuttons.  This allows us to just set one widget callback handler per button set rather than one for each button.
		#self.mainWindowButtonContainer = XPCreateWidget(self.mainWindowRect["x"], self.mainWindowRect["y"], self.mainWindowRect["x"] + self.mainWindowRect["width"], self.mainWindowRect["y"] - self.mainWindowRect["height"], 1,	"",	0, self.mainWindow, xpWidgetClass_SubWindow)
		#XPSetWidgetProperty(self.mainWindowButtonContainer, xpProperty_SubWindowType, xpSubWindowStyle_Screen)
		#self.mainMenuButtonsCB = self.mainMenuButtonsCallback
		#XPAddWidgetCallback(self.XATC, self.mainWindowButtonContainer, self.mainMenuButtonsCB)
		
		# Create a countainer for our frequency menu pushbuttons.  This allows us to just set one widget callback handler per button set rather than one for each button.
		#self.frequencyWindowButtonContainer = XPCreateWidget(self.frequencyWindowRect["x"], self.frequencyWindowRect["y"], self.frequencyWindowRect["x"] + self.frequencyWindowRect["width"], self.frequencyWindowRect["y"] - self.frequencyWindowRect["height"], 1,	"",	0, self.frequencyWindow, xpWidgetClass_SubWindow)
		#XPSetWidgetProperty(self.frequencyWindowButtonContainer, xpProperty_SubWindowType, xpSubWindowStyle_Screen)
		#self.frequencyMenuButtonsCB = self.frequencyMenuButtonsCallback
		#XPAddWidgetCallback(self.XATC, self.frequencyWindowButtonContainer, self.frequencyMenuButtonsCB)

		# Create an ArrayList of buttons for the menu items
		tempRect = {"x": self.mainWindowRect["x"] + WINDOW_BORDER, "y": self.mainWindowRect["y"] - TITLEBAR_HEIGHT - LINE_HEIGHT - LINE_SPACING, "width": SCROLLING_AREA_CHARACTER_COUNT * CHAR_WIDTH, "height": LINE_HEIGHT}
		
		self.mainMenuButtons = []

		for i in range(0, 18):
			self.mainMenuButtons.append(XPCreateWidget(tempRect["x"], tempRect["y"], tempRect["x"] + tempRect["width"], tempRect["y"] - tempRect["height"], 1, str(i), 0, self.mainWindow, xpWidgetClass_Button))
			# XPSetWidgetProperty(self.mainMenuButtons[-1], xpProperty_TextFieldType, xpTextTranslucent)
			XPSetWidgetProperty(self.mainMenuButtons[-1], xpProperty_ButtonType, xpPushButton)
			XPSetWidgetProperty(self.mainMenuButtons[-1], WIDGET_PROPERTY_MENUITEMID, i)
			tempRect["y"] = tempRect["y"] - LINE_HEIGHT - LINE_SPACING


		# Create an ArrayList of buttons for the frequencies
		tempRect = {"x": self.frequencyWindowRect["x"] + WINDOW_BORDER, "y": self.frequencyWindowRect["y"] - TITLEBAR_HEIGHT - LINE_SPACING, "width": self.frequencyWindowRect["width"] - 2 * WINDOW_BORDER, "height": LINE_HEIGHT}

		self.frequencyButtons = []

		for i in range(0, 18):
			self.frequencyButtons.append(XPCreateWidget(tempRect["x"], tempRect["y"], tempRect["x"] + tempRect["width"], tempRect["y"] - tempRect["height"], 1, str(i), 0, self.frequencyWindow, xpWidgetClass_Button))
			# XPSetWidgetProperty(self.frequencyButtons[-1], xpProperty_TextFieldType, xpTextTranslucent)
			XPSetWidgetProperty(self.frequencyButtons[-1], xpProperty_ButtonType, xpPushButton)
			XPSetWidgetProperty(self.frequencyButtons[-1], WIDGET_PROPERTY_MENUITEMID, i)
			tempRect["y"] = tempRect["y"] - LINE_HEIGHT - LINE_SPACING

		# Show the windows
		XPShowWidget(self.mainWindow)
		XPShowWidget(self.frequencyWindow)

		# Register our flight loop callback
		self.flightLoopCB = self.flightLoopCallback
		XPLMRegisterFlightLoopCallback(self.XATC, self.flightLoopCB, FLIGHTLOOP_CALLBACK_FREQUENCY, 0)
		

	def __del__(self):
		""" Destructor """
		XPHideWidget(self.mainWindow)
		XPDestroyWidget(self, self.mainWindow, 1)
		XPHideWidget(self.frequencyWindow)
		XPDestroyWidget(self, self.frequencyWindow, 1)
		XPLMSetDatai(DATAREF_TEXTATC, self.savedTextATCDataRefSetting)

	
	def flightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):
		""" Flight loop callback """
		self.work()
		return FLIGHTLOOP_CALLBACK_FREQUENCY


	def mainMenuButtonsCallback(self, message, widget, param1, param2):
		""" Main menu text fields callback """
		if (message == xpMsg_PushButtonPressed):
			self.mainMenuItemChosen(XPGetWidgetProperty(param1, WIDGET_PROPERTY_MENUITEMID, 0))
			return 1
		else:
			return 0


	def frequencyMenuButtonsCallback(self, message, widget, param1, param2):
		""" Frequency menu text fields callback """
		if (message == xpMsg_PushButtonPressed):
			self.frequencyMenuItemChosen(XPGetWidgetProperty(param1, WIDGET_PROPERTY_MENUITEMID, 0))
			return 1
		else:
			return 0


	def work(self):
		""" Perform regular actions """
		# Speak if necessary
		if (self.currentSpokenString != None):
			XPLMSpeakString(self.currentSpokenString)
			self.currentSpokenString = None

		if (int(time.clock() * 1000) - self.lastScrollTime > MS_PER_SCROLL_TICK):
			# Move the coarse scroll along one character, reset smooth scroll position
			self.lastScrollTime = int(time.clock() * 1000)
			self.scrollingMessageBuffer = self.scrollingMessageBuffer[1:]
			if (len(self.scrollingMessageBuffer) < SCROLLING_AREA_CHARACTER_COUNT): self.scrollingMessageBuffer += ' '
			XPSetWidgetDescriptor(self.messageTextField, self.scrollingMessageBuffer[0:SCROLLING_AREA_CHARACTER_COUNT])

		# Update the smooth scrolling position
		self.currentPixelScrollPos = int(CHAR_WIDTH - ((int(time.clock() * 1000) - self.lastScrollTime) * PIXELS_PER_MS))
		self.refreshScrollingMessageWidgetRect()
		self.refreshMainWindowRect()
		self.scrollingMessageFieldRect["x"] = self.mainWindowRect["x"] + WINDOW_BORDER + self.currentPixelScrollPos
		self.scrollingMessageFieldRect["y"] = self.mainWindowRect["y"] - TITLEBAR_HEIGHT
		XPSetWidgetGeometry(self.messageTextField, self.scrollingMessageFieldRect["x"], self.scrollingMessageFieldRect["y"], self.scrollingMessageFieldRect["x"] + self.scrollingMessageFieldRect["width"], self.scrollingMessageFieldRect["y"] - self.scrollingMessageFieldRect["height"])


	def getID(self):
		""" MessageHandler required method """
		return "UI Manager"


	def showMenu(self, menu):
		""" Display a menu to the user """
		self.currentMenu = menu
		self.currentMenuItem = 1
		self.refreshMainWindowRect()

		# Recalculate window size
		if (self.currentMenu == None): newHeight = TITLEBAR_HEIGHT + LINE_HEIGHT + LINE_SPACING + WINDOW_BORDER;
		else: newHeight = TITLEBAR_HEIGHT + LINE_HEIGHT + LINE_SPACING + (len(self.currentMenu) * (LINE_HEIGHT + LINE_SPACING)) + WINDOW_BORDER
		self.mainWindowRect["height"] = newHeight
		XPSetWidgetGeometry(self.mainWindow, self.mainWindowRect["x"], self.mainWindowRect["y"], self.mainWindowRect["x"] + self.mainWindowRect["width"], self.mainWindowRect["y"] - self.mainWindowRect["height"])

		if (self.XATC.userAircraft.currentATC == None): XPSetWidgetDescriptor(self.mainWindow, Frequency.formatFrequency(self.XATC.userAircraft.currentFrequency) + ": Air to Air")
		else: XPSetWidgetDescriptor(self.mainWindow, Frequency.formatFrequency(self.XATC.userAircraft.currentFrequency) + ' ' + self.XATC.userAircraft.currentATC.name)

		# Set up and position the menu fields
		# Create an ArrayList of text fields for the frequencies
		tempRect = {"x": self.mainWindowRect["x"] + WINDOW_BORDER, "y": self.mainWindowRect["y"] - TITLEBAR_HEIGHT - LINE_HEIGHT * 2 - LINE_SPACING, "width": SCROLLING_AREA_CHARACTER_COUNT * CHAR_WIDTH, "height": LINE_HEIGHT}

		for i in range(0, 18):
			textField = self.mainMenuButtons[i]
			XPSetWidgetGeometry(textField, tempRect["x"], tempRect["y"], tempRect["x"] + tempRect["width"], tempRect["y"] - tempRect["height"])

			if (self.currentMenu != None and i < len(self.currentMenu)):
				XPSetWidgetDescriptor(textField, str(i + 1) + ". " + self.currentMenu[i].menuText)
				XPShowWidget(textField)
			else:
				XPHideWidget(textField)

			tempRect["y"] -= LINE_HEIGHT + LINE_SPACING


		self.updateFrequencyWindow()


	def updateFrequencyWindow(self):
		""" Update the buttons in the frequency window """
		self.refreshFrequencyWindowRect()
		frequencies = self.XATC.communicationManager.getCurrentFrequencies()
		
		for i in range(0, 18):
			textField = self.frequencyButtons[i]
			
			if (i < len(frequencies)):
				frequency = frequencies[i]
				atc = self.XATC.communicationManager.getATC(frequency.frequencyStr)
				if (atc == None):
					XPSetWidgetDescriptor(textField, Frequency.formatFrequency(frequency.frequencyStr) + ": Air to Air")
				else:
					XPSetWidgetDescriptor(textField, Frequency.formatFrequency(frequency.frequencyStr) + ": " + atc.name)

				XPShowWidget(textField)

			else:
				XPHideWidget(textField)
				
				
	def displayMessageToUser(self, message):
		""" Add a String to the currently scrolling buffer """
		# Add the text with some space between messages
		self.scrollingMessageBuffer += message.data.text + "   "
		# Only speak messages that don't originate from the user (this may one day be a preference, or OMG perhaps a different voice?!!)
		if (message.sender != self.XATC.userAircraft): self.currentSpokenString = self.convertToSpoken(message.data.text)
		
		
	def convertToSpoken(self, string):
		""" Apply pronunciation mappings to a string """
		for mapping in PRONUNCIATION_MAPPINGS:
			string.replace(mapping[0], mapping[1])

		return string


	def stopSpeaking(self):
		""" Stop any current speaking by speaking an empty string """
		self.currentSpokenString = ""


	def handleMessage(self, message):
		""" Message handler """
		
		if (message.type == Message.TYPES["HOT_KEY_CALLBACK"]):
			vKey = message.data.charValue()
			if (vKey == XPLM_VK_1): self.mainMenuItemChosen(0)
			elif (vKey == XPLM_VK_2): self.mainMenuItemChosen(1)
			elif (vKey == XPLM_VK_3): self.mainMenuItemChosen(2)
			elif (vKey == XPLM_VK_4): self.mainMenuItemChosen(3)
			elif (vKey == XPLM_VK_5): self.mainMenuItemChosen(4)
			elif (vKey == XPLM_VK_6): self.mainMenuItemChosen(5)
			elif (vKey == XPLM_VK_7): self.mainMenuItemChosen(6)
			elif (vKey == XPLM_VK_8): self.mainMenuItemChosen(7)
			elif (vKey == XPLM_VK_9): self.mainMenuItemChosen(8)


	def mainMenuItemChosen(self, menuItemNo):
		""" Called when the user makes a selection from the main menu """
		if (menuItemNo < len(self.currentMenu)):
			menuItem = self.currentMenu[menuItemNo]
			data = RadioMessageData.RadioMessageData([menuItem.action], menuItem.spokenText)
			# Send the message. This assumes that we are sending it to the current ATC. If air to air is ever implemented, we need to alter the recipient accordingly
			self.XATC.communicationManager.transmit(self.XATC.userAircraft, self.XATC.userAircraft.currentFrequency, Message.Message(Message.TYPES["INCOMING_RADIO_TRANSMISSION_STARTED"], self.XATC.userAircraft, self.XATC.userAircraft.currentATC, data))


	def frequencyMenuItemChosen(self, menuItemNo):
		""" Called when the user makes a selection from the frequency menu """
		frequencies = self.XATC.communicationManager.getCurrentFrequencies()

		if (menuItemNo < len(frequencies)):
			frequency = frequencies[menuItemNo]
			self.XATC.userAircraft.changeFrequency(frequency.frequencyStr)


	def refreshMainWindowRect(self):
		""" Fetch the current main window coordinates and store them in the class properties """
		x = []; y = []; x2 = []; y2 = []
		XPGetWidgetGeometry(self.mainWindow, x, y, x2, y2)
		self.mainWindowRect["x"] = x[0]
		self.mainWindowRect["y"] = y[0]
		self.mainWindowRect["width"] = x2[0] - x[0]
		self.mainWindowRect["height"] = y[0] - y2[0]


	def refreshFrequencyWindowRect(self):
		""" Fetch the current frequency window coordinates and store them in the class properties """
		x = []; y = []; x2 = []; y2 = []
		XPGetWidgetGeometry(self.frequencyWindow, x, y, x2, y2)
		self.frequencyWindowRect["x"] = x[0]
		self.frequencyWindowRect["y"] = y[0]
		self.frequencyWindowRect["width"] = x2[0] - x[0]
		self.frequencyWindowRect["height"] = y[0] - y2[0]


	def refreshScrollingMessageWidgetRect(self):
		""" Fetch the current scrolling widget coordinates and store them in the class properties """
		x = []; y = []; x2 = []; y2 = []
		XPGetWidgetGeometry(self.messageTextField, x, y, x2, y2) 
		self.scrollingMessageFieldRect["x"] = x[0]
		self.scrollingMessageFieldRect["y"] = y[0]
		self.scrollingMessageFieldRect["width"] = x2[0] - x[0]
		self.scrollingMessageFieldRect["height"] = y[0] - y2[0]
