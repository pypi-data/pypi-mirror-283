# mkdocs-material-extensions-2
# Copyright (C) 2024-Present  Zhiyuan Chen

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import annotations

import codecs
import functools
import os
from glob import iglob
from inspect import getfile
from xml.etree.ElementTree import Element

import material
from markdown import Markdown
from pymdownx import emoji, emoji1_db, gemoji_db, twemoji_db

emoji_dbs = {"twemoji": twemoji_db, "emoji1": emoji1_db, "gemoji": gemoji_db}


def twemoji(options: object, md: Markdown):
    paths = options.get("custom_icons", [])[:]
    return _load_emoji_index(tuple(paths), "twemoji")


def emoji1(options: object, md: Markdown):
    paths = options.get("custom_icons", [])[:]
    return _load_emoji_index(tuple(paths), "emoji1")


def gemoji(options: object, md: Markdown):
    paths = options.get("custom_icons", [])[:]
    return _load_emoji_index(tuple(paths), "gemoji")


def to_svg(
    index: str,
    shortname: str,
    alias: str,
    uc: str | None,
    alt: str,
    title: str,
    category: str,
    options: object,
    md: Markdown,
):
    if not uc:
        icons = md.inlinePatterns["emoji"].emoji_index["emoji"]

        # Create and return element to host icon
        el = Element("span", {"class": options.get("classes", index)})
        el.text = md.htmlStash.store(_load(icons[shortname]["path"]))
        return el

    # Delegate to `pymdownx.emoji` extension
    return emoji.to_svg(index, shortname, alias, uc, alt, title, category, options, md)


def to_png(
    index: str,
    shortname: str,
    alias: str,
    uc: str | None,
    alt: str,
    title: str,
    category: str,
    options: object,
    md: Markdown,
):
    if not uc:
        icons = md.inlinePatterns["emoji"].emoji_index["emoji"]

        # Create and return element to host icon
        el = Element("span", {"class": options.get("classes", index)})
        el.text = md.htmlStash.store(_load(icons[shortname]["path"]))
        return el

    # Delegate to `pymdownx.emoji` extension
    return emoji.to_png(index, shortname, alias, uc, alt, title, category, options, md)


@functools.lru_cache(maxsize=None)
def _load(file: str):
    with codecs.open(file, encoding="utf-8") as f:
        return f.read()


@functools.lru_cache(maxsize=None)
def _load_emoji_index(paths, name: str = "twemoji"):
    emoji_db = emoji_dbs[name]
    index = {"name": name, "emoji": emoji_db.emoji, "aliases": emoji_db.aliases}

    # Compute path to theme root and traverse all icon directories
    root = os.path.dirname(getfile(material))
    root = os.path.join(root, "templates", ".icons")
    for path in [*paths, root]:
        base = os.path.normpath(path)

        # Index icons provided by the theme and via custom icons
        glob = os.path.join(base, "**", "*.svg")
        glob = iglob(os.path.normpath(glob), recursive=True)
        for file in glob:
            icon = file[len(base) + 1 : -4].replace(os.path.sep, "-")

            # Add icon to index
            name = f":{icon}:"
            if not any(name in index[key] for key in ["emoji", "aliases"]):
                index["emoji"][name] = {"name": name, "path": file}

    # Return index
    return index
