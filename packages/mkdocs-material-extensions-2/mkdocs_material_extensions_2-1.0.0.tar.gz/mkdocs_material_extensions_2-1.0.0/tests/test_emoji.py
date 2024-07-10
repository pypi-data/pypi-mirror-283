import os
import textwrap
from inspect import getfile

import markdown
import material
from bs4 import BeautifulSoup
from pymdownx.emoji import (  # GITHUB_CDN,
    EMOJIONE_PNG_CDN,
    EMOJIONE_SVG_CDN,
    GITHUB_UNICODE_CDN,
    TWEMOJI_PNG_CDN,
    TWEMOJI_SVG_CDN,
)

from materialy import emoji


class TestEmoji:

    extension = ["pymdownx.emoji"]
    extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.twemoji, "emoji_generator": emoji.to_svg}}

    md = markdown.Markdown(extensions=extension, extension_configs=extension_configs)

    def test_material_svg_injection(self):
        """Test that we inject icons for all the Material icon types."""

        text = r"""
        We can use Material Icons :material-airplane:.

        We can also use Fontawesome Icons :fontawesome-solid-hand:.

        That's not all, we can also use Octicons :octicons-alert-16:.
        """

        html = markdown.markdown(dedent(text), extensions=self.extension, extension_configs=self.extension_configs)

        soup = BeautifulSoup(html, "html.parser")

        p = soup.select("p")
        assert len(p) == 3
        assert p[0].select("span.twemoji > svg")
        assert p[1].select("span.twemoji > svg")
        assert p[2].select("span.twemoji > svg")

    def test_twemoji(self):
        extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.twemoji, "emoji_generator": emoji.to_svg}}
        md = markdown.Markdown(extensions=self.extension, extension_configs=extension_configs)
        smile = f'<p><img alt="\U0001f604" class="twemoji" src="{TWEMOJI_SVG_CDN}1f604.svg" title=":smile:" /></p>'
        assert md.convert(":smile:") == smile
        extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.twemoji, "emoji_generator": emoji.to_png}}
        md = markdown.Markdown(extensions=self.extension, extension_configs=extension_configs)
        smile = f'<p><img alt="\U0001f604" class="twemoji" src="{TWEMOJI_PNG_CDN}1f604.png" title=":smile:" /></p>'
        assert md.convert(":smile:") == smile

    def test_emoji1(self):
        extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.emoji1, "emoji_generator": emoji.to_svg}}
        md = markdown.Markdown(extensions=self.extension, extension_configs=extension_configs)
        smile = f'<p><img alt="\U0001f604" class="emoji1" src="{EMOJIONE_SVG_CDN}1f604.svg" title=":smile:" /></p>'
        assert md.convert(":smile:") == smile
        extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.emoji1, "emoji_generator": emoji.to_png}}
        md = markdown.Markdown(extensions=self.extension, extension_configs=extension_configs)
        smile = f'<p><img alt="\U0001f604" class="emoji1" src="{EMOJIONE_PNG_CDN}1f604.png" title=":smile:" /></p>'
        assert md.convert(":smile:") == smile

    def test_gemoji(self):
        extension_configs = {"pymdownx.emoji": {"emoji_index": emoji.gemoji, "emoji_generator": emoji.to_png}}
        md = markdown.Markdown(extensions=self.extension, extension_configs=extension_configs)
        smile = f'<p><img alt="\U0001f604" class="gemoji" src="{GITHUB_UNICODE_CDN}1f604.png" title=":smile:" /></p>'
        assert md.convert(":smile:") == smile

    def test_custom_icons(self):
        root = os.path.dirname(getfile(material))
        root = os.path.join(root, "templates", ".icons")
        arrow = (
            '<p><span class="twemoji"><svg xmlns="http://www.w3.org/2000/svg" '
            'viewBox="0 0 24 24"><path d="M13.22 19.03a.75.75 0 0 1 0-1.06L18.19 13H3.75a.75.75 '
            "0 0 1 0-1.5h14.44l-4.97-4.97a.749.749 0 0 1 .326-1.275.749.749 0 0 1 .734.215l6.25 "
            '6.25a.75.75 0 0 1 0 1.06l-6.25 6.25a.75.75 0 0 1-1.06 0Z"/></svg></span></p>'
        )
        assert self.md.convert(":octicons-arrow-right-24:") == arrow.replace("\n", "")


def dedent(text: str, strip: bool = True) -> str:
    return textwrap.dedent(text).strip("\n") if strip else textwrap.dedent(text)
