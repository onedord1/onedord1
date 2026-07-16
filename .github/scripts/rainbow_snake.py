#!/usr/bin/env python3
"""Convert the sentinel snake color emitted by Platane/snk into an animated SVG rainbow."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SENTINEL = re.compile(r"#ff00ff", re.IGNORECASE)

DEFS = r"""
<defs id="rainbow-snake-defs">
  <linearGradient id="rainbow-snake" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="900" y2="0" spreadMethod="reflect">
    <stop offset="0%" stop-color="#ff3b30">
      <animate attributeName="stop-color" values="#ff3b30;#ff9500;#ffd60a;#34c759;#30d5c8;#0a84ff;#5e5ce6;#bf5af2;#ff3b30" dur="7s" repeatCount="indefinite"/>
    </stop>
    <stop offset="25%" stop-color="#ffd60a">
      <animate attributeName="stop-color" values="#ffd60a;#34c759;#30d5c8;#0a84ff;#5e5ce6;#bf5af2;#ff3b30;#ff9500;#ffd60a" dur="7s" repeatCount="indefinite"/>
    </stop>
    <stop offset="50%" stop-color="#30d5c8">
      <animate attributeName="stop-color" values="#30d5c8;#0a84ff;#5e5ce6;#bf5af2;#ff3b30;#ff9500;#ffd60a;#34c759;#30d5c8" dur="7s" repeatCount="indefinite"/>
    </stop>
    <stop offset="75%" stop-color="#5e5ce6">
      <animate attributeName="stop-color" values="#5e5ce6;#bf5af2;#ff3b30;#ff9500;#ffd60a;#34c759;#30d5c8;#0a84ff;#5e5ce6" dur="7s" repeatCount="indefinite"/>
    </stop>
    <stop offset="100%" stop-color="#ff2d55">
      <animate attributeName="stop-color" values="#ff2d55;#ff9500;#ffd60a;#34c759;#30d5c8;#0a84ff;#5e5ce6;#bf5af2;#ff2d55" dur="7s" repeatCount="indefinite"/>
    </stop>
    <animateTransform attributeName="gradientTransform" type="translate" values="-180 0;180 0;-180 0" dur="5s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
""".strip()


def transform(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if 'id="rainbow-snake"' not in text:
        text, count = re.subn(r"(<svg\b[^>]*>)", r"\1\n" + DEFS, text, count=1, flags=re.IGNORECASE)
        if count != 1:
            raise RuntimeError(f"Could not locate opening <svg> element in {path}")

    replaced, count = SENTINEL.subn("url(#rainbow-snake)", text)
    if count == 0 and "url(#rainbow-snake)" not in text:
        raise RuntimeError(
            f"Sentinel snake color was not found in {path}. "
            "Platane/snk may have changed its SVG output format."
        )

    path.write_text(replaced, encoding="utf-8")
    print(f"Rainbow gradient applied to {path} ({count} replacement(s)).")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: rainbow_snake.py <snake.svg> [<snake.svg> ...]", file=sys.stderr)
        return 2

    for value in argv[1:]:
        transform(Path(value))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
