# import the necessary parts of the bluepy library
from datetime import datetime

from bluepy.btle import BTLEException

from OralBlue.BrushMode import BrushMode
from OralBlue.OralBToothbrush import OralBToothbrush

if __name__ == '__main__':
    device = OralBToothbrush("10:CE:A9:28:93:24")
    #device.readBrushMode(lambda x: print("Mode: {}".format(str(x))))
    #device.readBrushState(lambda x: print("State: {}".format(str(x))))
    # device.setBatteryUpdateCallback(lambda x: print("Battery: {}%".format(x)))
    # device.setBrushingTimeUpdateCallback(lambda x: print("Time: {}s".format(x)))
    # device.setBrushStateUpdateCallback(lambda x: print("State: {}".format(str(x))))
    # device.setBrushModeUpdateCallback(lambda x: print("Mode: {}".format(str(x))))
    #device.writeAvailableModes([BrushMode.DAILY_CLEAN,BrushMode.WHITENING,BrushMode.SENSITIVE])
    #print(device.readAvailableModes())
    session = device.readSession()
    [print(s) for s in session]
    while True:
        try:
            device.waitForNotifications(0.5)
        except BTLEException as e:
            print(e)
            break
