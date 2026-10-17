#!/usr/bin/env python3
"""Generate loose-bundle BrandLogo / BrandLogoNight PNGs for iOS LaunchScreen.

Usage:
  python3 generate_launch_logos.py SOURCE.png --out ios/Runner \\
      --gold E0B45D --width 400 --height 363

Requires: Pillow
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def knockout_black(im: Image.Image) -> Image.Image:
    """Match Flutter SplashLogo.knockoutBlack: alpha = min(255, 4*(R+G+B), srcA)."""
    im = im.convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            out_a = min(255, 4 * (r + g + b), a)
            px[x, y] = (r, g, b, out_a)
    return im


def tint_gold(im: Image.Image, gold: tuple[int, int, int]) -> Image.Image:
    """Solid gold with source alpha (srcIn)."""
    out = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sp, op = im.load(), out.load()
    w, h = im.size
    gr, gg, gb = gold
    for y in range(h):
        for x in range(w):
            _, _, _, a = sp[x, y]
            if a:
                op[x, y] = (gr, gg, gb, a)
    return out


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.removeprefix("#")
    if len(s) != 6:
        raise argparse.ArgumentTypeError(f"expected RRGGBB, got {s}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path, help="Source logo PNG (often studio black bg)")
    p.add_argument("--out", type=Path, required=True, help="Output directory (ios/Runner)")
    p.add_argument("--gold", type=parse_hex, default=parse_hex("E0B45D"))
    p.add_argument("--width", type=int, default=400, help="@1x width")
    p.add_argument("--height", type=int, default=363, help="@1x height")
    args = p.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    base = knockout_black(Image.open(args.source))
    night = tint_gold(base, args.gold)

    for scale, suffix in ((1, ""), (2, "@2x"), (3, "@3x")):
        size = (args.width * scale, args.height * scale)
        light = base.resize(size, Image.Resampling.LANCZOS)
        dark = night.resize(size, Image.Resampling.LANCZOS)
        light.save(args.out / f"BrandLogo{suffix}.png", "PNG")
        dark.save(args.out / f"BrandLogoNight{suffix}.png", "PNG")
        print("wrote", f"BrandLogo{suffix}.png", f"BrandLogoNight{suffix}.png", size)


if __name__ == "__main__":
    main()
