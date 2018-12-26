from typing import NamedTuple

class BrushSignal(NamedTuple):
    vibrate:bool = False
    finalVibrate:bool = False
    visualSignal:bool = False
    finalVisualSignal:bool = False

    @staticmethod
    def fromInt(value:int)->'BrushSignal':
        return BrushSignal(
            vibrate = bool(value & 0x01),
            finalVibrate = bool(value & 0x02),
            visualSignal = bool(value & 0x04),
            finalVisualSignal = bool(value & 0x08)
        )

    def toInt(self)->int:
        value = 0
        if self.vibrate:
            value = value | 1
        if self.finalVibrate:
            value = value | 2
        if self.visualSignal:
            value = value | 4
        if self.finalVisualSignal:
            value = value | 8
        return value