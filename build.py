# -*- coding: utf-8 -*-
"""Builds the Kodi add-on zips and the repository folder to publish on the web.

Usage (from the project root):
    python kodi/build.py --base-url https://your-site.example/kodi/

Creates kodi/dist/:
    plugin.video.tvsplayer-<version>.zip     install directly ("Install from zip file")
    repository.tvsplayer-<version>.zip       install once; then TVS Player comes from the repository
    repo/                                    upload THIS folder's content to --base-url
        addons.xml, addons.xml.md5, zips/<addon id>/<addon id>-<version>.zip (+ icon, fanart)
"""
import argparse
import hashlib
import os
import re
import shutil
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
ADDONS = ["plugin.video.tvsplayer", "repository.tvsplayer"]
SKIP_DIRS = {"__pycache__", ".git", ".idea"}
SKIP_FILES = (".pyc", ".pyo", ".DS_Store")


def addon_xml(addon_id, base_url):
    with open(os.path.join(HERE, addon_id, "addon.xml"), encoding="utf-8") as f:
        text = f.read()
    text = re.sub(r"<!--.*?-->\n?", "", text, flags=re.S)   # build notes are not for users
    return text.replace("@BASE_URL@", base_url)


def version_of(xml):
    return re.search(r'<addon[^>]*\sversion="([^"]+)"', xml).group(1)


def make_zip(addon_id, xml, target):
    """Zip with the add-on folder at the root (what Kodi expects)."""
    source = os.path.join(HERE, addon_id)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if name.endswith(SKIP_FILES):
                    continue
                path = os.path.join(root, name)
                arc = os.path.join(addon_id, os.path.relpath(path, source)).replace("\\", "/")
                if name == "addon.xml" and root == source:
                    z.writestr(arc, xml)       # with the real repository address
                else:
                    z.write(path, arc)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True,
                        help="public address of the repository folder, e.g. https://example.com/kodi/")
    base_url = parser.parse_args().base_url
    if not base_url.endswith("/"):
        base_url += "/"

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    repo = os.path.join(DIST, "repo")
    os.makedirs(os.path.join(repo, "zips"))

    # The repository add-on uses the plug-in's icon
    shutil.copy(os.path.join(HERE, "plugin.video.tvsplayer", "resources", "icon.png"),
                os.path.join(HERE, "repository.tvsplayer", "icon.png"))

    entries = []
    for addon_id in ADDONS:
        xml = addon_xml(addon_id, base_url)
        version = version_of(xml)
        name = "%s-%s.zip" % (addon_id, version)
        make_zip(addon_id, xml, os.path.join(DIST, name))

        folder = os.path.join(repo, "zips", addon_id)
        os.makedirs(folder)
        shutil.copy(os.path.join(DIST, name), os.path.join(folder, name))
        # Artwork shown when browsing the repository in Kodi
        for asset in re.findall(r"<(?:icon|fanart)>([^<]+)</", xml):
            src = os.path.join(HERE, addon_id, asset)
            if os.path.exists(src):
                dst = os.path.join(folder, asset)
                os.makedirs(os.path.dirname(dst) or folder, exist_ok=True)
                shutil.copy(src, dst)
        entries.append(re.sub(r"^<\?xml[^>]*\?>\s*", "", xml.strip()))
        print("built %s" % name)

    addons = u'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n%s\n</addons>\n' % "\n".join(entries)
    with open(os.path.join(repo, "addons.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(addons)
    with open(os.path.join(repo, "addons.xml.md5"), "w", encoding="utf-8") as f:
        f.write(hashlib.md5(addons.encode("utf-8")).hexdigest())
    # Kodi's File manager ("Add source") browses an address through its HTML links: put the
    # repository zip at the top level with a small index page, so users can pick it from Kodi.
    repo_zip = "repository.tvsplayer-%s.zip" % version_of(addon_xml("repository.tvsplayer", base_url))
    shutil.copy(os.path.join(DIST, repo_zip), os.path.join(repo, repo_zip))
    index = (
        '<!DOCTYPE html>\n'
        '<html><head><meta charset="utf-8"><title>TVS Player for Kodi</title></head>\n'
        '<body>\n<h1>TVS Player for Kodi</h1>\n'
        '<p>In Kodi: Add-ons &rarr; Install from zip file &rarr; this source &rarr; %s</p>\n'
        '<a href="%s">%s</a>\n'
        '</body></html>\n'
    ) % (repo_zip, repo_zip, repo_zip)
    with open(os.path.join(repo, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(index)
    print("repository folder: %s  (upload its content to %s)" % (repo, base_url))


if __name__ == "__main__":
    main()
