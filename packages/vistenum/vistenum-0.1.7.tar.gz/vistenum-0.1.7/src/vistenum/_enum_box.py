"""EnumBox provides a container for the VistEnum classes implementing the
same functionality as the AttriBox class. Because the VistEnum instances
are created along with the VistEnum subclasses themselves, the EnumBox
is substantially simpler to implement that the AttriBox class. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import Never

from attribox import AttriClass, AbstractDescriptor
from vistutils.fields import EmptyField
from vistutils.waitaminute import typeMsg

from vistenum import VistEnuMeta, VistEnum


class EnumBox(AbstractDescriptor):
  """EnumBox provides a container for the VistEnum classes implementing the
  same functionality as the AttriBox class. Because the VistEnum instances
  are created along with the VistEnum subclasses themselves, the EnumBox
  is substantially simpler to implement that the AttriBox class. """

  __enum_class__ = None
  __default_enum__ = None

  def _getEnumClass(self) -> VistEnuMeta:
    """Returns the inner enum class. """
    if self.__enum_class__ is None:
      e = """The inner enum class has not been assigned. """
      raise AttributeError(e)
    if isinstance(self.__enum_class__, VistEnuMeta):
      return self.__enum_class__
    e = typeMsg('__inner_enum_class__', self.__enum_class__, VistEnuMeta)
    raise TypeError(e)

  def _setEnumClass(self, cls: VistEnuMeta) -> None:
    """Sets the inner enum class. """
    if self.__enum_class__ is not None:
      e = """The inner enum class has already been assigned. """
      raise AttributeError(e)
    if not isinstance(cls, VistEnuMeta):
      e = typeMsg('innerEnumClass', cls, VistEnuMeta)
      raise TypeError(e)
    self.__enum_class__ = cls

  def _getDefaultEnum(self) -> object:
    """Returns the default enum instance. """
    if self.__default_enum__ is None:
      e = """The default enum instance has not been assigned. """
      raise AttributeError(e)
    if isinstance(type(self.__default_enum__), VistEnuMeta):
      return self.__default_enum__
    e = typeMsg('__default_enum__', type(self.__default_enum__), VistEnuMeta)
    raise TypeError(e)

  def _setDefaultEnum(self, defVal: object) -> None:
    """Sets the default enum instance. """
    if self.__default_enum__ is not None:
      e = """The default enum instance has already been assigned. """
      raise AttributeError(e)
    if not isinstance(type(defVal), VistEnuMeta):
      e = typeMsg('defaultEnum', type(defVal), VistEnuMeta)
      raise TypeError(e)
    self.__default_enum__ = defVal

  def __instance_get__(self, *_) -> Never:
    """EnumBox does not use the __instance_get__. """
    e = """'EnumBox' object has no attribute '__instance_get__'"""
    raise AttributeError(e)

  def __get__(self, instance: object, owner: type) -> object:
    """Returns the inner enum instance. """
    if instance is None:
      return self._getEnumClass()
    pvtName = self._getPrivateName()
    return getattr(instance, pvtName, self._getDefaultEnum())

  def __set__(self, instance: object, value: object) -> None:
    """Sets the inner enum instance. """
    cls = self._getEnumClass()
    if not isinstance(value, cls):
      e = typeMsg('value', value, cls)
      raise TypeError(e)
    pvtName = self._getPrivateName()
    setattr(instance, pvtName, value)

  def __delete__(self, instance: object) -> Never:
    """EnumBox does not implement deletion. """
    raise TypeError("""EnumBox does not implement deletion. """)

  @classmethod
  def __class_getitem__(cls, item) -> EnumBox:
    """Syntactic sugar for setting the inner enum class. """
    if not isinstance(item, VistEnuMeta):
      e = typeMsg('item', item, VistEnuMeta)
      raise TypeError(e)
    box = EnumBox()
    box._setEnumClass(item)
    return box

  def __call__(self, *args) -> EnumBox:
    """Syntactic sugar for setting the default enum instance. """
    cls = self._getEnumClass()
    defVal = cls(*args, 0)
    if isinstance(type(defVal), VistEnuMeta):
      self._setDefaultEnum(defVal)
      return self
    e = typeMsg('defaultEnum', type(defVal), VistEnuMeta)
    raise TypeError(e)
