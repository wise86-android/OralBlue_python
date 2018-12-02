from enum import IntEnum


class BrushState(IntEnum):
    UNKNOWN = 0x00
    INIT = 0x01
    IDLE = 0x02
    RUN = 0x03
    CHARGE = 0x4
    SETUP = 0x05
    FLIGHT_MENU = 0x06
    FINAL_TEST = 0x71
    PCB_TEST = 0x72
    SLEEP = 0x73
    TRANSPORT = 0x74

    @classmethod
    def _missing_(cls, value):
        return BrushState.UNKNOWN
