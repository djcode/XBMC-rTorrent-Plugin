# main imports
import urllib

PARAMS = get_params()

url = None
digest = None
mode = None
numfiles = None
method = None
arg1 = None
arg2 = None
arg3 = None
test = False

try:
    digest = str(PARAMS["digest"])
except:
    pass
try:
    mode = str(PARAMS["mode"])
except:
    pass
try:
    numfiles = int(PARAMS["numfiles"])
except:
    pass
try:
    method = str(urllib.unquote_plus(PARAMS["method"]))
except:
    pass
try:
    arg1 = str(urllib.unquote_plus(PARAMS["arg1"]))
except:
    pass
try:
    arg2 = str(urllib.unquote_plus(PARAMS["arg2"]))
except:
    pass
try:
    arg3 = str(urllib.unquote_plus(PARAMS["arg3"]))
except:
    pass

if mode is None:
    import resources.lib.mode_main as loader
    loader.main()
elif mode == 'files':
    import resources.lib.mode_files as loader
    loader.main(digest, numfiles)
elif mode == 'action':
    import resources.lib.mode_action as loader
    loader.main(method, arg1, arg2, arg3)
elif mode == 'play':
    import resources.lib.mode_play as loader
    loader.main(digest, arg1)
