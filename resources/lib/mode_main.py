''' Main program code '''
import sys
import xbmcgui
import xbmcplugin
from . import functions as function
from . import globals as g

def main():
    ''' Main program code '''
    # addonMenu();
    dlds = []
    dlds = g.RTC.d.multicall('main', "d.get_name=", "d.get_hash=", "d.get_completed_chunks=",
                             "d.get_size_chunks=", "d.get_size_files=", "d.get_directory=",
                             "d.is_active=", "d.get_complete=", "d.get_priority=",
                             "d.is_multi_file=", "d.get_size_bytes=")
    dlds_len = len(dlds)

    for dld in dlds:
        dld_name = dld[0]
        dld_hash = dld[1]
        dld_completed_chunks = dld[2]
        dld_size_chunks = dld[3]
        dld_percent_complete = dld_completed_chunks * 100 / dld_size_chunks
        dld_size_files = dld[4]
        # dld_directory = dld[5]
        dld_is_active = dld[6]
        dld_complete = dld[7]
        dld_priority = dld[8]
        # dld_is_multi_file = dld[9]
        dld_size_bytes = int(dld[10])
        tbn = function.get_icon(dld_size_files, dld_is_active, dld_complete, dld_priority)

        if dld_is_active == 1:
            context_menu_action = g.__lang__(30101), "xbmc.runPlugin(%s?mode=action&method=d.stop&arg1=%s)" % (
                sys.argv[0], dld_hash)
        else:
            context_menu_action = g.__lang__(30100), "xbmc.runPlugin(%s?mode=action&method=d.start&arg1=%s)" % (
                sys.argv[0], dld_hash)
        if dld_percent_complete < 100:
            list_item_name = dld_name + ' (' + str(dld_percent_complete) + '%)'
        else:
            list_item_name = dld_name

        context_menu = [context_menu_action,
                        (g.__lang__(30102), "xbmc.runPlugin(%s?mode=action&method=d.erase&arg1=%s)" % (sys.argv[0], dld_hash)),
                        (g.__lang__(30120),
                         "xbmc.runPlugin(%s?mode=action&method=d.set_priority&arg1=%s&arg2=3)" % (sys.argv[0], dld_hash)),
                        (g.__lang__(30121),
                         "xbmc.runPlugin(%s?mode=action&method=d.set_priority&arg1=%s&arg2=2)" % (sys.argv[0], dld_hash)),
                        (g.__lang__(30122),
                         "xbmc.runPlugin(%s?mode=action&method=d.set_priority&arg1=%s&arg2=1)" % (sys.argv[0], dld_hash)),
                        (g.__lang__(30123),
                         "xbmc.runPlugin(%s?mode=action&method=d.set_priority&arg1=%s&arg2=0)" % (sys.argv[0], dld_hash))]

        list_item = xbmcgui.ListItem(
            label=list_item_name,
            iconImage=tbn, thumbnailImage=tbn)
        list_item.addContextMenuItems(items=context_menu, replaceItems=True)
        list_item.setArt({'fanart': g.__addon__.getAddonInfo('fanart')})
        list_item.setInfo('video', {'title': list_item_name, 'size': dld_size_bytes})
        if dld_size_files > 1:
            if not xbmcplugin.addDirectoryItem(int(sys.argv[1]),
                                               sys.argv[0] + "?mode=files&hash=" + dld_hash +
                                               "&numfiles=" + str(dld_size_files),
                                               list_item, isFolder=True, totalItems=dlds_len):
                break
        else:
            if not xbmcplugin.addDirectoryItem(int(sys.argv[1]),
                                               sys.argv[0] + "?mode=play&arg1=0&hash=" + dld_hash,
                                               list_item, totalItems=dlds_len):
                break
    xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_SIZE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
