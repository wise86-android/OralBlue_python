from typing import Optional
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry

from OralBlue.OralBAdvertise import OralBAdvertise

# create a delegate class to receive the BLE broadcast packets
class OralBScanDelegate(DefaultDelegate):

    def handleNotification(self, cHandle, data):
        pass

    @staticmethod
    def _printNewDevice(device: ScanEntry, adv: OralBAdvertise):
        printMe = "New device detected:\n" \
              "Address: {}\n" \
              "Type: {}\n" \
              "FwVersion: {}\n".format(device.addr, str(adv.typeId), adv.fwVersion)
        print(printMe)
        print(str(adv))

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev: ScanEntry, isNewDev: bool, isNewData):
        advertise = OralBAdvertise.buildFromScanEntry(dev)

        if advertise is None:
            return

        if isNewDev:
            OralBScanDelegate._printNewDevice(dev,advertise)
        elif isNewData:
            print(str(advertise))


if __name__ == '__main__':
    # create a scanner object that sends BLE broadcast packets to the ScanDelegate
    scanner = Scanner().withDelegate(OralBScanDelegate())

    # start the scanner and keep the process running
    scanner.start()
    while True:
        print("Still running...")
        scanner.process()
