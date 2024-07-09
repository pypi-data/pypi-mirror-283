"""The VistEnuMeta class is the base class for enum classes."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

import sys

from attribox import AttriBox
from vistutils.metas import Bases, AbstractMetaclass
from vistutils.parse import maybe
from vistutils.text import monoSpace
from vistutils.waitaminute import typeMsg

from vistenum import EnumObject
from vistenum._enum_space import EnumSpace

from typing import TYPE_CHECKING

if sys.version_info.minor < 11:
  from typing_extensions import Self
else:
  from typing import Self


class _Flag:
  """Alternative to bool"""
  __inner_state__ = None

  def __init__(self, *args, **kwargs) -> None:
    if len(args) > 1:
      self.__inner_state__ = True
    elif len(args) == 1:
      self.__inner_state__ = True if args[0] else False
    else:
      self.__inner_state__ = False

  def __bool__(self, ) -> bool:
    return True if self.__inner_state__ else False

  def __int__(self) -> int:
    return 1 if self.__inner_state__ else 0

  def __str__(self) -> str:
    return 'True' if self else 'False'

  def __repr__(self) -> str:
    return 'True' if self else 'False'


class VistEnuMeta(AbstractMetaclass):
  """VistEnuMeta is the base class for enum classes."""

  __allow_instantiation__ = True
  __iter_contents__ = None
  __enum_instances__ = None
  __special_names__ = ['includeValue']

  includeValue = AttriBox[_Flag](False)

  @classmethod
  def getSpecialNames(mcls) -> list[str]:
    """Returns the special names of the class."""
    return mcls.__special_names__

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases, **kwargs) -> EnumSpace:
    """An instance of VistEnumNamespace is used by classes derived from
    VistEnum."""
    return EnumSpace(mcls, name, bases, **kwargs)

  def __new__(mcls,
              name: str,
              bases: Bases,
              enumSpace: EnumSpace,
              **kwargs) -> type:
    """The 'VistEnum' class is created by the metaclass."""
    bases = (EnumObject,)
    namespace = enumSpace.compile()
    specialMembers = enumSpace.getSpecialMembers()
    cls = type.__new__(mcls, name, bases, namespace, **kwargs)
    if 'includeValue' in specialMembers:
      cls.includeValue = specialMembers['includeValue']
    setattr(cls, '__allow_instantiation__', True)
    members = enumSpace.getMembers()
    for (i, member) in enumerate(members):
      instance = cls(name=member.name, value=member.value, pvtValue=i)
      setattr(cls, member.name, instance)
      existing = maybe(cls.__enum_instances__, [])
      cls.__enum_instances__ = [*existing, instance]
    setattr(cls, '__allow_instantiation__', False)
    return cls

  def __call__(cls, *args, **kwargs) -> object:
    """The allow instantiation flag determines if an instance is to be
    created, or an existing instance is to be returned."""
    if getattr(cls, '__allow_instantiation__'):
      return super().__call__(*args, **kwargs)
    return cls._recognizeMember(*args)

  def getInstances(cls) -> list[EnumObject]:
    """Returns a list of the instances of the enumeration."""
    return maybe(cls.__enum_instances__, [])

  def __iter__(cls, ) -> Self:
    """Returns the iterator for the enumeration."""
    cls.__iter_contents__ = [*cls.getInstances(), ]
    return cls

  def __next__(cls, ) -> EnumObject:
    """Returns the next instance of the enumeration."""
    if cls.__iter_contents__:
      return cls.__iter_contents__.pop(0)
    cls.__iter_contents__ = None
    raise StopIteration

  def __contains__(cls, item: object) -> bool:
    """Returns True if the item is an instance of the enumeration."""
    for instance in cls.getInstances():
      if instance == item:
        return True
    return False

  def _recognizeIndex(cls, index: int) -> EnumObject:
    """Returns the instance of the enumeration."""
    instances = cls.getInstances()
    while index < 0:
      index += len(instances)
    if index < len(instances):
      return instances[index]
    e = """The index: '%d' is out of range for the enumeration: '%s'."""
    raise IndexError(e % (index, cls.__name__))

  def _recognizeKey(cls, key: str) -> EnumObject:
    """Returns the instance of the enumeration."""
    instances = cls.getInstances()
    for instance in instances:
      if instance.name.lower() == key.lower():
        return instance
    try:
      e = """The key: '%s' is not a valid key for the enumeration: '%s'."""
      raise KeyError(e % (key, cls.__name__))
    except KeyError as keyError:
      try:
        getattr(cls, key)
      except AttributeError as attributeError:
        raise attributeError from keyError

  def _recognizeMember(cls, *args) -> EnumObject:
    """Returns the instance of the enumeration."""
    if not args:
      e = """Received no arguments!"""
      raise ValueError(e)
    enumObject = None
    for arg in args:
      if isinstance(arg, EnumObject):
        if isinstance(arg, cls):
          if TYPE_CHECKING:
            assert isinstance(arg, EnumObject)
          return arg
        enumObject = arg
      if isinstance(arg, int):
        return cls._recognizeIndex(arg)
      if isinstance(arg, str):
        return cls._recognizeKey(arg)
    if enumObject is not None:
      e = """The enum object: '%s' is not a member of the enumeration: 
      '%s'."""
      raise TypeError(monoSpace(e % (enumObject.name, cls.__name__)))
    e = typeMsg('index', args[0], int)
    raise TypeError(e)

  def __getitem__(cls, *args) -> EnumObject:
    """Returns the instance of the enumeration."""
    return cls._recognizeMember(*args)

  def __getattr__(cls, key: str) -> EnumObject:
    """Returns the instance of the enumeration."""
    try:
      return cls._recognizeKey(key)
    except Exception as exception:
      if isinstance(exception, AttributeError):
        e = str(exception).replace('_VistEnum', cls.__name__)
        raise AttributeError(e)
      try:
        return object.__getattribute__(cls, key)
      except AttributeError as attributeError:
        e = str(attributeError).replace('_VistEnum', cls.__name__)
        raise AttributeError(e) from exception

  def __str__(cls) -> str:
    """Returns the name of the enumeration."""
    return cls.__name__

  def __repr__(cls) -> str:
    """Returns the name of the enumeration."""
    return cls.__name__

  def __instancecheck__(cls, instance) -> bool:
    """Returns True if the instance is an instance of the enumeration."""
    if issubclass(type(instance), cls):
      return True
    return False


class VistEnum(metaclass=VistEnuMeta):
  """The VistEnum class is the base class for enum classes."""
  pass
