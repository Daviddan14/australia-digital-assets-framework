"""Prepare fonts and images in site/assets/. Run once, or when the brand kit changes.

    python3 tools/assets.py

Fonts: Be Vietnam Pro and JetBrains Mono (SIL Open Font License), taken from
the @fontsource packages on npm and cut down to the characters this site uses.
Logos: the two lockups from the Task Board brand kit.
Needs: fonttools, brotli, Pillow.
"""

import io
import os
import tarfile
import urllib.request

from fontTools import subset
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "site", "assets")
BUILD = os.path.join(ROOT, "build")
BRAND_KIT = "https://taskboard.redbellydao.network/brand/"

# npm package: (version, weights, short name used for the files in site/assets/fonts)
FONTS = {
    "be-vietnam-pro": ("5.2.5", ["400", "500", "600", "700"], "vietnam"),
    "jetbrains-mono": ("5.2.5", ["400", "500"], "jbmono"),
}
LOGOS = {"dao-logo-on-dark": "logo-dark-bg", "dao-logo-on-light": "logo-light-bg"}
# Basic Latin, Latin-1, general punctuation, currency, arrows, minus, ellipsis.
UNICODES = "U+0020-007E,U+00A0-00FF,U+2010-2027,U+2030-203A,U+20AC,U+2122,U+2190-2193,U+2212,U+2713,U+2715"

SLATE = (12, 19, 23)
STEEL = (29, 49, 64)
INK = (241, 245, 248)
MUTED = (143, 161, 173)
RED = (239, 83, 80)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def fonts():
    out_dir = os.path.join(ASSETS, "fonts")
    ttf_dir = os.path.join(BUILD, "ttf")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(ttf_dir, exist_ok=True)
    for family, (version, weights, short) in FONTS.items():
        tgz = fetch(f"https://registry.npmjs.org/@fontsource/{family}/-/{family}-{version}.tgz")
        with tarfile.open(fileobj=io.BytesIO(tgz)) as tar:
            for weight in weights:
                member = tar.extractfile(f"package/files/{family}-latin-{weight}-normal.woff2")
                src = os.path.join(BUILD, f"{family}-{weight}.woff2")
                with open(src, "wb") as fh:
                    fh.write(member.read())
                options = subset.Options()
                options.flavor = "woff2"
                options.layout_features = ["kern", "liga", "calt", "tnum", "case"]
                options.name_IDs = ["*"]
                font = subset.load_font(src, options)
                subsetter = subset.Subsetter(options)
                subsetter.populate(unicodes=subset.parse_unicodes(UNICODES))
                subsetter.subset(font)
                subset.save_font(font, os.path.join(out_dir, f"{short}-{weight}.woff2"), options)
                # a TTF copy for drawing the social card
                ttf = TTFont(src)
                ttf.flavor = None
                ttf.save(os.path.join(ttf_dir, f"{family}-{weight}.ttf"))
                print("font", family, weight)


def logos():
    img_dir = os.path.join(ASSETS, "img")
    os.makedirs(img_dir, exist_ok=True)
    marks = {}
    for name, out_name in LOGOS.items():
        im = Image.open(io.BytesIO(fetch(BRAND_KIT + name + ".png"))).convert("RGBA")
        im = im.crop(im.getbbox())
        marks[name] = im
        small = im.copy()
        small.thumbnail((360, 360), Image.LANCZOS)
        small.save(os.path.join(img_dir, out_name + ".png"), optimize=True)
        print("logo", name, small.size)
    # The mark alone (hexagon and DAO roundel) is the top part of the lockup.
    lockup = marks["dao-logo-on-dark"]
    mark = lockup.crop((0, 0, lockup.width, int(lockup.height * 0.70)))
    mark = mark.crop(mark.getbbox())
    for size, name in ((32, "favicon-32.png"), (180, "touch-icon-180.png"), (512, "app-icon-512.png")):
        tile = Image.new("RGBA", (size, size), SLATE + (255,))
        pad = int(size * 0.12)
        m = mark.copy()
        m.thumbnail((size - 2 * pad, size - 2 * pad), Image.LANCZOS)
        tile.alpha_composite(m, ((size - m.width) // 2, (size - m.height) // 2))
        tile.convert("RGB").save(os.path.join(img_dir, name), optimize=True)
    return marks


def social_card(marks):
    ttf = os.path.join(BUILD, "ttf")
    w, h = 1200, 630
    card = Image.new("RGBA", (w, h), SLATE + (255,))
    draw = ImageDraw.Draw(card)
    draw.rectangle((0, 0, w, 10), fill=RED)
    draw.rectangle((0, h - 150, w, h), fill=STEEL)
    mono = ImageFont.truetype(os.path.join(ttf, "jetbrains-mono-500.ttf"), 26)
    head = ImageFont.truetype(os.path.join(ttf, "be-vietnam-pro-700.ttf"), 64)
    body = ImageFont.truetype(os.path.join(ttf, "be-vietnam-pro-400.ttf"), 30)
    draw.text((72, 70), "PLAIN-LANGUAGE EXPLAINER", font=mono, fill=MUTED)
    draw.text((72, 120), "The Digital Assets\nFramework Act,\nin plain words", font=head, fill=INK, spacing=10)
    draw.text((72, h - 112), "Who needs a licence, the key dates, and what it\nmeans for issuers and Tokeniser on Redbelly", font=body, fill=INK, spacing=8)
    logo = marks["dao-logo-on-dark"].copy()
    logo.thumbnail((300, 300), Image.LANCZOS)
    card.alpha_composite(logo, (w - logo.width - 72, 110))
    card.convert("RGB").save(os.path.join(ASSETS, "img", "social-card.png"), optimize=True)
    print("social card")


if __name__ == "__main__":
    os.makedirs(BUILD, exist_ok=True)
    fonts()
    social_card(logos())
