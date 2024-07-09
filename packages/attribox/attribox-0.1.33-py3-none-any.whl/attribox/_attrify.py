"""Attrify decorates a custom class leaving a new class subclassing the
decorated class, and with the AttriClass.__dict__ as the class body."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from attribox import AttriClass
from vistutils.waitaminute import typeMsg


class Attrify:
  """Attrify decorates a custom class leaving a new class subclassing the
  decorated class, and with the AttriClass.__dict__ as the class body."""

  __pos_args__ = None
  __key_args__ = None

  def __init__(self, *args, **kwargs) -> None:
    """Initializes the decorator."""
    self.__pos_args__ = args
    self.__key_args__ = kwargs

  def __call__(self, cls: type) -> type:
    """Returns a new class subclassing"""
    name = cls.__name__
    bases = (cls,)
    namespace = {**AttriClass.__dict__, '__pos_args__': self.__pos_args__,
                 '__key_args__'                       : self.__key_args__}
    return type(name, bases, namespace)
