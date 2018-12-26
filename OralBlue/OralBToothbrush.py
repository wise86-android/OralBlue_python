import struct
from datetime import datetime, timedelta
from typing import Callable, Iterable, Optional, NamedTuple

from bluepy.btle import Peripheral, UUID, Characteristic, DefaultDelegate

from OralBlue.BrushBattery import BrushBattery
from OralBlue.BrushInfo import BrushInfo
from OralBlue.BrushMode import BrushMode
from OralBlue.BrushSector import BrushSector
from OralBlue.BrushSession import BrushSession
from OralBlue.BrushSignal import BrushSignal
from OralBlue.BrushState import BrushState
from OralBlue.OralBDate import OralBDate


class OralBButtonStatus(NamedTuple):
    powerButtonPressed: bool = False
    modeButtonPressed: bool = False

#todo add sensor data
#todo set signal not working?
class OralBToothbrush(Peripheral, DefaultDelegate):
    _TOOTHBRUSH_ID_TIME_CHAR = UUID("a0f0ff01-5047-4d53-8208-4f72616c2d42")
    _MODEL_ID_CHAR = UUID("a0f0ff02-5047-4d53-8208-4f72616c2d42")
    _USER_ID_CHAR = UUID("a0f0ff03-5047-4d53-8208-4f72616c2d42")
    _STATUS_CHAR = UUID("a0f0ff04-5047-4d53-8208-4f72616c2d42")
    _BATTERY_CHAR = UUID("a0f0ff05-5047-4d53-8208-4f72616c2d42")
    _BUTTON_CHAR = UUID("a0f0ff06-5047-4d53-8208-4f72616c2d42")
    _MODE_CHAR = UUID("a0f0ff07-5047-4d53-8208-4f72616c2d42")
    _BRUSING_TIME_CHAR = UUID("a0f0ff08-5047-4d53-8208-4f72616c2d42")
    _CURRENT_SECTOR_CHAR = UUID("a0f0ff09-5047-4d53-8208-4f72616c2d42")
    _CONTROL_CHAR = UUID("a0f0ff21-5047-4d53-8208-4f72616c2d42")
    _CURRENT_DATE_CHAR = UUID("a0f0ff22-5047-4d53-8208-4f72616c2d42")
    _SIGNAL_CHAR = UUID("a0f0ff24-5047-4d53-8208-4f72616c2d42")
    _AVAILABLE_MODES_CHAR = UUID("a0f0ff25-5047-4d53-8208-4f72616c2d42")
    _SECTOR_TIME_CHAR = UUID("a0f0ff26-5047-4d53-8208-4f72616c2d42")
    _SESSION_INFO_CHAR = UUID("a0f0ff29-5047-4d53-8208-4f72616c2d42")

    BatteryStatusCallback = Callable[[BrushBattery], None]
    BrushingTimeCallback = Callable[[int], None]
    BrushStateCallback = Callable[[BrushState], None]
    BrushModeCallback = Callable[[BrushMode], None]
    BrushButtonCallback = Callable[[OralBButtonStatus], None]
    BrushCurrentSectorCallback = Callable[[BrushSector], None]

    def handleNotification(self, cHandle, data):
        print("notify {} -> {}", cHandle, data)
        if cHandle in self._callbackMap:
            self._callbackMap[cHandle](data)

    @staticmethod
    def _findChar(uuid: UUID, chars: Iterable[Characteristic]) -> Optional[Characteristic]:
        results = filter(lambda x: x.uuid == uuid, chars)
        for result in results:  # return the first match
            return result
        return None

    def __init__(self, address: str, protocolVersion: int = 1):
        super().__init__(address)
        self._protocolVersion = protocolVersion
        self.withDelegate(self)
        allChars = self.getCharacteristics()
        self._batteryChar = OralBToothbrush._findChar(OralBToothbrush._BATTERY_CHAR, allChars)
        self._brushingTimeChar = OralBToothbrush._findChar(OralBToothbrush._BRUSING_TIME_CHAR, allChars)
        self._statusChar = OralBToothbrush._findChar(OralBToothbrush._STATUS_CHAR, allChars)
        self._modeChar = OralBToothbrush._findChar(OralBToothbrush._MODE_CHAR, allChars)
        self._modelIdChar = OralBToothbrush._findChar(OralBToothbrush._MODEL_ID_CHAR, allChars)
        self._controlChar = OralBToothbrush._findChar(OralBToothbrush._CONTROL_CHAR, allChars)
        self._currentDateChar = OralBToothbrush._findChar(OralBToothbrush._CURRENT_DATE_CHAR, allChars)
        self._availableModesChar = OralBToothbrush._findChar(OralBToothbrush._AVAILABLE_MODES_CHAR, allChars)
        self._sessionInfoChar = OralBToothbrush._findChar(OralBToothbrush._SESSION_INFO_CHAR, allChars)
        self._signalChar = OralBToothbrush._findChar(OralBToothbrush._SIGNAL_CHAR, allChars)
        self._buttonChar = OralBToothbrush._findChar(OralBToothbrush._BUTTON_CHAR, allChars)
        self._currentSectorChar = OralBToothbrush._findChar(OralBToothbrush._CURRENT_SECTOR_CHAR, allChars)
        self._sectorTimeChar = OralBToothbrush._findChar(OralBToothbrush._SECTOR_TIME_CHAR, allChars)
        self._userIdChar = OralBToothbrush._findChar(OralBToothbrush._USER_ID_CHAR, allChars)
        self._toothbrushIdChar = OralBToothbrush._findChar(OralBToothbrush._TOOTHBRUSH_ID_TIME_CHAR, allChars)
        self._callbackMap = {}

    def _writeCharDescriptor(self, characteristic: Characteristic, data):
        notify_handle = characteristic.getHandle() + 1
        self.writeCharacteristic(notify_handle, data, withResponse=True)

    def _enableNotification(self, characteristic: Characteristic):
        if not (characteristic.properties & Characteristic.props["NOTIFY"]):
            return
        self._writeCharDescriptor(characteristic, b"\x01\x00")

    def _disableNotification(self, characteristic: Characteristic):
        self._writeCharDescriptor(characteristic, b"\x00\x00")

    def _registerCallback(self, characteristic: Characteristic, callback: Callable):
        handle = characteristic.getHandle()
        self._callbackMap[handle] = callback
        self._enableNotification(characteristic)

    def _removeCallback(self, characteristic: Characteristic):
        handle = characteristic.getHandle()
        del self._callbackMap[handle]
        self._disableNotification(characteristic)

    @staticmethod
    def _parseBatteryStatysResponse(data) -> BrushBattery:
        if len(data) >= 3:
            remainingSec = struct.unpack("<H",data[1:3])[0]
            return BrushBattery(level=data[0],remainingSec=timedelta(seconds=remainingSec))
        else:
            return BrushBattery(level=data[0])

    @staticmethod
    def _parseBrushingTimeResponse(data) -> int:
        return int(data[0]) * 60 + int(data[1])

    @staticmethod
    def _parseBrushStateResponse(data) -> BrushState:
        return BrushState(data[0])

    @staticmethod
    def _parseBrushModeResponse(data) -> BrushMode:
        return BrushMode(data[0])

    @staticmethod
    def _parseButtonStateResponse(data) -> OralBButtonStatus:
        return OralBButtonStatus(
            powerButtonPressed=bool(data[0]),
            modeButtonPressed=bool(data[1])
        )

    def readModelId(self) ->BrushInfo:
        data = self._modelIdChar.read()
        if len(data) == 3:
            return BrushInfo(type=data[0],protocolVersion=data[1],fwversion=data[2])
        else:
            return BrushInfo(type=data[0])

    def readBatteryStatus(self)->BrushBattery:
        data = self._batteryChar.read()
        return OralBToothbrush._parseBatteryStatysResponse(data)

    def setBatteryUpdateCallback(self, callback: Optional[BatteryStatusCallback]):
        if callback is None:
            self._removeCallback(self._batteryChar)
        else:
            self._registerCallback(self._batteryChar,
                                   lambda data: callback(OralBToothbrush._parseBatteryStatysResponse(data)))

    def readBrushingTime(self) -> int:
        data = self._brushingTimeChar.read()
        return OralBToothbrush._parseBrushingTimeResponse(data)

    def setBrushingTimeUpdateCallback(self, callback: Optional[BrushingTimeCallback]):
        if callback is None:
            self._removeCallback(self._brushingTimeChar)
        else:
            self._registerCallback(self._brushingTimeChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushingTimeResponse(data)))

    def readBrushState(self) -> BrushState:
        data = self._statusChar.read()
        return OralBToothbrush._parseBrushStateResponse(data)

    def setBrushStateUpdateCallback(self, callback: Optional[BrushStateCallback]):
        if callback is None:
            self._removeCallback(self._statusChar)
        else:
            self._registerCallback(self._statusChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushStateResponse(data)))

    def setBrushButtonPressedCallback(self, callback: Optional[BrushButtonCallback]):
        if callback is None:
            self._removeCallback(self._buttonChar)
        else:
            self._registerCallback(self._buttonChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseButtonStateResponse(data)))

    def setBrushCurrentSectorCallback(self, callback: Optional[BrushCurrentSectorCallback]):
        if callback is None:
            self._removeCallback(self._currentSectorChar)
        else:
            self._registerCallback(self._currentSectorChar,
                                   lambda data: callback(BrushSector(data[0])))

    def readBrushMode(self) -> BrushMode:
        data = self._modeChar.read()
        return OralBToothbrush._parseBrushModeResponse(data)

    def setBrushModeUpdateCallback(self, callback: Optional[BrushModeCallback]):
        if callback is None:
            self._removeCallback(self._modeChar)
        else:
            self._registerCallback(self._modeChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushModeResponse(data)))

    def _writeControl(self, commandId: int, param: int):
        data = bytearray(2)
        data[0] = commandId
        data[1] = param
        self._controlChar.write(data)

    def readCurrentTime(self) -> datetime:
        # self._writeControl(0x01,0x00) #seemsnot needed...
        rawSecAfter2000 = self._currentDateChar.read()
        return OralBDate(rawSecAfter2000).datetime

    def setCurrentTime(self, now=datetime.now()):
        self._writeControl(0x37, 0x26)
        date = OralBDate.fromDatetime(now)
        self._currentDateChar.write(date.toBytes())

    def readAvailableModes(self) -> [BrushMode]:
        rawModes = self._availableModesChar.read()
        return [BrushMode(mode) for mode in rawModes]

    def writeAvailableModes(self, newOrder: [BrushMode]):
        self._writeControl(0x37, 0x29)
        rawData = bytearray(8)
        nMode = len(newOrder)
        rawData[0:nMode] = [mode.value for mode in newOrder]
        self._availableModesChar.write(rawData)

    def _nAvailableSessions(self) -> int:
        if 2 <= self._protocolVersion <= 4:
            return 30
        else:
            return 20

    def readSession(self) -> [BrushSession]:
        session = []
        for i in range(0, self._nAvailableSessions()):
            self._writeControl(2, i)
            data = self._sessionInfoChar.read()
            session.append(BrushSession(data,self._protocolVersion))
        return session

    def readSignalStatus(self) -> BrushSignal:
        rawData = self._signalChar.read()
        return BrushSignal.fromInt(rawData)

    def writeSignalStatus(self, newStatus: BrushSignal):
        self._writeControl(0x37, 0x28)
        rawData = struct.pack("I",newStatus.toInt())
        self._signalChar.write(rawData)

    def readSectorTimer(self) -> [int]:
        rawData = self._sectorTimeChar.read()
        nSector = len(rawData) >> 1  # /2
        return struct.unpack("<" + "H" * nSector, rawData)

    def setSectorTimer(self, time: [int]):
        missingValue = 8 - len(time)
        print(missingValue)
        time += [0] * missingValue
        print(time)
        rawTime = struct.pack("<" + "H" * 8, *time)
        self._writeControl(0x37, 0x2A)
        self._sectorTimeChar.write(rawTime)

    def gerUserId(self) -> int:
        return self._userIdChar.read()[0]

    def setUserId(self, newId: int):
        rawTime = struct.pack("B", newId)
        self._userIdChar.write(rawTime)

    def readToothbrushId(self) -> int:
        rawData = self._toothbrushIdChar.read()
        return struct.unpack("<I", rawData[0:4])[0]
