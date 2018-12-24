from enum import IntEnum


class BrushSector(IntEnum):
    SECTOR_1 = 0x00
    SECTOR_2 = 0x01
    SECTOR_3 = 0x02,
    SECTOR_4 = 0x03,
    SECTOR_5 = 0x04
    SECTOR_6 = 0x05
    SECTOR_7 = 0x07
    SECTOR_8 = 0x08
    LAST_SECTOR = 0xFE
    NO_SECTOR = 0xFF

    @classmethod
    def _missing_(cls, value):
        return BrushSector.NO_SECTOR
