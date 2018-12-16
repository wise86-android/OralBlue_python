import struct
from datetime import timedelta, datetime


class OralBDate(object):
    _BASEDATE = datetime(year=2000, month=1, day=1)

    def __init__(self, data: bytes):
        if len(data) != 4:
            raise ValueError
        secAfter2000 = struct.unpack("<I", data)[0]
        delta = timedelta(seconds=secAfter2000)
        self._datetime = self._BASEDATE + delta

    @property
    def datetime(self):
        return self._datetime

    def toBytes(self)->bytes:
        return OralBDate._toBytes(self.datetime)

    @staticmethod
    def _toBytes(date:datetime)->bytes:
        secAfter2000 = (date - OralBDate._BASEDATE).total_seconds()
        return struct.pack("<I", int(secAfter2000))

    @staticmethod
    def fromDatetime(date: datetime)->'OralBDate':
        return OralBDate(OralBDate._toBytes(date))
