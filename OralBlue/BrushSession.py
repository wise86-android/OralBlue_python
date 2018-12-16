import struct
from datetime import datetime, timedelta

from OralBlue.BrushMode import BrushMode
from OralBlue.OralBDate import OralBDate


class BrushSession(object):

    def __init__(self,data:bytes):
        if len(data) != 16:
            raise ValueError

        self._startDate = OralBDate(data[0:4]).datetime

        durationS = struct.unpack("<H",data[4:6])[0]
        self._duration = timedelta(seconds=durationS)

        #data[6] unknown

        self._prefMode = BrushMode(data[7])

        durationS = struct.unpack("<H", data[8:10])[0]
        self._timeUnderPressure = timedelta(seconds=durationS)

        self._nPressure= data[10]

    @property
    def startDate(self)->datetime:
        return self._startDate

    @property
    def duration(self) -> timedelta:
        return self._duration

    @property
    def prefMode(self)->BrushMode:
        return self._prefMode

    @property
    def nPressure(self)->int:
        return self._nPressure

    @property
    def timeUnderPressure(self)->timedelta:
        return self._timeUnderPressure

    def __str__(self):
        return "Start: {}\n\tDuration:{}\n\tMode:{}\n\tN pressure:{}\n\ttime underPressure:{}"\
            .format(self._startDate,
                    self.duration.total_seconds(),
                    self.prefMode,
                    self._nPressure,
                    self._timeUnderPressure)