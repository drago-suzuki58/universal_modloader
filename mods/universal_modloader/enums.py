from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class AtType(Enum):
    HEAD = auto()
    TAIL = auto()
    INVOKE = auto()
    RETURN = auto()
    ASSIGN = auto()
    FIELD = auto()


class Shift(Enum):
    BEFORE = auto()
    AFTER = auto()


@dataclass
class At:
    type: AtType
    target: Optional[str] = None
    shift: Shift = Shift.BEFORE
    ordinal: int = 0

    @staticmethod
    def HEAD():
        return At(AtType.HEAD)

    @staticmethod
    def TAIL():
        return At(AtType.TAIL)

    @staticmethod
    def INVOKE(target: str, shift: Shift = Shift.BEFORE, ordinal: int = 0):
        return At(AtType.INVOKE, target=target, shift=shift, ordinal=ordinal)

    @staticmethod
    def RETURN(shift: Shift = Shift.BEFORE):
        return At(AtType.RETURN, shift=shift)
