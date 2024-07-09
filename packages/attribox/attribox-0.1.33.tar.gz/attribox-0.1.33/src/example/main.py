"""Example test script."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from example import Rectangle

if __name__ == '__main__':
  r = Rectangle(0, 0, 69, 420)
  print(r)
  r.topLeft.x = 77
  print(r)
