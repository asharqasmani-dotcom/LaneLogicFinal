#!/usr/bin/env python3
"""Remove the light-gray exterior background from the section-2 icons.

Each icon is a solid blue circle (with a white symbol inside) sitting on an
opaque ~#EFEFEF box. A global white/gray->alpha would punch holes in the white
symbol, so we flood-fill inward from the border: only light pixels connected to
the edge become transparent. The white symbol, enclosed by the blue circle, is
preserved.
"""
from PIL import Image
from collections import deque
import os

OUT = "assets/sec2/processed"
os.makedirs(OUT, exist_ok=True)
CUT = 215  # pixels brighter than this on all channels are "background"

ICONS = ["we buy icon.png", "we teach icon.png", "tick icon.png"]


def cutout(name):
    img = Image.open(os.path.join("assets/sec2", name)).convert("RGBA")
    w, h = img.size
    px = img.load()

    def is_bg(x, y):
        r, g, b, a = px[x, y]
        return r >= CUT and g >= CUT and b >= CUT

    visited = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_bg(x, y) and not visited[y * w + x]:
                visited[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_bg(x, y) and not visited[y * w + x]:
                visited[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx]:
                if is_bg(nx, ny):
                    visited[ny * w + nx] = 1
                    q.append((nx, ny))

    img.save(os.path.join(OUT, name))
    print("wrote", name)


for ic in ICONS:
    cutout(ic)
print("done")
