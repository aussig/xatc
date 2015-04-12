# XATC #
This is a framework for a replacement for the X-Plane Air Traffic system. It was originally built in Java but the Java plugin for X-Plane became unsupported and is now defunct, so it was ported to Python.

## Currently Implemented ##
  1. ATC framework complete, with loading and initialisation of ATZs. Current implementation doesn't do any 'real world' loading of zones, i.e. there is no current map of real world ATZs,  some are just hard coded at startup for testing.
  1. Stub classes developed for all ATC controller stations.
  1. Full ATIS loop ATC implemented, gets latest METAR data from the Internet and parses it to produce correct ATIS for any ICAO code (it doesn't yet handle the case where no report is available, needs to get nearest available in that case).
  1. User interface implemented, menu system with scrolling ATC messages shown. Mouse click selection partially implemented.
  1. List of available frequencies window implemented, clicking on a frequency tunes current COM radio.
  1. Work complete on Air/Ground Communications Service ATC (UK 'Radio').  Probably need to do a US (CTAS) version of this, as well as any variants for other countries.

## To-do ##
Everything else!  For example:

  1. Implement the rest of the ATC classes (!)
  1. Work out a new format or use an existing format for specifying ATC zones and load the local zones for the position of the user aircraft.
  1. Expand the system for handling the local user area so ATZs are loaded and disposed of automatically as the user flies (coupled with previous item).
  1. Set the current X-Plane weather to match the closest METAR report (coupled with previous two items).
  1. Provide an option to get METAR from the metar file in the X-Plane folder.


## Dependencies ##
It is written in Python and is therefore dependant on Sandy Barbour's Python plugin, available here: http://www.xpluginsdk.org/python_interface_sdk200_downloads.htm.  Note that this is written using v2.01 of the Python Interface, which only works with X-Plane 9.00 and above.

## Checkout / Install ##
The source package consists of the top-level plugin file (PI\_XATC.py) and a folder containing all classes used by the plugin (XATC/).  Both these items must be placed inside a folder titled **PythonScripts** in your X-Plane plugins folder.  The only way to get the source at the moment is to use an SVN client.  [Here are instructions](http://code.google.com/p/xatc/source/checkout) for checking out a read-only copy.

## Developers ##
If you would like to contribute to the project, please contact me at: austin dot goudge at gmail dot com