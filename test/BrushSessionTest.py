import unittest
from datetime import datetime, timedelta

from OralBlue import OralBAdvertise
from OralBlue.BrushMode import BrushMode
from OralBlue.BrushSession import BrushSession
from OralBlue.BrushState import BrushState


class BrushSessionTestCase(unittest.TestCase):

    def test_anExceptionIsThrownWhenTheDataAreLessThan16Bytes(self):
        with self.assertRaises(ValueError):
            BrushSession(b"\x00")

    def test_anExceptionIsThrownWhenTheDataAreMoreThan16Bytes(self):
        with self.assertRaises(ValueError):
            BrushSession(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

    def test_first4byteAreTheStartDate(self):
        session = BrushSession(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.startDate,datetime(year=2000,month=1,day=1))

        session = BrushSession(b"\x0A\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.startDate, datetime(year=2000, month=1, day=1,second=10))

    def test_byte5and6areTheDuration(self):
        session = BrushSession(b"\x00\x01\x02\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.duration,timedelta(seconds=1))
        session = BrushSession(b"\x00\x00\x00\x00\xb4\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.duration, timedelta(seconds=180))
        session = BrushSession(b"\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.duration, timedelta(seconds=0x2000))

    def test_byte8IsThePrefMode(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.prefMode,BrushMode(0x01))
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x04\x00\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.prefMode, BrushMode(0x04))

    def test_byte9And10IsSecondsUnderPressure(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x00\x00\x00\x00\x00")
        self.assertEqual(session.timeUnderPressure,timedelta(seconds=0x0908))
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x01\x00\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.timeUnderPressure, timedelta(seconds=1))

    def test_byte10IsNumberOfPressure(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x00\x00\x00\x00\x00")
        self.assertEqual(session.nPressure, 10)
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x00\x00\x00\x00\x00")
        self.assertEqual(session.nPressure,0)

    def test_byte11IsBatteryCharge(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x00\x00\x00\x00")
        self.assertEqual(session.finalBatteryState, 11)
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x32\x00\x00\x00\x00")
        self.assertEqual(session.finalBatteryState,50)

    def test_last4BytesAreTheLastCharge(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x00\x00\x00\x00")
        self.assertEqual(session.lastCharge,datetime(year=2000,month=1,day=1))
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x3B\x0A\x00\x00\x00")
        self.assertEqual(session.lastCharge,datetime(year=2000, month=1, day=1,second=10))

class BrushSessionV2Or3TestCase(unittest.TestCase):

    def test_bytes12AsNSectionAndTargetTime(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x00\x00\x00\x00",protocolVersion=3)
        self.assertEqual(session.lastCharge,None)
        self.assertEqual(session.numberOfSector,0)
        self.assertEqual(session.sessionTargetTime, 0)
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x3B\x78\x80\x00\x00",protocolVersion=3)
        self.assertEqual(session.lastCharge, None)
        self.assertEqual(session.numberOfSector, 4)
        self.assertEqual(session.sessionTargetTime, 120)

    def test_bytes14AsSessionIdAndUserId(self):
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x00\x00",protocolVersion=3)
        self.assertEqual(session.lastCharge,None)
        self.assertEqual(session.sessionId,0)
        self.assertEqual(session.userId, 0)
        session = BrushSession(b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x3B\x78\x80\x03\x20",protocolVersion=3)
        self.assertEqual(session.lastCharge, None)
        self.assertEqual(session.sessionId, 3)
        self.assertEqual(session.userId, 1)

if __name__ == '__main__':
    unittest.main()
