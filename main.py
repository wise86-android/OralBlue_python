# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate

from OralBlue.AdvertiseParser import AdvertiseParser


def stateToStr(state:int):
    stateStr = {
        3:"brushing",
        2: "idle",
        4: "charging"
    }
    return stateStr[state]
def modeToStr(mode:int):
    modeStr = {
        0: 'off',
        1: 'daily_clean',
        2: 'sensitive',
        3: 'massage',
        4: 'whitening',
        5: 'deep_clean',
        6: 'tongue_cleaning',
        7: 'turbo'
    }
    return modeStr[mode]

def parse(data:str):
    advParser = AdvertiseParser(data)
    if advParser.isValid:
        print(advParser)

    if len(data)<22:
        print("unknow:",data)
        return
    print(data)
    values = {
        'state': stateToStr(int(data[11])),
        'pressure': data[12],
        'minute': data[15],
        'seconds': data[16:18],
        'mode': modeToStr(int(data[19])),
        'sector': data[21],

    }

    print(values)


# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        advertise = [data for (id,type,data) in dev.getScanData() if id == 255][0]
        parse(advertise)
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)


if __name__ == '__main__':
    # create a scanner object that sends BLE broadcast packets to the ScanDelegate
    scanner = Scanner().withDelegate(ScanDelegate())

    # start the scanner and keep the process running
    scanner.start()
    while True:
        print("Still running...")
        scanner.process()
