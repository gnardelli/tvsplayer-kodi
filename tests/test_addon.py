# -*- coding: utf-8 -*-
"""End-to-end test of the add-on logic outside Kodi (fake Kodi modules + a local web server).

Run from the project root:  python kodi/tests/test_addon.py
Uses the internet only for the Radio Browser part (skip with --offline).
"""
import os
import shutil
import sys
import threading

try:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
except ImportError:  # pragma: no cover
    raise SystemExit("Python 3 required")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fake_kodi as K  # noqa: E402  (installs the fake xbmc* modules)

sys.path.insert(0, os.path.join(K.ADDON_DIR, "resources", "lib"))
from tvsplayer import m3u  # noqa: E402
from tvsplayer.plugin import run  # noqa: E402

OFFLINE = "--offline" in sys.argv
BASE = "plugin://plugin.video.tvsplayer/"

# ── local web server with a test playlist and a "working" stream ─────────
WWW = os.path.join(HERE, "_www")
PLAYLIST = u"""#EXTM3U
#EXTINF:-1 tvg-logo="http://logo/news.png" group-title="News",News One
http://127.0.0.1:9/dead.m3u8
#EXTINF:-1 group-title="News",News One
http://127.0.0.1:{port}/stream.m3u8
#EXTINF:-1 group-title="Sport",Sport, "Live" HD
#EXTVLCOPT:http-user-agent=MyAgent/1.0
http://127.0.0.1:{port}/sport.m3u8
#EXTINF:-1 radio="true" group-title="Music",Radio Rock
http://127.0.0.1:{port}/rock.mp3
#EXTINF:-1 group-title="Radio Italia",Radio Pop
http://127.0.0.1:{port}/pop.aac
http://127.0.0.1:{port}/plain-entry.m3u8
"""


class Quiet(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        SimpleHTTPRequestHandler.__init__(self, *a, directory=WWW, **k)

    def log_message(self, *a):
        pass


def start_server():
    server = HTTPServer(("127.0.0.1", 0), Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server.server_address[1]


def call(query=""):
    """Runs the add-on like Kodi does for a menu/action; returns the listed items."""
    del K.DIRECTORY[:]
    run([BASE, "1", "?" + query if query else ""])
    return list(K.DIRECTORY)


def labels(items):
    return [i[1] for i in items]


def check(condition, message):
    print(("  OK   " if condition else "  FAIL ") + message)
    if not condition:
        check.failed += 1


check.failed = 0


def main():
    for d in (K.PROFILE, WWW):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    port = start_server()
    with open(os.path.join(WWW, "list.m3u"), "w", encoding="utf-8") as f:
        f.write(PLAYLIST.format(port=port))
    for name in ("stream.m3u8", "sport.m3u8", "rock.mp3", "pop.aac", "plain-entry.m3u8"):
        open(os.path.join(WWW, name), "w").write("#EXTM3U\n")

    print("1. M3U parser")
    entries = m3u.parse(PLAYLIST.format(port=port), "Default")
    check(len(entries) == 6, "6 entries read")
    check(entries[2]["name"] == 'Sport, "Live" HD', "name with comma and quotes")
    check(entries[2]["url"].endswith("|User-Agent=MyAgent/1.0"), "#EXTVLCOPT user agent → Kodi header")
    check([e["type"] for e in entries] == ["tv", "tv", "tv", "radio", "radio", "tv"], "TV / radio detection")
    check(entries[5]["group"] == "Default" and entries[5]["name"] == "plain-entry.m3u8", "plain address line")

    print("2. First start")
    if OFFLINE:
        K.ANSWERS[:] = [False]                       # decline the radio stations
    else:
        K.ANSWERS[:] = [True, "PRESELECTED"]         # accept; take the preselected country
    # "PRESELECTED" → answer the select with the index the add-on preselected (Italy, Kodi language "it")
    original_select = K.Dialog.select

    def select(self, heading, items, preselect=-1, *a, **k):
        if K.ANSWERS and K.ANSWERS[0] == "PRESELECTED":
            K.ANSWERS.pop(0)
            K.LOG.append(("select-preselected", items[preselect]))
            return preselect
        return original_select(self, heading, items, *a, **k)

    K.Dialog.select = select
    root = call()
    check(labels(root) == ["TV", "Radio", "Favourites", "Search", "Playlists"], "main menu")
    check(K.SETTINGS["first_run_done"] == "true", "radio offered only once")
    if not OFFLINE:
        picked = [v for k, v in K.LOG if k == "select-preselected"]
        check(picked and picked[0].startswith("Ital"), "Italy preselected from Kodi language: %s" % picked)
        radio = call("action=groups&type=radio")
        check(len(radio) > 3 and radio[0][1].startswith("All ("), "radio categories: %s" % labels(radio)[:5])
    asked_before = len([k for k, v in K.LOG if k == "yesno"])
    call()
    asked_after = len([k for k, v in K.LOG if k == "yesno"])
    check(asked_after == asked_before, "second start does not ask again")

    print("3. Add playlist by web address")
    K.ANSWERS[:] = ["http://127.0.0.1:%d/list.m3u" % port, "My list", 0]   # address, name, Automatic
    call("action=pl_add_url")
    notes = [v for k, v in K.LOG if k == "notify"]
    check(notes and notes[-1] == "My list: 6 channels", "loaded: %s" % notes[-1:])
    tv = call("action=groups&type=tv")
    # 3 channels: the two "News One" entries are one channel with 2 links
    check(labels(tv) == ["All (3)", "News (1)", "Sport (1)", "My list (1)"], "TV categories %s" % labels(tv))

    print("4. Channels and fallback")
    channels = call("action=channels&type=tv&group=News")
    check(labels(channels) == ["News One"] and channels[0][2] == "2 links", "duplicate merged: 2 links")
    check(channels[0][4].get("IsPlayable") == "true", "playable item")
    play_url = channels[0][0]
    del K.RESOLVED[:]
    run([play_url.split("?")[0], "1", "?" + play_url.split("?")[1]])
    check(K.RESOLVED and K.RESOLVED[-1][0] and K.RESOLVED[-1][1].endswith("/stream.m3u8"),
          "dead first link skipped, second plays: %s" % K.RESOLVED[-1:])

    print("5. Favourites")
    K.ANSWERS[:] = [1]                                   # which link? → second
    call("action=fav_add&type=tv&group=News&name=News+One")
    K.ANSWERS[:] = []
    call("action=fav_add&type=radio&group=Music&name=Radio+Rock")
    favs = call("action=favorites")
    check(labels(favs) == ["News One", "Radio Rock"], "two favourites")
    rock_url = "http://127.0.0.1:%d/rock.mp3" % port
    call("action=fav_move&offset=-1&url=" + rock_url)
    check(labels(call("action=favorites")) == ["Radio Rock", "News One"], "moved up")
    call("action=fav_remove&url=" + rock_url)
    check(labels(call("action=favorites")) == ["News One"], "removed")

    print("6. Search")
    K.ANSWERS[:] = ["radio"]
    call("action=search")
    update = [v for k, v in K.LOG if k == "builtin"][-1]
    check("q=radio" in update, "re-opens with the query: %s" % update)
    found = call("action=search&q=radio")
    # (online, the free Italian stations from the first start match "radio" too)
    check(labels(found)[-2:] == ["Radio Rock", "Radio Pop"] and "News One" not in labels(found),
          "found the test radios (%d results)" % len(found))

    print("7. Playlists menu and delete")
    pls = call("action=playlists")
    check(labels(pls)[-3:] == ["[B]+ Add M3U playlist (web address)[/B]", "[B]+ Add M3U playlist (file)[/B]",
                               "[B]+ Add free radio stations by country[/B]"], "add entries listed")
    my_id = [i[0] for i in pls if i[1] == "My list"][0].split("id=")[1]
    K.ANSWERS[:] = [True]
    call("action=pl_delete&id=" + my_id)
    check("My list" not in labels(call("action=playlists")), "playlist deleted")
    check(labels(call("action=favorites")) == ["News One"], "favourites stay after delete")

    print("8. Errors are friendly")
    K.ANSWERS[:] = ["http://127.0.0.1:9/nothing.m3u", "Broken", 0]
    call("action=pl_add_url")
    oks = [v for k, v in K.LOG if k == "ok"]
    check(oks and oks[-1].startswith("Could not load the playlist"), "error dialog shown")
    check("Broken" not in labels(call("action=playlists")), "failed playlist not kept")

    print("\n%s" % ("ALL TESTS PASSED" if not check.failed else "%d TEST(S) FAILED" % check.failed))
    shutil.rmtree(K.PROFILE, ignore_errors=True)
    shutil.rmtree(WWW, ignore_errors=True)
    sys.exit(1 if check.failed else 0)


if __name__ == "__main__":
    main()
