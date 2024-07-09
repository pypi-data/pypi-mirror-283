"""This module provides a test suite for the VistEnum class"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from attribox import AttriBox
from vistutils.text import stringList
from vistutils.waitaminute import typeMsg

from vistenum import VistEnum, auto


class RGB:
  """RGB provides a dataclass representation of colors"""
  red = AttriBox[int](255)
  green = AttriBox[int](255)
  blue = AttriBox[int](255)

  @staticmethod
  def int2Hex(value: int) -> str:
    """Converts an integer to a hexadecimal string"""
    return f'{value:02X}'

  def __init__(self, *args, **kwargs) -> None:
    redKeys = stringList("""red, RED, r, R""")
    greenKeys = stringList("""green, GREEN, g, G""")
    blueKeys = stringList("""blue, BLUE, b, B""")
    types = dict(red=int, green=int, blue=int)
    values = {}
    KEYS = [redKeys, greenKeys, blueKeys]
    posArgs = [*args, ]
    for (keys, (name, type_)) in zip(KEYS, types.items()):
      for key in keys:
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, type_):
            values[name] = kwargs[key]
            break
          e = typeMsg(key, val, type_)
          raise TypeError(e)
      else:
        frozenArgs = [*posArgs, ]
        posArgs = []
        for arg in frozenArgs:
          if isinstance(arg, type_) and name not in values:
            values[name] = arg
          else:
            posArgs.append(arg)
        else:
          pass
    self.red = values['red']
    self.green = values['green']
    self.blue = values['blue']

  def __eq__(self, other: RGB) -> bool:
    """Returns true if each channel has the same value"""
    diffSum = sum([
      (self.red - other.red) ** 2,
      (self.green - other.green) ** 2,
      (self.blue - other.blue) ** 2,
    ])
    return False if diffSum else True

  def __str__(self) -> str:
    """Returns a string representation of the color"""
    r = self.int2Hex(self.red)
    g = self.int2Hex(self.green)
    b = self.int2Hex(self.blue)
    return '#%s%s%s' % (r, g, b)


class NamedColors(VistEnum):
  """NamedColors provides an enumeration of colors"""
  RED = auto(RGB(red=255, green=0, blue=0))
  GREEN = auto(RGB(red=0, green=255, blue=0))
  BLUE = auto(RGB(red=0, green=0, blue=255))
  YELLOW = auto(RGB(red=255, green=255, blue=0))
  CYAN = auto(RGB(red=0, green=255, blue=255))
  MAGENTA = auto(RGB(red=255, green=0, blue=255))
  ORANGE = auto(RGB(red=255, green=165, blue=0))
  PURPLE = auto(RGB(red=128, green=0, blue=128))
  PINK = auto(RGB(red=255, green=192, blue=203))
  BROWN = auto(RGB(red=165, green=42, blue=42))
  WHITE = auto(RGB(red=255, green=255, blue=255))

  names = [
    'RED',
    'GREEN',
    'BLUE',
    'YELLOW',
    'CYAN',
    'MAGENTA',
    'ORANGE',
    'PURPLE',
    'PINK',
    'BROWN',
    'WHITE',
  ]


class TestVistEnum(TestCase):

  def test_access(self) -> None:
    """Enumerations should be accessible at the case-insensitive name at
    both the dot, the call and the index:"""
    self.assertEqual(NamedColors.RED, NamedColors('RED'))
    self.assertEqual(NamedColors.RED, NamedColors['RED'])

  def test_iteration(self) -> None:
    """Enumerations should be iterable"""
    colorNames = NamedColors.names
    for color in NamedColors:
      self.assertIn(color.name, colorNames)
      colorNames.remove(color.name)
    self.assertFalse(colorNames)

  def test_hashing(self) -> None:
    """Enumerations should be hashable"""
    hexDict = {
      NamedColors.RED    : '#FF0000',
      NamedColors.GREEN  : '#00FF00',
      NamedColors.BLUE   : '#0000FF',
      NamedColors.YELLOW : '#FFFF00',
      NamedColors.CYAN   : '#00FFFF',
      NamedColors.MAGENTA: '#FF00FF',
      NamedColors.ORANGE : '#FFA500',
      NamedColors.PURPLE : '#800080',
      NamedColors.PINK   : '#FFC0CB',
      NamedColors.BROWN  : '#A52A2A',
      NamedColors.WHITE  : '#FFFFFF',
    }
    self.assertEqual(hexDict[NamedColors.RED], '#FF0000')
    self.assertEqual(hexDict[NamedColors.GREEN], '#00FF00')
    self.assertEqual(hexDict[NamedColors.BLUE], '#0000FF')
    self.assertEqual(hexDict[NamedColors.YELLOW], '#FFFF00')
    self.assertEqual(hexDict[NamedColors.CYAN], '#00FFFF')
    self.assertEqual(hexDict[NamedColors.MAGENTA], '#FF00FF')
    self.assertEqual(hexDict[NamedColors.ORANGE], '#FFA500')
    self.assertEqual(hexDict[NamedColors.PURPLE], '#800080')
    self.assertEqual(hexDict[NamedColors.PINK], '#FFC0CB')
    self.assertEqual(hexDict[NamedColors.BROWN], '#A52A2A')
    self.assertEqual(hexDict[NamedColors.WHITE], '#FFFFFF')

  def test_includeValue(self) -> None:
    """Testing functionality of includeValue flag at runtime"""
    NamedColors.includeValue = True
    for color in NamedColors:
      self.assertIn(str(color.value), str(color))
    NamedColors.includeValue = False
    for color in NamedColors:
      self.assertNotIn(str(color.value), str(color))
