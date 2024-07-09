"""Rectangle provides a class representation of a plane rectangle."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriBox
from example import Point


class Rectangle:
  """This rectangle now uses AttriBox to define topLeft and bottomRight
  corners. """

  __field_name__ = None
  __field_owner__ = None

  topLeft = AttriBox[Point](0, 0)
  bottomRight = AttriBox[Point](0, 0)

  def __init__(self, *args) -> None:
    print('%s start of __init__' % self.__class__.__name__)
    intArgs = []
    pointArgs = []
    for arg in args:
      if isinstance(arg, int):
        intArgs.append(arg)
      elif isinstance(arg, Point):
        pointArgs.append(arg)
    if len(pointArgs) == 2:
      self.topLeft.x = pointArgs[0].x
      self.topLeft.y = pointArgs[0].y
      self.bottomRight.x = pointArgs[1].x
      self.bottomRight.y = pointArgs[1].y
    elif len(intArgs) == 4:
      self.bottomRight.y = intArgs.pop()
      self.bottomRight.x = intArgs.pop()
      self.topLeft.y = intArgs.pop()
      self.topLeft.x = intArgs.pop()
    clsName = self.__class__.__name__
    print('End of %s.__init__' % (clsName,))

  def getName(self) -> str:
    """Getter-function for instance name. If __set_name__ has run, the
    name received is included here."""
    if self.__field_name__ is None:
      return self.__class__.__name__
    return '%s.%s' % (self.__field_owner__.__name__, self.__field_name__)

  def __str__(self, ) -> str:
    """String representation of the rectangle. """
    return '%s(%s, %s)' % (self.getName(), self.topLeft, self.bottomRight)

  def area(self) -> int:
    """Returns the area of the rectangle. """
    v = self.topLeft - self.bottomRight
    return abs(v.x * v.y)
