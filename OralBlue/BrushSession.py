import struct
from datetime import datetime, timedelta
from typing import Optional

from OralBlue.BrushMode import BrushMode
from OralBlue.OralBDate import OralBDate


class BrushSession(object):

    def __init__(self,data:bytes,protocolVersion: int = 1):
        if len(data) != 16:
            raise ValueError

        self._startDate = OralBDate(data[0:4]).datetime

        durationS = struct.unpack("<H",data[4:6])[0]
        self._duration = timedelta(seconds=durationS)

        self._eventCount = data[6]

        self._prefMode = BrushMode(data[7])

        durationS = struct.unpack("<H", data[8:10])[0]
        self._timeUnderPressure = timedelta(seconds=durationS)

        self._nPressure= data[10]

        self._finalBatteryState = data[11]

        if(protocolVersion == 1):
            self._parseProtocolV1(data)
        elif protocolVersion == 2 or protocolVersion == 3:
            self._parseProtocolV2Or3(data)
        elif protocolVersion == 4:
            self._parseProtocolV4(data)

    def _parseProtocolV1(self, data: bytes):
        self._lastCharge = OralBDate(data[12:16]).datetime
        self._sessionId=-1
        self._userId =0
        self._sessionTargetTime = -1
        self._numberOfSectors=-1

    def _parseProtocolV2Or3(self, data: bytes):
        self._lastCharge = None
        temp = struct.unpack("<H", data[12:14])[0]
        self._sessionTargetTime = temp & 0x1FFF # 13 bits
        self._numberOfSectors = temp >> 13 # 3 bits
        temp = struct.unpack("<H", data[14:16])[0]
        self._sessionId = (temp ) & 0x1FFF  # 13 bits
        self._userId = temp >> 13 # 3 bits

    def _parseProtocolV4(self,data:bytes):
        self._parseProtocolV2Or3(data)
        durationMS = (struct.unpack("<H", data[8:10])[0])*100
        self._timeUnderPressure = timedelta(milliseconds=durationMS)

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

    @property
    def finalBatteryState(self)->int:
        return self._finalBatteryState

    @property
    def lastCharge(self)->Optional[timedelta]:
        return self._lastCharge

    @property
    def sessionId(self)->int:
        return self._sessionId

    @property
    def userId(self) -> int:
        return self._userId

    @property
    def numberOfSector(self) -> int:
        return self._numberOfSectors

    @property
    def sessionTargetTime(self) -> int:
        return self._sessionTargetTime


    def __str__(self):
        return "Start: {}\n\tDuration:{}\n\tMode:{}\n\tN pressure:{}\n\ttime underPressure:{}" \
               "\n\tbattery:{}\n\tlastCharge:{}\n\tSessionId:{}\n\tUserId:{}\n\tnSection:{}\n\t" \
               "sessionTargetTime:{}"\
            .format(self._startDate,
                    self.duration.total_seconds(),
                    self.prefMode,
                    self._nPressure,
                    self._timeUnderPressure,
                    self._finalBatteryState,
                    self._lastCharge,
                    self._sessionId,
                    self._userId,
                    self._numberOfSectors,
                    self._sessionTargetTime)