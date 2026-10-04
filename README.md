# TVS Player for Kodi

Play **your own M3U / M3U8 playlists** (from a web address or a file) and **thousands of free
radio stations** from the open [Radio Browser](https://www.radio-browser.info) directory, by country
and genre. Channels are sorted by category with logos and search, dead links are skipped
automatically, and favourites can be reordered.

TVS Player is only a player: it does not include or provide any TV channels or playlists.
Add only content you have the right to use.

## Install in Kodi (Kodi 19 Matrix or newer)

1. **Settings → System → Add-ons → Unknown sources: ON**
2. **Settings → File manager → Add source** → `<None>` → type
   `https://gnardelli.github.io/tvsplayer-kodi/` → name it `TVS Player` → OK
3. **Add-ons → Install from zip file → TVS Player → repository.tvsplayer-1.0.0.zip**
4. **Add-ons → Install from repository → TVS Player Repository → Video add-ons → TVS Player → Install**

Updates are installed automatically.

## Use

- **Playlists → Add M3U playlist (web address / file)**, or **Add free radio stations by country**
- **TV** and **Radio**: channels by category; **Search** across all playlists
- To reload a playlist that changed online: **Playlists → your playlist → Refresh**

## For developers

| Folder | Content |
|---|---|
| `plugin.video.tvsplayer/` | the add-on |
| `repository.tvsplayer/` | the repository add-on (address filled in by `build.py`) |
| `docs/` | the published Kodi repository (GitHub Pages) |
| `tests/` | tests that run without Kodi: `python tests/test_addon.py` |

Publish a new version: raise `version` and `<news>` in `plugin.video.tvsplayer/addon.xml`, then

```
python build.py --base-url https://gnardelli.github.io/tvsplayer-kodi/
```

and copy the content of `dist/repo/` into `docs/`.

## License

GPL-2.0-or-later, see [LICENSE.txt](LICENSE.txt).
