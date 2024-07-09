"""EnumObject provides the object representation of an enumeration member."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from vistutils.fields import EmptyField
from vistutils.parse import maybe
from vistutils.text import monoSpace, stringList
from vistutils.waitaminute import typeMsg


class EnumObject:
  """EnumObject provides the object representation of an enumeration
  member."""

  __enum_name__ = None
  __public_value__ = None
  __private_value__ = None

  enumCls = EmptyField()
  name = EmptyField()
  value = EmptyField()

  @enumCls.GET
  def _getEnumCls(self) -> object:
    """Getter-function for the enum class."""
    return self.__class__

  @name.SET
  def _setName(self, name: str) -> None:
    """Setter-function for the name of the enum object."""
    if not isinstance(name, str):
      e = typeMsg('name', name, str)
      raise TypeError(e)
    if self.__enum_name__ is not None:
      e = """The name of the enum object has already been set to %s!"""
      raise AttributeError(monoSpace(e % self.__enum_name__))
    self.__enum_name__ = name

  @name.GET
  def _getName(self) -> str:
    """Getter-function for the name of the enum object."""
    if self.__enum_name__ is None:
      e = """The name of the enum object has not been set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__enum_name__, str):
      return self.__enum_name__
    e = typeMsg('name', self.__enum_name__, str)
    raise TypeError(e)

  @value.SET
  def _setValue(self, value: int) -> None:
    """Setter-function for the value of the enum object."""
    if self.__public_value__ is not None:
      e = """The value of the enum object has already been set to %s!"""
      raise AttributeError(monoSpace(e % self.__public_value__))
    self.__public_value__ = value

  @value.GET
  def _getValue(self) -> object:
    """Getter-function for the value of the enum object."""
    return maybe(self.__public_value__, self.__enum_name__)

  def _setPrivateValue(self, value: int) -> None:
    """Setter-function for the private value of the enum object."""
    if self.__private_value__ is not None:
      e = """The private value of the enum object has already been set to 
      %s!"""
      raise AttributeError(monoSpace(e % self.__private_value__))
    self.__private_value__ = value

  def _getPrivateValue(self) -> int:
    """Getter-function for private value"""
    if self.__private_value__ is None:
      e = """The private value of the enum object has not been set!"""
      raise AttributeError(monoSpace(e))
    if isinstance(self.__private_value__, int):
      return self.__private_value__
    e = typeMsg('__private_value__', self.__private_value__, int)
    raise TypeError(e)

  def __init__(self, *args, **kwargs) -> None:
    nameKeys = stringList("""name, enumName, title, enum_name""")
    publicValueKeys = stringList("""value, pubValue, publicValue, 
    pub_value, public_value""")
    privateValueKeys = stringList("""privateValue, pvtValue, pvt_value,
    private_value""")
    KEYS = [nameKeys, privateValueKeys, publicValueKeys, ]
    types = dict(name=str, private=int, public=object)
    values = {}
    posArgs = [*args, ]
    for (keys, (varName, varType)) in zip(KEYS, types.items()):
      for key in keys:
        if key in kwargs:
          val = kwargs[key]
          if isinstance(val, varType):
            values[varName] = val
            break
          e = typeMsg(key, val, varType)
          raise TypeError(e)
      else:
        frozenArgs = [*posArgs, ]
        posArgs = []
        for arg in frozenArgs:
          if isinstance(arg, varType) and varName not in values:
            values[varName] = arg
          else:
            posArgs.append(arg)
    if 'name' in values:
      self.name = values['name']
    if 'private' in values:
      self._setPrivateValue(values['private'])
    if 'public' in values:
      self.value = values['public']

  def __init_subclass__(cls, **kwargs) -> None:
    """Why are we still here? Just to suffer? Or raise errors?"""

  def __str__(self) -> str:
    """Returns the name of the enum object."""
    if TYPE_CHECKING:
      assert isinstance(self.name, str)
      assert hasattr(self.enumCls, 'includeValue')
    clsName = self.enumCls.__name__
    if self.enumCls.includeValue:
      return '%s.%s(%s)' % (clsName, self.name, str(self.value))
    return '%s.%s' % (clsName, self.name)

  def __repr__(self) -> str:
    """Returns the name of the enum object."""
    if TYPE_CHECKING:
      assert isinstance(self.name, str)
    clsName = self.__class__.__name__
    return '%s(%s)' % (clsName, self.name)

  def __eq__(self, other: object) -> bool:
    """Returns True if the other object is an enum object."""
    if TYPE_CHECKING:
      assert isinstance(self.name, str)
    if isinstance(other, EnumObject):
      return True if self.name == other.name else False
    if isinstance(other, str):
      if self.name.lower() == other.lower():
        return True
    if isinstance(other, int):
      if self._getPrivateValue() == other:
        return True
    return False

  def __hash__(self, ) -> int:
    """Returns the hash of the enum object."""
    if TYPE_CHECKING:
      assert isinstance(self.name, str)
    return hash(self.name)
