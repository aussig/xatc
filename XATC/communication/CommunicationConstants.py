#
#  CommunicationConstants.py
#  XATC
#
#  Created by Austin Goudge on 10/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

# Alphanumeric IDs
ALPHANUMERIC_IDS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25, "0": 26, "1": 27, "2": 28, "3": 29, "4": 30, "5": 31, "6": 32, "7": 33, "8": 34, "9": 35}
ALPHANUMERIC_ID_MIN = 0
ALPHANUMERIC_ID_MAX = 35
ALPHA_ID_MIN = 0
ALPHA_ID_MAX = 25
NUMERIC_ID_MIN = 26
NUMERIC_ID_MAX = 35

# Alphanumeric Strings
ALPHANUMERIC_STRING = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa","quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "x-ray", "yankee", "zulu", "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
		
# The available mappable parameters in a radio message */
RADIO_MESSAGE_PARAMETERS = {"SENDERCALLSIGN": "%sen%", "RECIPIENTCALLSIGN": "%rec%", "FREQUENCY": "%freq%", "ALTITUDE_FEET": "%altfeet%", "VFR_RUNWAY": "%vfrrunway%", "VFR_LANDING_RUNWAY": "%vfrlandingrunway%", "VFR_DEPARTING_RUNWAY": "%vfrdepartingrunway%", "IFR_RUNWAY": "%ifrrunway%", "IFR_LANDING_RUNWAY": "%ifrlandingrunway%", "IFR_DEPARTING_RUNWAY": "%ifrdepartingrunway%", "CIRCUIT_DIRECTION": "%circdir%", "AIRFIELD_QNH": "%airfieldqnh%", "AIRFIELD_QFE": "%airfieldqfe%", "LOCATION_RELATIVE_TO_AIRFIELD": "%locrelairfield%", "AIRCRAFT_TYPE": "%aircrafttype%", "ORIGINATING_AIRPORT": "%origin%", "DESTINATION_AIRPORT": "%destination%", "AIRCRAFT_QNH": "%aircraftqnh%", "HEADING": "%hdng%", "AIRFIELD_TRAFFIC": "%airfieldtraffic%", "AIRFIELD_WIND_DIRECTION": "%airfieldwinddir%", "AIRFIELD_WIND_SPEED": "%airfieldwindspd%", "AIRFIELD_NAME": "%airfieldname%"}

# Null ID
NO_ID = "-----"

