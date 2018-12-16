import unittest
from datetime import datetime

from OralBlue.OralBDate import OralBDate


class OralBDateTestCase(unittest.TestCase):

    def test_theConstructorThrowIfTheDataAreLessThan4Bytes(self):
        with self.assertRaises(ValueError):
            OralBDate(b"\x00")

    def test_theConstructorThrowIfTheDataAreMoreThan4Bytes(self):
        with self.assertRaises(ValueError):
            OralBDate(b"\x00\x00\x00\x00\x00")

    def test_theBytesAreTheSecondAfter2000gen1(self):
        date = OralBDate(b"\x00\x00\x00\x00")
        self.assertEqual(date.datetime, datetime(year=2000, month=1, day=1))

    def test_theBytesAreInLittleEndian(self):
        date = OralBDate(b"\x01\x00\x00\x00")
        self.assertEqual(date.datetime, datetime(year=2000, month=1, day=1,second=1))

    def test_toByteReturnTheOriginalSequence(self):
        byteSeq = b"\x01\x02\x03\x04"
        date = OralBDate(byteSeq)
        self.assertEqual(byteSeq,date.toBytes())

    def test_fromDatetimeConvertToOralBDate(self):
        byteSeq1 = b"\x00\x00\x00\x00"
        date1 = datetime(year=2000,month=1,day=1)
        oralb1 = OralBDate(byteSeq1)
        self.assertEqual(oralb1.toBytes(),byteSeq1)
        byteSeq2 = b"\x05\x00\x00\x00"
        date2 = datetime(year=2000, month=1, day=1,second=5)
        oralb2 = OralBDate(byteSeq2)
        self.assertEqual(oralb2.toBytes(), byteSeq2)

if __name__ == '__main__':
    unittest.main()