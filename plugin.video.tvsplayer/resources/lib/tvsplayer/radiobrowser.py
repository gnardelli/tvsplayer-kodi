# -*- coding: utf-8 -*-
"""Free radio stations from Radio Browser (https://www.radio-browser.info).

Radio Browser is an open community database (public domain data) used by many radio apps.
The add-on only plays the stations' own public streams.
"""
import json
from collections import Counter

from . import net
from .m3u import RADIO

SOURCE_PREFIX = "radiobrowser:"
TAG_PREFIX = "tag:"                 # radiobrowser:tag:<genre> = genre search
_SERVERS = ("all", "de1", "nl1", "at1")   # "all" picks a mirror; the others are fallbacks
_MAX_CATEGORIES = 14


def source(country_code):
    return SOURCE_PREFIX + country_code.upper()


def tag_source(tag):
    return SOURCE_PREFIX + TAG_PREFIX + tag.strip().lower()


def country_of(src):
    return src[len(SOURCE_PREFIX):]


def _is_tag_source(src):
    return src.startswith(SOURCE_PREFIX + TAG_PREFIX)


def _tag_of(src):
    return src[len(SOURCE_PREFIX + TAG_PREFIX):]


def _get(path):
    last_error = None
    for server in _SERVERS:
        try:
            return json.loads(net.get_text("https://%s.api.radio-browser.info%s" % (server, path)))
        except Exception as e:  # try the next mirror
            last_error = e
    raise IOError("Radio stations could not be loaded (%s)" % last_error)


def countries():
    """[(code, name, station_count)] sorted by name, only countries with stations."""
    data = _get("/json/countries?hidebroken=true")
    result = [(c.get("iso_3166_1", ""), c.get("name", ""), int(c.get("stationcount", 0))) for c in data]
    return sorted([c for c in result if c[0] and c[2] > 0], key=lambda c: c[1].lower())


def genres():
    """[(tag, name, station_count)] of the top 200 genre tags, sorted alphabetically."""
    # Fetch the 200 most popular tags (so we don't get obscure ones)
    data = _get("/json/tags?hidebroken=true&order=stationcount&reverse=true&limit=200")
    result = []
    for t in data:
        name = (t.get("name") or "").strip()
        count = int(t.get("stationcount", 0))
        if name and count > 0:
            result.append((name, name.title(), count))
            
    # Sort the 200 results alphabetically by the display label
    return sorted(result, key=lambda x: x[1].lower())


def _entries(data):
    """Convert raw station records from the API into playlist entries."""
    found = []
    for s in data:
        url = (s.get("url_resolved") or s.get("url") or "").strip()
        name = (s.get("name") or "").strip()
        if not url or not name:
            continue
        tags = [t.strip().lower() for t in (s.get("tags") or "").split(",") if 2 <= len(t.strip()) <= 24]
        found.append((name, url, (s.get("favicon") or "").strip(), tags))

    # Categories = the most common genre tags; tags almost every station has say nothing
    counts = Counter(t for _, _, _, tags in found for t in set(tags))
    categories = {t for t, n in counts.most_common() if 3 <= n < len(found) / 2}
    categories = set(sorted(categories, key=lambda t: -counts[t])[:_MAX_CATEGORIES])

    entries = []
    for name, url, logo, tags in found:
        tag = next((t for t in tags if t in categories), None)
        entries.append({
            "name": name,
            "logo": logo,
            "group": tag.title() if tag else "Other",
            "url": url,
            "type": RADIO,
        })
    return entries


def stations(country_code, limit=500):
    """Most popular working stations of a country as playlist entries, grouped by main genre."""
    data = _get("/json/stations/search?countrycode=%s&hidebroken=true&order=clickcount&reverse=true&limit=%d"
                % (country_code, limit))
    return _entries(data)


def genre_stations(tag, limit=500):
    """Most popular working stations for a genre/tag as playlist entries, grouped by main genre."""
    data = _get("/json/stations/search?tag=%s&hidebroken=true&order=clickcount&reverse=true&limit=%d"
                % (net.quote(tag), limit))
    return _entries(data)


def stations_for(src, limit=500):
    """Dispatch on a source string: country source or genre source."""
    if _is_tag_source(src):
        return genre_stations(_tag_of(src), limit)
    return stations(country_of(src), limit)
    
def search_raw(query, limit=50):
    """Returns the raw API response for a name search (used for selection dialogs)."""
    # Using the exact endpoint you provided, but keeping it strict to 50 results
    return _get("/json/stations/search?name=%s&hidebroken=true&order=name&reverse=true&limit=%d"
                % (net.quote(query), limit))    