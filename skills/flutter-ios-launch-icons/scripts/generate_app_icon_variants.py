#!/usr/bin/env python3
"""Generate Dark + Tinted App Icon variants from a light 1024 marketing icon.

Usage:
  python3 generate_app_icon_variants.py Icon-App-1024x1024@1x.png \\
      --out ios/Runner/Assets.xcassets/AppIcon.appiconset \\
      --plate 17120E --gold-deep C9953E --gold-light F8E7C0

Requires: Pillow
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def parse_hex(s: str) -> tuple[int, int, int]:
    s = s.removeprefix("#")
    if len(s) != 6:
        raise argparse.ArgumentTypeError(f"expected RRGGBB, got {s}")
    return int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def coverage(r: int, g: int, b: int, bg: tuple[int, int, int], lo: int = 48, hi: int = 120) -> float:
    d = abs(r - bg[0]) + abs(g - bg[1]) + abs(b - bg[2])
    if d <= lo:
        return 0.0
    if d >= hi:
        return 1.0
    return (d - lo) / (hi - lo)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path, help="Light 1024 App Icon PNG")
    p.add_argument("--out", type=Path, required=True, help="AppIcon.appiconset directory")
    p.add_argument("--plate", type=parse_hex, default=parse_hex("17120E"), help="Dark icon background")
    p.add_argument("--gold-deep", type=parse_hex, default=parse_hex("C9953E"))
    p.add_argument("--gold-light", type=parse_hex, default=parse_hex("F8E7C0"))
    p.add_argument("--home-sizes", action="store_true", help="Also write 60pt @2x/@3x variants")
    args = p.parse_args()

    src = Image.open(args.source).convert("RGBA")
    w, h = src.size
    bg = src.getpixel((10, 10))[:3]
    dark = Image.new("RGB", (w, h))
    tinted = Image.new("RGB", (w, h))
    dp, tp, sp = dark.load(), tinted.load(), src.load()

    for y in range(h):
        for x in range(w):
            r, g, b, _ = sp[x, y]
            c = coverage(r, g, b, bg)
            lum = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            gold = mix(args.gold_deep, args.gold_light, min(1.0, lum * 1.35))
            dp[x, y] = mix(args.plate, gold, c)
            shade = int(255 * c)
            tp[x, y] = (shade, shade, shade)

    args.out.mkdir(parents=True, exist_ok=True)
    dark_path = args.out / "Icon-App-1024x1024-dark.png"
    tinted_path = args.out / "Icon-App-1024x1024-tinted.png"
    dark.save(dark_path, "PNG")
    tinted.save(tinted_path, "PNG")
    print("wrote", dark_path.name, tinted_path.name)

    if args.home_sizes:
        for scale in (2, 3):
            size = 60 * scale
            name = f"60x60@{scale}x"
            dark.resize((size, size), Image.Resampling.LANCZOS).save(
                args.out / f"Icon-App-{name}-dark.png", "PNG"
            )
            tinted.resize((size, size), Image.Resampling.LANCZOS).save(
                args.out / f"Icon-App-{name}-tinted.png", "PNG"
            )
            print("wrote", f"Icon-App-{name}-dark.png", f"Icon-App-{name}-tinted.png")


if __name__ == "__main__":
    main()
