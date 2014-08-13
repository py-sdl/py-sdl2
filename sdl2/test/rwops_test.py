import os
import sys
import ctypes
import unittest
from io import BytesIO
from .. import rwops

if sys.version_info[0] >= 3:
    byteify = bytes
    stringify = lambda x, enc: x.decode(enc)
else:
    byteify = lambda x, enc: x.encode(enc)
    stringify = lambda x, enc: str(x)

testfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "resources", "rwopstest.txt")


# TODO: extended checks for r/w operations outside of buffer ranges, invalid
# values, etc.!
class SDLRWopsTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_RWops(self):
        rw = rwops.SDL_RWops()
        self.assertIsInstance(rw, rwops.SDL_RWops)

    def test_SDL_RWFromFile(self):
        rw = rwops.SDL_RWFromFile(testfile.encode("utf-8"), b"r")
        self.assertIsInstance(rw.contents, rwops.SDL_RWops)
        # Read the first 36 bytes(sic!). It should be:
        # 'This is a test file for sdl2.rwops!'
        length = 36
        buf = BytesIO()
        while length >= 2:
            # Reading in two bytes - we have plain text(1-byte encoding), so
            # we read in 2 characters at a time. This means that the first
            # character is always stored in the lo byte.
            ch = rwops.SDL_ReadLE16(rw)
            buf.write(byteify(chr(ch & 0x00FF), "utf-8"))
            buf.write(byteify(chr(ch >> 8), "utf-8"))
            length -= 2
        self.assertEqual(stringify(buf.getvalue(), "utf-8"),
                         "This is a test file for  sdl2.rwops!")

    @unittest.skip("not implemented")
    def test_SDL_RWFromFP(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_RWFromMem(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_RWFromConstMem(self):
        pass

    def test_rw_from_object(self):
        buf = BytesIO()
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        for s in("Test", "Test", "Test", "Banana"):
            buf.write(byteify(s, "utf-8"))
            length = rwops.SDL_RWseek(rw, 0, rwops.RW_SEEK_END)
            rwops.SDL_RWseek(rw, 0, rwops.RW_SEEK_SET)
            self.assertEqual(len(buf.getvalue()), length)
        rwops.SDL_RWclose(rw)
        self.assertTrue(buf.closed)
        self.assertRaises(ValueError, buf.write, "Test")
        self.assertRaises(ValueError, buf.getvalue)

    def test_SDL_RWSeekTell(self):
        data = byteify("A Teststring of length 25", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        pos = rwops.SDL_RWseek(rw, 0, rwops.RW_SEEK_END)
        self.assertTrue(pos == buf.tell() == len(data))
        pos = rwops.SDL_RWseek(rw, 0, rwops.RW_SEEK_SET)
        self.assertTrue(pos == buf.tell() == 0)

        pos = rwops.SDL_RWseek(rw, 15, rwops.RW_SEEK_CUR)
        self.assertTrue(pos == buf.tell() == 15)
        pos = rwops.SDL_RWseek(rw, -3, rwops.RW_SEEK_CUR)
        self.assertTrue(pos == buf.tell() == 12)
        pos = rwops.SDL_RWseek(rw, 7, rwops.RW_SEEK_CUR)
        self.assertTrue(pos == buf.tell() == 19)

        pos = rwops.SDL_RWseek(rw, -11, rwops.RW_SEEK_END)
        self.assertTrue(pos == buf.tell() == 14)

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertTrue(pos == buf.tell() == 8)

        pos = rwops.SDL_RWseek(rw, -2, rwops.RW_SEEK_SET)
        self.assertEqual(pos, -1)
        self.assertTrue(buf.tell() == 8)
        pos = rwops.SDL_RWseek(rw, 12, rwops.RW_SEEK_END)
        self.assertTrue(pos == buf.tell() == len(data) + 12)

    def test_SDL_RWread(self):
        data = byteify("A Teststring of length 25", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)
        
        readbuf = ctypes.create_string_buffer(2)
        
        read = rwops.SDL_RWread(rw, readbuf, 1, 2)
        self.assertEqual(read, 2)
        self.assertEqual(readbuf.raw, b"A ")
        readbuf = ctypes.create_string_buffer(10)
        read = rwops.SDL_RWread(rw, readbuf, 1, 10)
        self.assertEqual(read, 10)
        self.assertEqual(readbuf.raw, b"Teststring")

    def test_SDL_RWwrite(self):
        data = byteify("A Teststring of length 25", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        writebuf = ctypes.create_string_buffer(b"XQ")
        written = rwops.SDL_RWwrite(rw, writebuf, 1, 2)
        self.assertEqual(written, 2)
        self.assertEqual(buf.getvalue(), b"XQTeststring of length 25")
        
        writebuf = ctypes.create_string_buffer(b"banana")
        rwops.SDL_RWseek(rw, 14, rwops.RW_SEEK_CUR)
        written = rwops.SDL_RWwrite(rw, writebuf, 1, 6)
        self.assertEqual(written, 6)
        self.assertEqual(buf.getvalue(), b"XQTeststring of banana 25")
       
    def test_SDL_RWclose(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        self.assertEqual(buf.getvalue(), data)
        rwops.SDL_RWclose(rw)
        self.assertRaises(ValueError, buf.getvalue)

    @unittest.skip("not implemented")
    def test_SDL_AllocFreeRW(self):
        pass

    def test_SDL_ReadLE16(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadLE16(rw)
        self.assertEqual(chr(ch & 0x00FF), "A")
        self.assertEqual(chr(ch >> 8), " ")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadLE16(rw)
        self.assertEqual(chr(ch & 0x00FF), "r")
        self.assertEqual(chr(ch >> 8), "i")

    def test_SDL_ReadBE16(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadBE16(rw)
        self.assertEqual(chr(ch & 0x00FF), " ")
        self.assertEqual(chr(ch >> 8), "A")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadBE16(rw)
        self.assertEqual(chr(ch & 0x00FF), "i")
        self.assertEqual(chr(ch >> 8), "r")

    def test_SDL_ReadLE32(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadLE32(rw)
        self.assertEqual(chr(ch & 0x000000FF), "A")
        self.assertEqual(chr((ch & 0x0000FF00) >> 8), " ")
        self.assertEqual(chr((ch & 0x00FF0000) >> 16), "T")
        self.assertEqual(chr((ch & 0xFF000000) >> 24), "e")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadLE32(rw)
        self.assertEqual(chr(ch & 0x000000FF), "r")
        self.assertEqual(chr((ch & 0x0000FF00) >> 8), "i")
        self.assertEqual(chr((ch & 0x00FF0000) >> 16), "n")
        self.assertEqual(chr((ch & 0xFF000000) >> 24), "g")

    def test_SDL_ReadBE32(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadBE32(rw)
        self.assertEqual(chr(ch & 0x000000FF), "e")
        self.assertEqual(chr((ch & 0x0000FF00) >> 8), "T")
        self.assertEqual(chr((ch & 0x00FF0000) >> 16), " ")
        self.assertEqual(chr((ch & 0xFF000000) >> 24), "A")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadBE32(rw)
        self.assertEqual(chr(ch & 0x000000FF), "g")
        self.assertEqual(chr((ch & 0x0000FF00) >> 8), "n")
        self.assertEqual(chr((ch & 0x00FF0000) >> 16), "i")
        self.assertEqual(chr((ch & 0xFF000000) >> 24), "r")

    def test_SDL_ReadLE64(self):
        data = byteify("A Teststring 64b", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadLE64(rw)
        self.assertEqual(chr(ch & 0x00000000000000FF), "A")
        self.assertEqual(chr((ch & 0x000000000000FF00) >> 8), " ")
        self.assertEqual(chr((ch & 0x0000000000FF0000) >> 16), "T")
        self.assertEqual(chr((ch & 0x00000000FF000000) >> 24), "e")
        self.assertEqual(chr((ch & 0x000000FF00000000) >> 32), "s")
        self.assertEqual(chr((ch & 0x0000FF0000000000) >> 40), "t")
        self.assertEqual(chr((ch & 0x00FF000000000000) >> 48), "s")
        self.assertEqual(chr((ch & 0xFF00000000000000) >> 56), "t")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadLE64(rw)
        self.assertEqual(chr(ch & 0x00000000000000FF), "r")
        self.assertEqual(chr((ch & 0x000000000000FF00) >> 8), "i")
        self.assertEqual(chr((ch & 0x0000000000FF0000) >> 16), "n")
        self.assertEqual(chr((ch & 0x00000000FF000000) >> 24), "g")
        self.assertEqual(chr((ch & 0x000000FF00000000) >> 32), " ")
        self.assertEqual(chr((ch & 0x0000FF0000000000) >> 40), "6")
        self.assertEqual(chr((ch & 0x00FF000000000000) >> 48), "4")
        self.assertEqual(chr((ch & 0xFF00000000000000) >> 56), "b")

    def test_SDL_ReadBE64(self):
        data = byteify("A Teststring 64b", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        ch = rwops.SDL_ReadBE64(rw)
        self.assertEqual(chr(ch & 0x00000000000000FF), "t")
        self.assertEqual(chr((ch & 0x000000000000FF00) >> 8), "s")
        self.assertEqual(chr((ch & 0x0000000000FF0000) >> 16), "t")
        self.assertEqual(chr((ch & 0x00000000FF000000) >> 24), "s")
        self.assertEqual(chr((ch & 0x000000FF00000000) >> 32), "e")
        self.assertEqual(chr((ch & 0x0000FF0000000000) >> 40), "T")
        self.assertEqual(chr((ch & 0x00FF000000000000) >> 48), " ")
        self.assertEqual(chr((ch & 0xFF00000000000000) >> 56), "A")

        pos = rwops.SDL_RWseek(rw, 8, rwops.RW_SEEK_SET)
        self.assertEqual(pos, 8)
        ch = rwops.SDL_ReadBE64(rw)
        self.assertEqual(chr(ch & 0x00000000000000FF), "b")
        self.assertEqual(chr((ch & 0x000000000000FF00) >> 8), "4")
        self.assertEqual(chr((ch & 0x0000000000FF0000) >> 16), "6")
        self.assertEqual(chr((ch & 0x00000000FF000000) >> 24), " ")
        self.assertEqual(chr((ch & 0x000000FF00000000) >> 32), "g")
        self.assertEqual(chr((ch & 0x0000FF0000000000) >> 40), "n")
        self.assertEqual(chr((ch & 0x00FF000000000000) >> 48), "i")
        self.assertEqual(chr((ch & 0xFF00000000000000) >> 56), "r")

    def test_SDL_WriteLE16(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("q") << 8) | (ord("%")))
        rwops.SDL_WriteLE16(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "%qTeststring")

        rwops.SDL_RWseek(rw, 6, rwops.RW_SEEK_SET)
        rwops.SDL_WriteLE16(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "%qTest%qring")

    def test_SDL_WriteBE16(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("q") << 8) | (ord("%")))
        rwops.SDL_WriteBE16(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "q%Teststring")

        rwops.SDL_RWseek(rw, 6, rwops.RW_SEEK_SET)
        rwops.SDL_WriteBE16(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "q%Testq%ring")

    def test_SDL_WriteLE32(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("a") << 24) |
                 (ord("c") << 16) |
                 (ord("f") << 8) |
                 (ord("z"))
                 )
        rwops.SDL_WriteLE32(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "zfcaststring")

        rwops.SDL_RWseek(rw, 6, rwops.RW_SEEK_SET)
        rwops.SDL_WriteLE32(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "zfcastzfcang")

    def test_SDL_WriteBE32(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("a") << 24) |
                 (ord("c") << 16) |
                 (ord("f") << 8) |
                 (ord("z"))
                 )
        rwops.SDL_WriteBE32(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "acfzststring")

        rwops.SDL_RWseek(rw, 6, rwops.RW_SEEK_SET)
        rwops.SDL_WriteBE32(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "acfzstacfzng")

    def test_SDL_WriteLE64(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("q") << 56) |
                 (ord("w") << 48) |
                 (ord("b") << 40) |
                 (ord("k") << 32) |
                 (ord("a") << 24) |
                 (ord("c") << 16) |
                 (ord("f") << 8) |
                 (ord("z"))
                 )

        rwops.SDL_WriteLE64(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "zfcakbwqring")

        rwops.SDL_RWseek(rw, 4, rwops.RW_SEEK_SET)
        rwops.SDL_WriteLE64(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "zfcazfcakbwq")

    def test_SDL_WriteBE64(self):
        data = byteify("A Teststring", "utf-8")
        buf = BytesIO(data)
        rw = rwops.rw_from_object(buf)
        self.assertIsInstance(rw, rwops.SDL_RWops)

        value = ((ord("q") << 56) |
                 (ord("w") << 48) |
                 (ord("b") << 40) |
                 (ord("k") << 32) |
                 (ord("a") << 24) |
                 (ord("c") << 16) |
                 (ord("f") << 8) |
                 (ord("z"))
                 )

        rwops.SDL_WriteBE64(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "qwbkacfzring")

        rwops.SDL_RWseek(rw, 4, rwops.RW_SEEK_SET)
        rwops.SDL_WriteBE64(rw, value)
        self.assertEqual(stringify(buf.getvalue(), "utf-8"), "qwbkqwbkacfz")

if __name__ == '__main__':
    sys.exit(unittest.main())
