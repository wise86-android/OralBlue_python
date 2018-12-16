import struct
from datetime import timedelta, datetime
from typing import Callable, Iterable, Optional

from bluepy.btle import Peripheral, UUID, Characteristic, DefaultDelegate

from OralBlue.BrushMode import BrushMode
from OralBlue.BrushState import BrushState


class OralBToothbrush(Peripheral, DefaultDelegate):
    _MODEL_ID_CHAR = UUID("a0f0ff02-5047-4d53-8208-4f72616c2d42")
    _STATUS_CHAR = UUID("a0f0ff04-5047-4d53-8208-4f72616c2d42")
    _BATTERY_CHAR = UUID("a0f0ff05-5047-4d53-8208-4f72616c2d42")
    _MODE_CHAR = UUID("a0f0ff07-5047-4d53-8208-4f72616c2d42")
    _BRUSING_TIME_CHAR = UUID("a0f0ff08-5047-4d53-8208-4f72616c2d42")
    _CONTROL_CHAR = UUID("a0f0ff21-5047-4d53-8208-4f72616c2d42")
    _CURRENT_DATE_CHAR = UUID("a0f0ff22-5047-4d53-8208-4f72616c2d42")
    _AVAILABLE_MODES_CHAR = UUID("a0f0ff25-5047-4d53-8208-4f72616c2d42")


    BatteryStatusCallback = Callable[[int], None]
    BrushingTimeCallback = Callable[[int], None]
    BrushStateCallback = Callable[[BrushState], None]
    BrushModeCallback = Callable[[BrushMode], None]


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

    def __init__(self, address: str):
        super().__init__(address)
        self.withDelegate(self)
        allChars = self.getCharacteristics()
        self._batteryChar = OralBToothbrush._findChar(OralBToothbrush._BATTERY_CHAR, allChars)
        self._brushingTimeChar = OralBToothbrush._findChar(OralBToothbrush._BRUSING_TIME_CHAR, allChars)
        self._statusChar = OralBToothbrush._findChar(OralBToothbrush._STATUS_CHAR, allChars)
        self._modeChar = OralBToothbrush._findChar(OralBToothbrush._MODE_CHAR, allChars)
        self._modelIdChar = OralBToothbrush._findChar(OralBToothbrush._MODEL_ID_CHAR, allChars)
        self._controlChar = OralBToothbrush._findChar(OralBToothbrush._CONTROL_CHAR,allChars)
        self._currentDateChar = OralBToothbrush._findChar(OralBToothbrush._CURRENT_DATE_CHAR, allChars)
        self._availableModes = OralBToothbrush._findChar(OralBToothbrush._AVAILABLE_MODES_CHAR, allChars)
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
    def _parseBatteryStatysResponse(data) -> int:
        return int(data[0])

    @staticmethod
    def _parseBrushingTimeResponse(data) -> int:
        return int(data[0]) * 60 + int(data[1])

    @staticmethod
    def _parseBrushStateResponse(data) -> BrushState:
        return BrushState(data[0])

    @staticmethod
    def _parseBrushModeResponse(data) -> BrushMode:
        return BrushMode(data[0])

    def readModelId(self):
        data = self._modelIdChar.read()
        return data[0]

    def readBatteryStatus(self, onRead: BatteryStatusCallback):
        if self._batteryChar is None:
            return
        data = self._batteryChar.read()
        onRead(OralBToothbrush._parseBatteryStatysResponse(data))

    def setBatteryUpdateCallback(self, callback: Optional[BatteryStatusCallback]):
        if callback is None:
            self._removeCallback(self._batteryChar)
        else:
            self._registerCallback(self._batteryChar,
                                   lambda data: callback(OralBToothbrush._parseBatteryStatysResponse(data)))

    def readBrushingTime(self, onRead: BrushingTimeCallback):
        if self._brushingTimeChar is None:
            return
        data = self._statusChar.read()
        onRead(OralBToothbrush._parseBrushingTimeResponse(data))

    def setBrushingTimeUpdateCallback(self, callback: Optional[BrushingTimeCallback]):
        if callback is None:
            self._removeCallback(self._statusChar)
        else:
            self._registerCallback(self._statusChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushingTimeResponse(data)))

    def readBrushState(self, onRead: BrushStateCallback):
        if self._statusChar is None:
            return
        data = self._statusChar.read()
        onRead(OralBToothbrush._parseBrushStateResponse(data))

    def setBrushStateUpdateCallback(self, callback: Optional[BrushStateCallback]):
        if callback is None:
            self._removeCallback(self._statusChar)
        else:
            self._registerCallback(self._statusChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushStateResponse(data)))

    def readBrushMode(self, onRead: BrushModeCallback):
        if self._modeChar is None:
            return
        data = self._modeChar.read()
        onRead(OralBToothbrush._parseBrushModeResponse(data))

    def setBrushModeUpdateCallback(self, callback: Optional[BrushModeCallback]):
        if callback is None:
            self._removeCallback(self._modeChar)
        else:
            self._registerCallback(self._modeChar,
                                   lambda data: callback(
                                       OralBToothbrush._parseBrushModeResponse(data)))

    def _writeControl(self,commandId:int,param:int):
        data = bytearray(2)
        data[0] = commandId
        data[1] = param
        self._controlChar.write(data)

    def readCurrentTime(self) ->datetime:
        #self._writeControl(0x01,0x00) #seemsnot needed...
        rawSecAfter2000 = self._currentDateChar.read()
        print(rawSecAfter2000)
        secAfter2000 = struct.unpack("<I", rawSecAfter2000)[0]
        print(secAfter2000)
        delta = timedelta(seconds = secAfter2000)
        return datetime(year=2000,month=1,day=1) + delta

    def setCurrentTime(self,now = datetime.now()):
        self._writeControl(0x37,38)
        base = datetime(year=2000,month=1,day=1)
        secAfter2000 = (now - base).total_seconds()
        print(secAfter2000)
        rawSecAfter2000 = struct.pack("<I",int(secAfter2000))
        print(rawSecAfter2000)
        self._currentDateChar.write(rawSecAfter2000)

    def readAvailableModes(self)->[BrushMode]:
        rawModes = self._availableModes.read()
        return [BrushMode(mode) for mode in rawModes]

    def writeAvailableModes(self,newOrder:[BrushMode]):
        self._writeControl(0x37,0x29)
        rawData = bytearray(8)
        nMode = len(newOrder)
        rawData[0:nMode] = [mode.value for mode in newOrder]
        print(rawData)
        self._availableModes.write(rawData)