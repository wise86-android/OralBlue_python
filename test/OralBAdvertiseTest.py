import unittest
from OralBlue import OralBAdvertise
from OralBlue.BrushMode import BrushMode
from OralBlue.BrushSector import BrushSector
from OralBlue.BrushState import BrushState


class AdvertiseParserTestCase(unittest.TestCase):

    def test_advertiseMustStartWithDC00(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertTrue(validParser.isValid)

        invalidParser = OralBAdvertise.OralBAdvertise("dd000000000000000000000000")
        self.assertFalse(invalidParser.isValid)

    def test_advetiseLengthIs11or13Bytes(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertTrue(validParser.isValid)
        validParser = OralBAdvertise.OralBAdvertise("dc00000000000000000000")
        self.assertTrue(validParser.isValid)

        invalidParser = OralBAdvertise.OralBAdvertise("dc0000000000000000000000")
        self.assertFalse(invalidParser.isValid)

    def test_the3thByteIsProtocolVersion(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000300000000000000000000")
        self.assertEqual(validParser.protocolVersion, 3)
        validParser = OralBAdvertise.OralBAdvertise("dc001000000000000000000000")
        self.assertEqual(validParser.protocolVersion, 16)

    def test_the4thByteIsTypeId(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000056000000000000000000")
        self.assertEqual(validParser.typeId, 0x56)
        validParser = OralBAdvertise.OralBAdvertise("dc000041000000000000000000")
        self.assertEqual(validParser.typeId, 0x41)

    def test_the5thByteIsFwVersion(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000040000000000000000")
        self.assertEqual(validParser.fwVersion, 0x04)
        validParser = OralBAdvertise.OralBAdvertise("dc000000200000000000000000")
        self.assertEqual(validParser.fwVersion, 0x20)

    def test_the6thByteIsState(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000200000000000000")
        self.assertEqual(validParser.state, BrushState.IDLE)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000300000000000000")
        self.assertEqual(validParser.state, BrushState.RUN)

    def test_invalidStateAreMappedToUnknown(self):
        # state 0x18 doesn't exist
        validParser = OralBAdvertise.OralBAdvertise("dc00000000FF00000000000000")
        self.assertEqual(validParser.state, BrushState.UNKNOWN)

    def test_the7thByteHasTheHighPressureDetectorBit(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000080000000000000")
        self.assertTrue(validParser.hightPressureDetected)
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000FF000000000000")
        self.assertTrue(validParser.hightPressureDetected)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertFalse(validParser.hightPressureDetected)
        validParser = OralBAdvertise.OralBAdvertise("dc00000000007F000000000000")
        self.assertFalse(validParser.hightPressureDetected)

    def test_the6thByteHasMotorSpeedBit(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000040000000000000")
        self.assertTrue(validParser.hasReducedMotorSpeed)
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000FF000000000000")
        self.assertTrue(validParser.hasReducedMotorSpeed)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertFalse(validParser.hasReducedMotorSpeed)
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000BF000000000000")
        self.assertFalse(validParser.hasReducedMotorSpeed)

    def test_the1stBitIsTheTimerMode(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000001000000000000")
        self.assertFalse(validParser.hasProfesionalTimer)
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000FF000000000000")
        self.assertFalse(validParser.hasProfesionalTimer)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertTrue(validParser.hasProfesionalTimer)
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000FE000000000000")
        self.assertTrue(validParser.hasProfesionalTimer)

    def test_the8thByteIsBrushingTime(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertEqual(validParser.brushingTimeS, 0)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000100000000")
        self.assertEqual(validParser.brushingTimeS, 1)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000010000000000")
        self.assertEqual(validParser.brushingTimeS, 60)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000010100000000")
        self.assertEqual(validParser.brushingTimeS, 61)

    def test_the10thByteIsTheBrushMode(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000002000000")
        self.assertEqual(validParser.brushingMode, BrushMode.SENSITIVE)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000003000000")
        self.assertEqual(validParser.brushingMode, BrushMode.MASSAGE)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000007000000")
        self.assertEqual(validParser.brushingMode, BrushMode.TURBO)

    def test_invalidBrushModeAreMapedAsUnknown(self):
        validParser = OralBAdvertise.OralBAdvertise("dc0000000000000000FF000000")
        self.assertEqual(validParser.brushingMode, BrushMode.UNKNOWN)

    def test_theLast3bitsOf11thByteIsCurrentSector(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertEqual(validParser.sector, BrushSector.NO_SECTOR)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000010000")
        self.assertEqual(validParser.sector, BrushSector.SECTOR_1)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000020000")
        self.assertEqual(validParser.sector, BrushSector.SECTOR_2)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000FF0000")
        self.assertEqual(validParser.sector, BrushSector.LAST_SECTOR)

    def test_thecentral3bitsOf11thByteIsCurrentSmily(self):
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000000000")
        self.assertEqual(validParser.smiley, 0x00)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000080000")
        self.assertEqual(validParser.smiley, 0x01)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000100000")
        self.assertEqual(validParser.smiley, 0x02)
        validParser = OralBAdvertise.OralBAdvertise("dc000000000000000000FF0000")
        self.assertEqual(validParser.smiley, 0x07)

if __name__ == '__main__':
    unittest.main()
