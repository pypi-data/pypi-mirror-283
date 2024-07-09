"""TestEnumBox tests the EnumBox class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from attribox import AttriBox

from vistenum import VistEnum, auto, EnumBox


class Position(VistEnum):
  """Position enumerates baseball positions."""
  PITCHER = auto('P')
  CATCHER = auto('C')
  FIRST_BASE = auto('1B')
  SECOND_BASE = auto('2B')
  THIRD_BASE = auto('3B')
  SHORT_STOP = auto('SS')
  LEFT_FIELD = auto('LF')
  CENTER_FIELD = auto('CF')
  RIGHT_FIELD = auto('RF')

  def __getattr__(self, key: str) -> object:
    if 'designated' in key.lower():
      raise SyntaxError("""Abolish the DH rule!""")
    return object.__getattribute__(self, key)


class BattingSide(VistEnum):
  """BattingSide enumerates left and right handed batters."""
  LEFT = auto()
  RIGHT = auto()
  SWITCH = auto()


class ThrowingSide(VistEnum):
  """ThrowingSide enumerates left and right handed throwers."""
  LEFT = auto()
  RIGHT = auto()


class AttackStage(VistEnum):
  """BatterStage enumerates the stages of a batter."""
  BENCH = auto()
  ON_DECK = auto()
  AT_BAT = auto()
  FIRST = auto()
  SECOND = auto()
  THIRD = auto()


class Player:
  """Player represents a baseball player."""

  name = AttriBox[str]('')
  number = AttriBox[int](0)
  position = EnumBox[Position]()
  battingSide = EnumBox[BattingSide]()
  throwingSide = EnumBox[ThrowingSide]()
  attackStage = EnumBox[AttackStage]()

  def __init__(self, *args, ) -> None:
    for arg in args:
      if isinstance(arg, str) and not self.name:
        self.name = arg
      elif isinstance(arg, int) and not self.number:
        self.number = arg
      elif isinstance(arg, Position):
        self.position = arg
      elif isinstance(arg, BattingSide):
        self.battingSide = arg
      elif isinstance(arg, ThrowingSide):
        self.throwingSide = arg
    self.attackStage = AttackStage.BENCH

  def __str__(self, ) -> str:
    """String representation"""
    pos = self.position.value
    bat = self.battingSide.value
    thr = self.throwingSide.value
    num = self.number
    name = self.name
    return """%d %s (%s, %s, %s)""" % (num, name, pos, bat, thr)


class TestEnumBox(TestCase):
  """TestEnumBox tests the EnumBox class. """

  zambrano = Player('Carlos Zambrano', 38, Position.PITCHER,
                    BattingSide.SWITCH, ThrowingSide.RIGHT)

  def test_enum_box(self, ) -> None:
    """Tests the EnumBox class."""
    self.assertEqual(self.zambrano.name, 'Carlos Zambrano')
    self.assertEqual(self.zambrano.number, 38)
    self.assertEqual(self.zambrano.position, Position.PITCHER)
    self.assertEqual(self.zambrano.battingSide, BattingSide.SWITCH)
    self.assertEqual(self.zambrano.throwingSide, ThrowingSide.RIGHT)
    self.assertEqual(str(self.zambrano),
                     '38 Carlos Zambrano (P, SWITCH, RIGHT)')
    self.assertEqual(self.zambrano.attackStage, AttackStage.BENCH)
    self.zambrano.attackStage = AttackStage.ON_DECK
    self.assertEqual(self.zambrano.attackStage, AttackStage.ON_DECK)
    self.zambrano.attackStage = AttackStage.AT_BAT
    self.assertEqual(self.zambrano.attackStage, AttackStage.AT_BAT)
    self.zambrano.attackStage = AttackStage.FIRST
    self.assertEqual(self.zambrano.attackStage, AttackStage.FIRST)
    self.zambrano.attackStage = AttackStage.SECOND
    self.assertEqual(self.zambrano.attackStage, AttackStage.SECOND)
    self.zambrano.attackStage = AttackStage.THIRD
    self.assertEqual(self.zambrano.attackStage, AttackStage.THIRD)
