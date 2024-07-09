"""Point provides a class representation of a two-dimensional point. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriBox


class Point:
  """This example class uses AttriBox to implement coordinates"""

  __field_name__ = None
  __field_owner__ = None

  x = AttriBox[int](0)
  y = AttriBox[int](0)

  def __set_name__(self, owner: type, name: str) -> None:
    """Sets the name of the field. This method runs only when the instance
    of the class is itself used as a descriptor."""
    self.__field_name__ = name
    self.__field_owner__ = owner

  def __init__(self, x: int = 0, y: int = 0) -> None:
    print('Point.__init__ at: (%d, %d)' % (x, y))
    self.x = x
    self.y = y

  @x.ONGET
  def _notifyGet(self, value: int) -> None:
    """This method notifies when an AttriBox calls __get__"""
    # value = maybe(value, 0)
    # print('%s.x get -> %d' % (self.getName(), value))

  @x.ONSET
  def _notifySet(self, oldVal: int, newVal: int) -> None:
    """This method notifies when an AttriBox calls __set__"""
    # newVal = maybe(newVal, 0)
    # oldVal = maybe(oldVal, 0)
    # print('%s.x set from %d to %d' % (self.getName(), oldVal, newVal))

  def __add__(self, other: Point) -> Point:
    """Implementation of the addition operator."""
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other: Point) -> Point:
    """Implementation of the subtraction operator."""
    return Point(self.x - other.x, self.y - other.y)

  def getFieldName(self) -> str:
    """Getter-function for the field name. """
    if self.__field_name__ is None:
      return self.__class__.__name__
    return self.__field_name__

  def getOwnerName(self) -> str:
    """Getter-function for the field owner. """
    if self.__field_owner__ is None:
      return self.__class__.__name__
    return self.__field_owner__.__name__

  def getName(self) -> str:
    """Getter-function for instance name. If __set_name__ has run, the
    name received is included here."""
    if self.__field_name__ is None:
      return self.__class__.__name__
    ownerName = self.getOwnerName()
    fieldName = self.getFieldName()
    return '%s.%s' % (ownerName, fieldName)

  def __str__(self, ) -> str:
    """String representation of the point. """
    return '(%d, %d)' % (self.x, self.y)

  def __repr__(self) -> str:
    """Code representation"""
    return '%s(%d, %d)' % (self.__class__.__name__, self.x, self.y)
