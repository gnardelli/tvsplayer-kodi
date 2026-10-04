# -*- coding: utf-8 -*-
"""Small HTTP helpers (standard library only)."""
try:
    from urllib.request import Request, urlopen
except ImportError:  # pragma: no cover
    from urllib2 import Request, urlopen

USER_AGENT = "TVSPlayer-Kodi/1.0"


def _split_kodi_url(url):
    """'http://x/y|User-Agent=a&Referer=b' -> ('http://x/y', {'User-Agent': 'a', 'Referer': 'b'})."""
    address, _, options = url.partition("|")
    headers = {}
    for part in options.split("&"):
        key, _, value = part.partition("=")
        if key:
            headers[key] = value
    return address, headers


def get_text(url, timeout=20):
    address, headers = _split_kodi_url(url)
    headers.setdefault("User-Agent", USER_AGENT)
    response = urlopen(Request(address, headers=headers), timeout=timeout)
    try:
        raw = response.read()
    finally:
        response.close()
    for encoding in ("utf-8-sig", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def is_reachable(url, timeout=4):
    """Quick check that a stream answers, used to skip dead links before playing."""
    address, headers = _split_kodi_url(url)
    if not address.lower().startswith(("http://", "https://")):
        return True  # rtmp, udp…: cannot be checked cheaply, let Kodi try
    headers.setdefault("User-Agent", USER_AGENT)
    try:
        response = urlopen(Request(address, headers=headers), timeout=timeout)
        try:
            ok = response.getcode() < 400
            response.read(1)
        finally:
            response.close()
        return ok
    except Exception:
        return False
