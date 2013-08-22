import os
import sys
import unittest
import urllib
if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.request as urllib2
from ..ext import resources


class SDL2ExtResourcesTest(unittest.TestCase):
    __tags__ = ["sdl2ext"]

    def test_open_zipfile(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        zfile = os.path.join(fpath, "resources.zip")

        # resources.zip is a packed version of resources/, which at
        # least contains
        #
        # resources/rwopstest.txt
        # resources/surfacetest.bmp

        resfile = resources.open_zipfile(zfile, "rwopstest.txt", "resources")
        self.assertIsNotNone(resfile)
        resfile = resources.open_zipfile(zfile, "resources/rwopstest.txt")
        self.assertIsNotNone(resfile)

        self.assertRaises(KeyError, resources.open_zipfile, zfile, "invalid")
        self.assertRaises(KeyError, resources.open_zipfile, zfile, None)
        self.assertRaises(KeyError, resources.open_zipfile, zfile,
                          "rwopstest.txt", "data")
        self.assertRaises(KeyError, resources.open_zipfile, zfile,
                          "rwopstest.txt", 1234)
        self.assertRaises(KeyError, resources.open_zipfile, zfile,
                          None, None)

        self.assertRaises(TypeError, resources.open_zipfile, None,
                          "rwopstest.txt")
        self.assertRaises(TypeError, resources.open_zipfile, None, None)
        self.assertRaises(TypeError, resources.open_zipfile, None,
                          "rwopstest.txt", "resources")

    def test_open_tarfile(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        tfile = os.path.join(fpath, "resources.tar.gz")

        # resources.tar.gz is a packed version of resources/, which at
        # least contains
        #
        # resources/rwopstest.txt
        # resources/surfacetest.bmp

        resfile = resources.open_tarfile(tfile, "rwopstest.txt", "resources")
        self.assertIsNotNone(resfile)
        resfile = resources.open_tarfile(tfile, "resources/rwopstest.txt")
        self.assertIsNotNone(resfile)

        # TODO: refine the error handling in open_tarfile()
        self.assertRaises(KeyError, resources.open_tarfile, tfile, "invalid")
        self.assertRaises(AttributeError, resources.open_tarfile, tfile, None)
        self.assertRaises(KeyError, resources.open_tarfile, tfile,
                          "rwopstest.txt", "data")
        self.assertRaises(KeyError, resources.open_tarfile, tfile,
                          "rwopstest.txt", 1234)
        self.assertRaises(AttributeError, resources.open_tarfile, tfile,
                          None, None)

        self.assertRaises(ValueError, resources.open_tarfile, None,
                          "rwopstest.txt")
        self.assertRaises(ValueError, resources.open_tarfile, None, None)
        self.assertRaises(ValueError, resources.open_tarfile, None,
                          "rwopstest.txt", "resources")

    def test_open_url(self):
        if sys.version_info[0] < 3:
            p2url = urllib.pathname2url
        else:
            p2url = urllib2.pathname2url

        fpath = os.path.join(os.path.dirname(__file__), "resources")
        fpath = os.path.abspath(fpath)
        tfile = os.path.join(fpath, "rwopstest.txt")
        urlpath = "file:%s" % p2url(tfile)
        resfile = resources.open_url(urlpath)
        self.assertIsNotNone(resfile)

        tfile = os.path.join(fpath, "invalid")
        urlpath = "file:%s" % p2url(tfile)
        self.assertRaises(urllib2.URLError, resources.open_url, urlpath)

    def test_Resources(self):
        self.assertRaises(ValueError, resources.Resources, "invalid")

        res = resources.Resources()
        self.assertIsInstance(res, resources.Resources)
        self.assertRaises(KeyError, res.get, "surfacetest.bmp")

        fpath = os.path.join(os.path.dirname(__file__), "resources")
        res = resources.Resources(fpath)
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertIsNotNone(res.get("surfacetest.bmp"))

        res2 = resources.Resources(__file__)
        self.assertIsNotNone(res2.get("rwopstest.txt"))
        self.assertIsNotNone(res2.get("surfacetest.bmp"))

        res3 = resources.Resources(__file__, "resources")
        self.assertIsNotNone(res3.get("rwopstest.txt"))
        self.assertIsNotNone(res3.get("surfacetest.bmp"))

    def test_Resources_add(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        sfile = os.path.join(fpath, "surfacetest.bmp")
        zfile = os.path.join(fpath, "resources.zip")

        res = resources.Resources()
        res.add(sfile)
        self.assertRaises(KeyError, res.get, "rwopstest.txt")
        self.assertIsNotNone(res.get("surfacetest.bmp"))

        res.add(zfile)
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertIsNotNone(res.get("surfacetest.bmp"))

        self.assertRaises(TypeError, res.add, None)
        self.assertRaises(ValueError, res.add, "invalid_name.txt")

    def test_Resources_add_file(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        sfile = os.path.join(fpath, "surfacetest.bmp")
        zfile = os.path.join(fpath, "resources.zip")

        res = resources.Resources()
        res.add_file(sfile)
        res.add_file(zfile)

        self.assertRaises(KeyError, res.get, "rwopstest.txt")
        self.assertIsNotNone(res.get("surfacetest.bmp"))
        self.assertIsNotNone(res.get("resources.zip"))

        self.assertRaises(TypeError, res.add_file, None)
        self.assertRaises(ValueError, res.add_file, "invalid_name.txt")

    def test_Resources_add_archive(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        zfile = os.path.join(fpath, "resources.zip")
        tfile = os.path.join(fpath, "resources.tar.gz")

        res = resources.Resources()
        res.add_archive(zfile)

        self.assertIsNotNone(res.get("surfacetest.bmp"))
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertRaises(KeyError, res.get, "resources.zip")

        self.assertRaises(TypeError, res.add_archive, None)
        self.assertRaises(ValueError, res.add_archive, "invalid_name.txt")

        res = resources.Resources()
        res.add_archive(tfile, typehint="targz")
        self.assertIsNotNone(res.get("surfacetest.bmp"))
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertRaises(KeyError, res.get, "resources.tar.gz")

    def test_Resources_get(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")

        for path in (fpath, None):
            res = resources.Resources(path)

            self.assertRaises(KeyError, res.get, "invalid_file.txt")
            self.assertRaises(KeyError, res.get, None)
            self.assertRaises(KeyError, res.get, 123456)
            if path is None:
                self.assertRaises(KeyError, res.get, "surfacetest.bmp")
                self.assertRaises(KeyError, res.get, "rwopstest.txt")
            else:
                self.assertIsNotNone(res.get("surfacetest.bmp"))
                self.assertIsNotNone(res.get("rwopstest.txt"))

    def test_Resources_get_filelike(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        zfile = os.path.join(fpath, "resources.zip")
        pfile = os.path.join(fpath, "rwopstest.txt")

        res = resources.Resources()
        res.add(zfile)

        v1 = res.get_filelike("rwopstest.txt")
        v2 = res.get_filelike("surfacetest.bmp")
        self.assertEqual(type(v1), type(v2))

        res.add(pfile)

        v1 = res.get_filelike("rwopstest.txt")
        v2 = res.get_filelike("surfacetest.bmp")
        self.assertNotEqual(type(v1), type(v2))

        self.assertRaises(KeyError, res.get_filelike, None)
        self.assertRaises(KeyError, res.get_filelike, "invalid")
        self.assertRaises(KeyError, res.get_filelike, 1234)

    def test_Resources_get_path(self):
        fpath = os.path.join(os.path.dirname(__file__), "resources")
        zfile = os.path.join(fpath, "resources.zip")
        pfile = os.path.join(fpath, "rwopstest.txt")

        res = resources.Resources()
        res.add(zfile)
        res.add(pfile)

        zpath = res.get_path("surfacetest.bmp")
        self.assertTrue(zpath.find("surfacetest.bmp@") != -1)
        self.assertNotEqual(zpath, zfile)
        ppath = res.get_path("rwopstest.txt")
        self.assertTrue(ppath.find("rwopstest.txt") != -1)

        self.assertRaises(KeyError, res.get_path, None)
        self.assertRaises(KeyError, res.get_path, "invalid")
        self.assertRaises(KeyError, res.get_path, 1234)

    def test_Resources_scan(self):
        fpath = os.path.join(os.path.dirname(__file__))
        res = resources.Resources()
        res.scan(fpath)
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertIsNotNone(res.get("surfacetest.bmp"))

        self.assertRaises(ValueError, res.scan, "invalid")
        self.assertRaises(ValueError, res.scan, fpath, "invalid")
        self.assertRaises(Exception, res.scan, 12345)

        res = resources.Resources()
        res.scan(fpath, "resources")
        self.assertIsNotNone(res.get("rwopstest.txt"))
        self.assertIsNotNone(res.get("surfacetest.bmp"))

if __name__ == '__main__':
    sys.exit(unittest.main())
