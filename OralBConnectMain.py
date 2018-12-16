# import the necessary parts of the bluepy library
from bluepy.btle import BTLEException

from OralBlue.OralBToothbrush import OralBToothbrush

if __name__ == '__main__':
    device = OralBToothbrush("10:CE:A9:28:93:24")
    #device.readBrushMode(lambda x: print("Mode: {}".format(str(x))))
    #device.readBrushState(lambda x: print("State: {}".format(str(x))))
    # device.setBatteryUpdateCallback(lambda x: print("Battery: {}%".format(x)))
    # device.setBrushingTimeUpdateCallback(lambda x: print("Time: {}s".format(x)))
    # device.setBrushStateUpdateCallback(lambda x: print("State: {}".format(str(x))))
    # device.setBrushModeUpdateCallback(lambda x: print("Mode: {}".format(str(x))))
    print(device.readCurrentTime())
    device.setCurrentTime()
    print(device.readCurrentTime())

    while True:
        try:
            device.waitForNotifications(0.5)
        except BTLEException as e:
            print(e)
            break
