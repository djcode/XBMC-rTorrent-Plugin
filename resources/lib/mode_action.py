'''Application to send "actions" back to rTorrent'''
import xbmc
import xbmcgui
import resources.lib.globals as g

def main(method, arg1, arg2, arg3):
    ''' Send action to rTorrent '''
    allok = 0
    if method.find('erase') != -1:
        dialog = xbmcgui.Dialog()
        ret = dialog.yesno(g.__lang__(30153), g.__lang__(30154))
        if ret is True:
            allok = 1
    else:
        allok = 1
    if allok == 1:
        if arg3:
            # only used at this stage to change priority on files in torrent
            function = 'g.rtc.' + method + '("' + arg1 + '",' + arg2 + ',' + arg3 + ')'
        elif arg2:
            function = 'g.rtc.' + method + '("' + arg1 + '","' + arg2 + '")'
        else:
            function = 'g.rtc.' + method + '("' + arg1 + '")'
        # print function
        exec function
        xbmc.executebuiltin('Container.Refresh')
