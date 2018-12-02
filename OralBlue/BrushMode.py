from enum import IntEnum


class BrushMode(IntEnum):
    OFF = 0x00
    DAILY_CLEAN = 0x01
    SENSITIVE = 0x02
    MASSAGE = 0x03
    WHITENING = 0x04
    DEEP_CLEAN = 0x05
    TONGUE_CLEANING = 0x06
    TURBO = 0x07
    UNKNOWN = 0xFF

    @classmethod
    def _missing_(cls, value):
        return BrushMode.UNKNOWN
