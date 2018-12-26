# import the necessary parts of the bluepy library
from datetime import datetime

from bluepy.btle import BTLEException

from OralBlue.BrushBattery import BrushBattery
from OralBlue.OralBToothbrush import OralBToothbrush

if __name__ == '__main__':
    device = OralBToothbrush("10:CE:A9:28:93:24",protocolVersion=3)
    #device.readBrushMode(lambda x: print("Mode: {}".format(str(x))))
    #device.readBrushState(lambda x: print("State: {}".format(str(x))))
    #device.setBatteryUpdateCallback(lambda x: print("Battery: {} {}".format(x.level,x.remainingSec)))
    # device.setBrushingTimeUpdateCallback(lambda x: print("Time: {}s".format(x)))
    # device.setBrushStateUpdateCallback(lambda x: print("State: {}".format(str(x))))
    # device.setBrushModeUpdateCallback(lambda x: print("Mode: {}".format(str(x))))
    #device.writeAvailableModes([BrushMode.DAILY_CLEAN,BrushMode.WHITENING,BrushMode.SENSITIVE])
    print(str(device.readModelId()))
    print(str(device.readBatteryStatus()))
    #print(device.readAvailableModes())
    # device.setSectorTimer([30,30,30,30])
    # session = device.readSectorTimer()
    # [print(s) for s in session]
    # device.setUserId(10)
    # print(device.gerUserId())
    #device.writeSignalStatus(BrushSignal(vibrate=True,visualSignal=True))
    while True:
        try:
            device.waitForNotifications(0.5)
        except BTLEException as e:
            print(e)
            break
