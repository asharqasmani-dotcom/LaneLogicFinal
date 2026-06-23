#!/usr/bin/env python3
"""Remove ONLY the exterior white background from the truck image.

The truck body is also white, so a global white->alpha would destroy it.
Instead we flood-fill inward from the image border: only white pixels that are
connected to the edge (the backdrop) become transparent. White enclosed by the
truck's dark outlines (body panels) is preserved.
"""
from PIL import Image
from collections import deque

SRC = "assets/Car Image.png"
OUT = "assets/processed/Car Image.png"
CUT = 232  # brightness threshold for "background white"

img = Image.open(SRC).convert("RGBA")
w, h = img.size
px = img.load()


def is_bg(x, y):
    r, g, b, a = px[x, y]
    return r >= CUT and g >= CUT and b >= CUT


visited = bytearray(w * h)
q = deque()

# seed from every border pixel that is white
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
    px[x, y] = (r, g, b, 0)  # make background transparent
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny * w + nx]:
            if is_bg(nx, ny):
                visited[ny * w + nx] = 1
                q.append((nx, ny))

img.save(OUT)
print("wrote", OUT)
