"""The auto function indicates that the variable is meant to be an enum
object."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from vistenum import EnumObject


def auto(*args) -> object:
  """The auto function indicates that the variable is meant to be an enum
  object."""
  obj = EnumObject()
  obj.value = [*args, None][0]
  return obj
