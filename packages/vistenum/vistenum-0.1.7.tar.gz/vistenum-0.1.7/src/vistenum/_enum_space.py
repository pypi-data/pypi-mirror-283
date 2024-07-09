"""EnumSpace provides the namespace object for the VistEnum derived
classes"""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from vistutils.metas import BaseNamespace
from vistutils.parse import maybe

from vistenum import EnumObject

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from vistenum import VistEnum


class EnumSpace(BaseNamespace):
  """EnumSpace provides the namespace object for the VistEnum derived
  classes"""

  __enum_members__ = None
  __special_members__ = None

  def getMetaclass(self, ) -> VistEnum:
    """Getter-function for the metaclass"""
    mcls = BaseNamespace.getMetaclass(self)
    if TYPE_CHECKING:
      assert isinstance(mcls, VistEnum)
    return mcls

  def __setitem__(self, key: str, value: object) -> None:
    """Set the value of the key in the namespace."""
    mcls = self.getMetaclass()
    if key in mcls.getSpecialNames():
      existing = maybe(self.__special_members__, {})
      self.__special_members__ = {**existing, key: value}
      return
    if not isinstance(value, EnumObject):
      return BaseNamespace.__setitem__(self, key, value)
    existing = maybe(self.__enum_members__, [])
    for item in existing:
      if item.name == key:
        e = """The enum object with the name %s already exists!"""
        raise AttributeError(e % key)
    value.name = key
    self.__enum_members__ = [*existing, value]

  def getMembers(self, ) -> list[EnumObject]:
    """Getter-function for the enum members"""
    return maybe(self.__enum_members__, [])

  def getSpecialMembers(self, ) -> dict[str, object]:
    """Getter-function for the special members"""
    return maybe(self.__special_members__, {})
