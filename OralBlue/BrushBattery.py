from datetime import timedelta
from typing import NamedTuple

class BrushBattery(NamedTuple):
    level:int
    remainingSec:timedelta = None
