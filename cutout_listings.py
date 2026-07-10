#!/usr/bin/env python3
"""Remove baked-in matte backgrounds from Listings page assets (v2)."""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

ROOT = Path("assets/listings")

SKIP = {
    ROOT / "hero" / "listings-hero.png",
    ROOT / "stories" / "brandon-kent.png",
    ROOT / "stories" / "marcus-thompson.png",
    ROOT / "stories" / "jason-ellis.png",
}

WHITE_ON_BLUE = set((ROOT / "how-it-works").glob("step-*.png")) | {
    ROOT / "guarantee-strip" / "icon-guarantee.png",
    ROOT / "guarantee-strip" / "icon-stand-behind.png",
    ROOT / "guarantee-strip" / "icon-relationships.png",
    ROOT / "stories" / "action-learn.png",
    ROOT / "stories" / "action-book.png",
    ROOT / "stories" / "action-browse.png",
}

BLUE_ON_WHITE = {
    ROOT / "how-it-works" / "icon-vehicle.png",
    ROOT / "how-it-works" / "icon-calendar.png",
    ROOT / "how-it-works" / "arrow-white.png",
}
BLUE_ON_WHITE |= set((ROOT / "guarantee").glob("feature-*.png"))
BLUE_ON_WHITE |= set((ROOT / "why").glob("icon-*.png"))
BLUE_ON_WHITE |= {
    ROOT / "stories" / "icon-saved.png",
    ROOT / "stories" / "icon-recon.png",
    ROOT / "stories" / "icon-thousands.png",
    ROOT / "guarantee" / "check-circle.png",
    ROOT / "stories" / "quote-circle.png",
    ROOT / "stories" / "star.png",
}

BLACK_MATTE = {
    ROOT / "stories" / "action-arrow.png",
}

SKY = {
    ROOT / "guarantee" / "delivery-truck.png",
}

BADGE = {
    ROOT / "guarantee" / "guarantee-badge.png",
}

VEHICLES = set((ROOT / "vehicles").glob("*.png"))


def is_blue(r: int, g: int, b: int) -> bool:
    return b >= 90 and b >= r + 20 and b >= g - 15


def is_white(r: int, g: int, b: int, cut: int = 238) -> bool:
    return r >= cut and g >= cut and b >= cut


def is_black(r: int, g: int, b: int, cut: int = 28) -> bool:
    return r <= cut and g <= cut and b <= cut


def is_sky(r: int, g: int, b: int) -> bool:
    return r >= 150 and g >= 180 and b >= 200 and b >= r + 15


def flood_to_alpha(img: Image.Image, predicate) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    visited = bytearray(w * h)
    q: deque[tuple[int, int]] = deque()

    def try_seed(x: int, y: int) -> None:
        idx = y * w + x
        if visited[idx]:
            return
        r, g, b, a = px[x, y]
        if predicate(r, g, b):
            visited[idx] = 1
            q.append((x, y))

    for x in range(w):
        for y in (0, h - 1):
            try_seed(x, y)
    for y in range(h):
        for x in (0, w - 1):
            try_seed(x, y)

    while q:
        x, y = q.popleft()
        r, g, b, a = px[x, y]
        px[x, y] = (r, g, b, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not visited[idx]:
                    r2, g2, b2, a2 = px[nx, ny]
                    if predicate(r2, g2, b2):
                        visited[idx] = 1
                        q.append((nx, ny))
    return img


def keep_white_only(img: Image.Image, cut: int = 210) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= cut and g >= cut and b >= cut:
                px[x, y] = (255, 255, 255, 255)
            else:
                px[x, y] = (255, 255, 255, 0)
    return img


def remove_white_only(img: Image.Image, cut: int = 235) -> Image.Image:
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if r >= cut and g >= cut and b >= cut:
                px[x, y] = (255, 255, 255, 0)
    return img


def process(path: Path) -> None:
    img = Image.open(path)

    if path in WHITE_ON_BLUE:
        out = keep_white_only(img)
    elif path in BLUE_ON_WHITE:
        out = remove_white_only(flood_to_alpha(img, lambda r, g, b: is_white(r, g, b, 230)))
    elif path in BLACK_MATTE:
        out = flood_to_alpha(img, is_black)
    elif path in SKY:
        out = flood_to_alpha(img, lambda r, g, b: is_sky(r, g, b) or is_white(r, g, b, 245))
    elif path in BADGE:
        out = flood_to_alpha(img, lambda r, g, b: is_white(r, g, b, 235))
    elif path in VEHICLES:
        out = flood_to_alpha(img, lambda r, g, b: is_white(r, g, b, 245))
    else:
        out = flood_to_alpha(img, lambda r, g, b: is_white(r, g, b, 235))

    out.save(path)
    print("processed", path)


def main() -> None:
    for path in sorted(ROOT.rglob("*.png")):
        if path in SKIP:
            print("skip", path)
            continue
        process(path)


if __name__ == "__main__":
    main()
