import unittest
from OralBlue import AdvertiseParser
from OralBlue.BrushMode import BrushMode
from OralBlue.BrushState import BrushState


class AdvertiseParserTestCase(unittest.TestCase):

    def test_advertiseMustStartWithDC00(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000000000")
        self.assertTrue(validParser.isValid)

        invalidParser = AdvertiseParser.AdvertiseParser("dd000000000000000000000000")
        self.assertFalse(invalidParser.isValid)

    def test_advetiseLengthIs11or13Bytes(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000000000")
        self.assertTrue(validParser.isValid)
        validParser = AdvertiseParser.AdvertiseParser("dc00000000000000000000")
        self.assertTrue(validParser.isValid)

        invalidParser = AdvertiseParser.AdvertiseParser("dc0000000000000000000000")
        self.assertFalse(invalidParser.isValid)

    def test_the3thByteIsProtocolVersion(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000300000000000000000000")
        self.assertEqual(validParser.protocolVersion, 3)
        validParser = AdvertiseParser.AdvertiseParser("dc001000000000000000000000")
        self.assertEqual(validParser.protocolVersion, 16)

    def test_the4thByteIsTypeId(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000056000000000000000000")
        self.assertEqual(validParser.typeId, 0x56)
        validParser = AdvertiseParser.AdvertiseParser("dc000041000000000000000000")
        self.assertEqual(validParser.typeId, 0x41)

    def test_the5thByteIsFwVersion(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000040000000000000000")
        self.assertEqual(validParser.fwVersion, 0x04)
        validParser = AdvertiseParser.AdvertiseParser("dc000000200000000000000000")
        self.assertEqual(validParser.fwVersion, 0x20)

    def test_the6thByteIsState(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000200000000000000")
        self.assertEqual(validParser.state, BrushState.IDLE)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000300000000000000")
        self.assertEqual(validParser.state, BrushState.RUN)

    def test_invalidStateAreMappedToUnknown(self):
        # state 0x18 doesn't exist
        validParser = AdvertiseParser.AdvertiseParser("dc00000000FF00000000000000")
        self.assertEqual(validParser.state, BrushState.UNKNOWN)

    def test_the7thByteHasTheHighPressureDetectorBit(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000080000000000000")
        self.assertTrue(validParser.hightPressureDetected)
        validParser = AdvertiseParser.AdvertiseParser("dc0000000000FF000000000000")
        self.assertTrue(validParser.hightPressureDetected)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000000000")
        self.assertFalse(validParser.hightPressureDetected)
        validParser = AdvertiseParser.AdvertiseParser("dc00000000007F000000000000")
        self.assertFalse(validParser.hightPressureDetected)

    def test_the8thByteIsBrushingTime(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000000000")
        self.assertEqual(validParser.brushingTimeS, 0)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000100000000")
        self.assertEqual(validParser.brushingTimeS, 1)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000010000000000")
        self.assertEqual(validParser.brushingTimeS, 60)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000010100000000")
        self.assertEqual(validParser.brushingTimeS, 61)

    def test_the10thByteIsTheBrushMode(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000002000000")
        self.assertEqual(validParser.brushingMode, BrushMode.SENSITIVE)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000003000000")
        self.assertEqual(validParser.brushingMode, BrushMode.MASSAGE)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000007000000")
        self.assertEqual(validParser.brushingMode, BrushMode.TURBO)

    def test_invalidBrushModeAreMapedAsUnknown(self):
        validParser = AdvertiseParser.AdvertiseParser("dc0000000000000000FF000000")
        self.assertEqual(validParser.brushingMode, BrushMode.UNKNOWN)

    def test_theLast3bitsOf11thByteIsCurentSector(self):
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000000000")
        self.assertEqual(validParser.sector, 0x00)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000010000")
        self.assertEqual(validParser.sector, 0x01)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000020000")
        self.assertEqual(validParser.sector, 0x02)
        validParser = AdvertiseParser.AdvertiseParser("dc000000000000000000FF0000")
        self.assertEqual(validParser.sector, 0x07)


if __name__ == '__main__':
    unittest.main()
