'''Assorted functions for the rTorrent plugin'''
import os
import sys
from . import globals as g

def get_params():
    '''Get parameters script (from Voinage's tutorial)'''
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in xrange(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

def get_icon(isdir, active, complete, priority):
    '''Get torrent or file status icon'''
    if isdir > 1:
        icon = "dir"
        priority += 3
    elif isdir == 0:
        icon = "file"
    else:
        icon = "file"
        priority += 3
    if active == 1:
        if complete == 1:
            iconcol = "9"
        else:
            switch = {
                # Files
                0: "0", # Don't Download
                1: "3", # Normal
                2: "4", # High
                # Downloads
                3: "1", # Idle
                4: "2", # Low
                5: "3", # Normal
                6: "4" # High
            }
            iconcol = switch.get(priority, "0")
    else:
        iconcol = "0"
    return os.path.join(g.__icondir__, icon + '_' + iconcol + '.jpg')

    # Colour scheme - NO LONGER USED
    # Dld & File Completed: Green
    # Dld & File P: High  : Yellow
    # Dld & File P: Normal: Blue
    # Dld P: Low   : Purple
    # Dld Priority: Idle  : Orange
    # Dld Stopped & File Don't Download: Red
