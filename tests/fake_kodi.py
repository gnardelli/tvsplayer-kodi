# -*- coding: utf-8 -*-
"""Minimal stand-ins for Kodi's Python modules, so the add-on can be tested outside Kodi.

Dialog answers are taken from ANSWERS (a list filled by the test); every call is logged in LOG.
"""
import os
import sys
import types

LOG = []          # (what, details)
ANSWERS = []      # queued dialog answers, consumed in order
DIRECTORY = []    # items of the last listing: (url, label, label2, is_folder, props, context_menu)
RESOLVED = []     # setResolvedUrl calls: (succeeded, path)
SETTINGS = {"probe_links": "true", "probe_timeout": "3", "radio_limit": "60", "first_run_done": "false"}
PROFILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_profile")
ADDON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin.video.tvsplayer")


def _answer(kind):
    if not ANSWERS:
        raise AssertionError("no answer queued for dialog %s" % kind)
    value = ANSWERS.pop(0)
    LOG.append((kind, value))
    return value


def _strings():
    """Reads strings.po so labels in the test look like in Kodi."""
    path = os.path.join(ADDON_DIR, "resources", "language", "resource.language.en_gb", "strings.po")
    result, ctx = {}, None
    for line in open(path, encoding="utf-8"):
        if line.startswith('msgctxt "#'):
            ctx = int(line.split("#")[1].split('"')[0])
        elif line.startswith("msgid ") and ctx is not None:
            result[ctx] = line[7:-2].replace('\\"', '"')
            ctx = None
    return result


STRINGS = _strings()

# ── xbmc ─────────────────────────────────────────────────────────────────
xbmc = types.ModuleType("xbmc")
xbmc.ISO_639_1 = 0
xbmc.getLanguage = lambda fmt=None: "it"
xbmc.translatePath = lambda p: p
xbmc.executebuiltin = lambda cmd: LOG.append(("builtin", cmd))


class _Player(object):
    def play(self, url, item=None):
        LOG.append(("player.play", url))


xbmc.Player = _Player

# ── xbmcaddon ────────────────────────────────────────────────────────────
xbmcaddon = types.ModuleType("xbmcaddon")


class _Addon(object):
    def getAddonInfo(self, key):
        return {"name": "TVS Player", "icon": "icon.png", "fanart": "fanart.jpg", "profile": PROFILE}[key]

    def getLocalizedString(self, sid):
        return STRINGS.get(sid, "#%d" % sid)

    def getSetting(self, key):
        return SETTINGS.get(key, "")

    def getSettingBool(self, key):
        return SETTINGS.get(key) == "true"

    def getSettingInt(self, key):
        return int(SETTINGS.get(key, "0"))

    def setSetting(self, key, value):
        SETTINGS[key] = value


xbmcaddon.Addon = _Addon

# ── xbmcvfs ──────────────────────────────────────────────────────────────
xbmcvfs = types.ModuleType("xbmcvfs")
xbmcvfs.translatePath = lambda p: p


class _File(object):
    def __init__(self, path):
        self.f = open(path, "rb")

    def read(self):
        return self.f.read().decode("utf-8")

    def close(self):
        self.f.close()


xbmcvfs.File = _File

# ── xbmcgui ──────────────────────────────────────────────────────────────
xbmcgui = types.ModuleType("xbmcgui")
xbmcgui.NOTIFICATION_ERROR = "error"


class _InfoTag(object):
    def __getattr__(self, name):
        return lambda *a, **k: None


class ListItem(object):
    def __init__(self, label="", label2="", path=""):
        self.label, self.label2, self.path = label, label2, path
        self.props, self.menu, self.art = {}, [], {}

    def setArt(self, art):
        self.art = art

    def setProperty(self, k, v):
        self.props[k] = v

    def addContextMenuItems(self, items):
        self.menu = items

    def getVideoInfoTag(self):
        return _InfoTag()

    def getMusicInfoTag(self):
        return _InfoTag()


class Dialog(object):
    def yesno(self, heading, message, *a, **k):
        return _answer("yesno")

    def ok(self, heading, message):
        LOG.append(("ok", heading + " | " + message))
        return True

    def input(self, heading, default="", *a, **k):
        return _answer("input")

    def select(self, heading, items, *a, **k):
        LOG.append(("select-items", items[:5]))
        return _answer("select")

    def browseSingle(self, *a, **k):
        return _answer("browse")

    def notification(self, heading, message, icon=None, time=0):
        LOG.append(("notify", message))


class DialogProgressBG(object):
    def create(self, *a):
        pass

    def close(self):
        pass


xbmcgui.ListItem = ListItem
xbmcgui.Dialog = Dialog
xbmcgui.DialogProgressBG = DialogProgressBG

# ── xbmcplugin ───────────────────────────────────────────────────────────
xbmcplugin = types.ModuleType("xbmcplugin")
xbmcplugin.SORT_METHOD_UNSORTED = 0
xbmcplugin.SORT_METHOD_LABEL = 1
xbmcplugin.addDirectoryItem = lambda h, url, item, isFolder=False: DIRECTORY.append(
    (url, item.label, item.label2, isFolder, item.props, item.menu))
xbmcplugin.endOfDirectory = lambda h, succeeded=True, updateListing=False, cacheToDisc=True: LOG.append(
    ("end", succeeded))
xbmcplugin.setContent = lambda h, c: None
xbmcplugin.addSortMethod = lambda h, m: None
xbmcplugin.setResolvedUrl = lambda h, ok, item: RESOLVED.append((ok, item.path))

for module in (xbmc, xbmcaddon, xbmcvfs, xbmcgui, xbmcplugin):
    sys.modules[module.__name__] = module
