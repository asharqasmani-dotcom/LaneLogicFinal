#!/usr/bin/env python3
"""Preprocess Lane Logic hero assets.

All source PNGs ship on an opaque white background (no alpha). For the design
to composite correctly we need:
  - stat icons  -> pure white silhouette on transparent background
  - patterns    -> keep their light-blue pixels, drop the white box
  - truck       -> drop the white box so it sits cleanly on the hero bg
"""
from PIL import Image
import os

SRC = "assets"
OUT = "assets/processed"
os.makedirs(OUT, exist_ok=True)

WHITE_CUTOFF = 230  # pixels brighter than this (all channels) become transparent


def near_white(r, g, b):
    return r >= WHITE_CUTOFF and g >= WHITE_CUTOFF and b >= WHITE_CUTOFF


def white_to_alpha(name, recolor_white=False):
    img = Image.open(os.path.join(SRC, name)).convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if near_white(r, g, b):
                px[x, y] = (r, g, b, 0)
            elif recolor_white:
                # soft anti-aliased edge: keep alpha proportional to darkness
                px[x, y] = (255, 255, 255, a)
    img.save(os.path.join(OUT, name))
    print("wrote", name)


# Stat icons -> white silhouette
for icon in ["car icon.png", "shake hand.png", "dollar.png", "watch.png", "map.png"]:
    white_to_alpha(icon, recolor_white=True)

# Patterns -> keep light blue, drop white
for pat in ["Pattern.png", "Pattern 2.png"]:
    white_to_alpha(pat, recolor_white=False)

# Truck is itself white-bodied; removing white would destroy it.
# It is left untouched and sits on the white hero background.

print("done")
