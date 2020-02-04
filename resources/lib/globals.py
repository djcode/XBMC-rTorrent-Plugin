''' Globals to be used throughout the app '''
import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import resources.lib.xmlrpc2scgi as xmlrpc2scgi

# Addon constants
__plugin__ = "RTorrent"
__addonID__ = "plugin.program.rtorrent"
__author__ = "Daniel Jolly"
__url__ = "http://www.danieljolly.com"
__credits__ = "See README"
__version__ = "1.16.1"
__date__ = "04/01/2016"

# Set a variable for Addon info and language strings
__addon__ = xbmcaddon.Addon(__addonID__)
__setting__ = __addon__.getSetting
__lang__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path')

# Set plugin fanart
xbmcplugin.setPluginFanart(int(sys.argv[1]), os.path.join(__cwd__, 'fanart.jpg'))

# Connection constants
# Check to see if addon is set to socket or port mode
if int(__setting__('use_socket')) == 1:
    __connection__ = 'scgi://{}'.format(__setting__('domain_socket'))
else:
    __connection__ = 'scgi://{}:{}'.format(__setting__('scgi_server'), __setting__('scgi_port'))

RTC_TEST = xmlrpc2scgi.RTorrentXMLRPCClient(__connection__)

def connection_ok():
    '''Check to see if we can connect to rTorrent. If not ask to open Settings page.'''
    # establishing connection
    try:
        RTC_TEST.system.client_version()
    except:
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno(__lang__(30155), __lang__(30156), __lang__(30157))
        if ret is True:
            __addon__.openSettings()
            connection_ok()
        else:
            sys.exit()
    else:
        return RTC_TEST


RTC = connection_ok()

# Directory containing status icons for torrents
__icondir__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'icons'))

# Try to work out if the copy of rTorrent we're connecting to is running on the same machine.
if __setting__('use_socket') == '0':
    LOCAL_NAMES = ['localhost', '127.0.0.1', os.getenv('COMPUTERNAME')]
    if __setting__('scgi_server') in LOCAL_NAMES:
        __islocal__ = 1
    else:
        __islocal__ = 0
else:
    __islocal__ = 1
