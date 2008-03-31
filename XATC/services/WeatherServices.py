#
#  WeatherServices.py
#  XATC
#
#  Created by Austin Goudge on 06/03/2008.
#  Copyright (c) 2008 Austin Goudge. All rights reserved.
#

import urllib2

from XATC.metar import Metar

# The METAR download URL
METAR_URL = "http://weather.noaa.gov/pub/data/observations/metar/stations/$$$$.TXT"


def getWeatherData(position):
	""" Get the weather data for a lat / long position """
	# Need to code this.  Should find the closest available
	return getWeatherData("")
	
	
def getWeatherData(ICAO):
	""" Get the weather data for a particular ICAO station """
	# Download the data
	try:
		sock = urllib2.urlopen(METAR_URL.replace("$$$$", ICAO))
		metarCodeLines = sock.readlines()
		sock.close()
		
		if (len(metarCodeLines) < 2): return None
		
		# Downloaded METAR has two lines, the first is the datestamp (which we can ignore because the date is also included in the METAR report)
		# the second line is the METAR report itself
		return Metar.Metar(metarCodeLines[1])
		
	except urllib2.URLError:
		print "Error loading Metar for " + ICAO
		return None
	
	except Metar.ParserError:
		print "Error parsing Metar for " + ICAO
		return None


def getHumanReadableMetar(metar):
	result = ""
	if metar == None: return result
	
	if metar.time: result += metar.time.ctime()
	if metar.wind_speed: result += ", wind " + metar.wind()
	if metar.vis: result += ", visibility " + metar.visibility()
	if metar.weather: result += ", " + metar.present_weather()
	if metar.sky: result += ", " + metar.sky_conditions(", ")
	if metar.temp: result += ", temperature " + metar.temp.string("C")
	if metar.press: result += ", pressure " + metar.press.string("mb")
	
	"""
			if self.dewpt:
					lines.append("dew point: %s" % self.dewpt.string("C"))
			if self.wind_speed_peak:
					lines.append("peak wind: %s" % self.peak_wind())
			if self.runway:
					lines.append("visual range: %s" % self.runway_visual_range())
			if self.press_sea_level:
					lines.append("sea-level pressure: %s" % self.press_sea_level.string("mb"))
			if self.max_temp_6hr:
					lines.append("6-hour max temp: %s" % str(self.max_temp_6hr))
			if self.max_temp_6hr:
					lines.append("6-hour min temp: %s" % str(self.min_temp_6hr))
			if self.max_temp_24hr:
					lines.append("24-hour max temp: %s" % str(self.max_temp_24hr))
			if self.max_temp_24hr:
					lines.append("24-hour min temp: %s" % str(self.min_temp_24hr))
			if self.precip_1hr:
					lines.append("1-hour precipitation: %s" % str(self.precip_1hr))
			if self.precip_3hr:
					lines.append("3-hour precipitation: %s" % str(self.precip_3hr))
			if self.precip_6hr:
					lines.append("6-hour precipitation: %s" % str(self.precip_6hr))
			if self.precip_24hr:
					lines.append("24-hour precipitation: %s" % str(self.precip_24hr))
	"""
	return result
