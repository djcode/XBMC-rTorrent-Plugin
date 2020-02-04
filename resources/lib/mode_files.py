''' Working with files inside torrents '''
import sys
import xbmcgui
import xbmcplugin
from . import functions as function
from . import globals as g

def main(digest, numfiles):
    ''' Files inside a multi-file torrent code '''
    files = []
    files = g.RTC.f.multicall(digest, 1, "f.get_path=", "f.get_completed_chunks=",
                              "f.get_size_chunks=", "f.get_priority=", "f.get_size_bytes=")
    i = 0
    for t_f in files:
        f_name = t_f[0]
        f_completed_chunks = int(t_f[1])
        f_size_chunks = int(t_f[2])
        f_size_bytes = int(t_f[4])
        if f_size_chunks < 1:
            f_percent_complete = 100
        else:
            f_percent_complete = f_completed_chunks * 100 / f_size_chunks
        f_priority = t_f[3]
        if f_percent_complete == 100:
            f_complete = 1
        else:
            f_complete = 0
        tbn = function.get_icon(0, 1, f_complete, f_priority)
        if f_percent_complete < 100:
            list_item_name = f_name + ' (' + str(f_percent_complete) + '%)'
        else:
            list_item_name = f_name
        list_item = xbmcgui.ListItem(
            label=list_item_name,
            iconImage=tbn, thumbnailImage=tbn)
        context_menu = [(g.__lang__(30120),
                         "xbmc.runPlugin(%s?mode=action&method=f.set_priority&arg1=%s&arg2=%s&arg3=2)" % (sys.argv[0], digest, i)),
                        (g.__lang__(30121),
                         "xbmc.runPlugin(%s?mode=action&method=f.set_priority&arg1=%s&arg2=%s&arg3=1)" % (sys.argv[0], digest, i)),
                        (g.__lang__(30124),
                         "xbmc.runPlugin(%s?mode=action&method=f.set_priority&arg1=%s&arg2=%s&arg3=0)" % (sys.argv[0], digest, i))]
        list_item.addContextMenuItems(items=context_menu, replaceItems=True)
        list_item.setArt({'fanart': g.__addon__.getAddonInfo('fanart')})
        list_item.setInfo('video', {'title': list_item_name, 'size': f_size_bytes})
        if not xbmcplugin.addDirectoryItem(int(sys.argv[1]),
                                           "{}?mode=play&arg1={}&digest={}".format(sys.argv[0], str(i), digest),
                                           list_item, totalItems=numfiles):
            break
        i += 1
    xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_SIZE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
