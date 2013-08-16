import sys
import unittest
from ..ext import particles


class SDL2ExtParticlesTest(unittest.TestCase):
    __tags__ = ["sdl2ext"]

    def test_Particle(self):
        p = particles.Particle(0, 0, 0)
        self.assertIsInstance(p, particles.Particle)
        self.assertTrue(p.x == p.y == p.life == 0)
        p = particles.Particle(1, 2, 3)
        self.assertIsInstance(p, particles.Particle)
        self.assertEqual(p.x, 1)
        self.assertEqual(p.y, 2)
        self.assertEqual(p.life, 3)

    def test_Particle_xy_position(self):
        for x in range(-100, 100):
            for y in range(-100, 100):
                p = particles.Particle(x, y, 1)
                self.assertEqual(p.position, (x, y))
                self.assertEqual(p.x, x)
                self.assertEqual(p.y, y)
                p.position = x + 1, y + 1
                self.assertEqual(p.position, (x + 1, y + 1))
                self.assertEqual(p.x, x + 1)
                self.assertEqual(p.y, y + 1)
                p.x = x
                self.assertEqual(p.position, (x, y + 1))
                self.assertEqual(p.x, x)
                self.assertEqual(p.y, y + 1)
                p.y = y
                self.assertEqual(p.position, (x, y))
                self.assertEqual(p.x, x)
                self.assertEqual(p.y, y)

    def test_Particle_life(self):
        for life in range(-100, 100):
            p = particles.Particle(0, 0, life)
            self.assertEqual(p.life, life)

    def test_ParticleEngine(self):
        engine = particles.ParticleEngine()
        self.assertIsInstance(engine, particles.ParticleEngine)
        self.assertTrue(particles.Particle in engine.componenttypes)
        self.assertIsNone(engine.createfunc)
        self.assertIsNone(engine.deletefunc)
        self.assertIsNone(engine.updatefunc)

    def test_ParticleEngine_createfunc(self):
        def func(w, c):
            pass
        engine = particles.ParticleEngine()
        self.assertIsNone(engine.createfunc)
        engine.createfunc = func
        self.assertEqual(engine.createfunc, func)

        def setf(x, f):
            x.createfunc = f
        self.assertRaises(TypeError, setf, engine, None)
        self.assertRaises(TypeError, setf, engine, "Test")
        self.assertRaises(TypeError, setf, engine, 1234)

    def test_ParticleEngine_deletefunc(self):
        def func(w, c):
            pass
        engine = particles.ParticleEngine()
        self.assertIsNone(engine.deletefunc)
        engine.deletefunc = func
        self.assertEqual(engine.deletefunc, func)

        def setf(x, f):
            x.deletefunc = f
        self.assertRaises(TypeError, setf, engine, None)
        self.assertRaises(TypeError, setf, engine, "Test")
        self.assertRaises(TypeError, setf, engine, 1234)

    def test_ParticleEngine_updatefunc(self):
        def func(w, c):
            pass
        engine = particles.ParticleEngine()
        self.assertIsNone(engine.updatefunc)
        engine.updatefunc = func
        self.assertEqual(engine.updatefunc, func)

        def setf(x, f):
            x.updatefunc = f
        self.assertRaises(TypeError, setf, engine, None)
        self.assertRaises(TypeError, setf, engine, "Test")
        self.assertRaises(TypeError, setf, engine, 1234)

    def test_ParticleEngine_process(self):
        def cfunc(w, c):
            self.assertEqual(len(c), w["runs"])
            for p in c:
                self.assertLessEqual(p.life, 0)

        def ufunc(w, c):
            self.assertEqual(len(c), 100 - w["runs"])
            for p in c:
                self.assertGreaterEqual(p.life, 1)

        def dfunc(w, c):
            self.assertEqual(len(c), w["runs"])
            for p in c:
                self.assertLessEqual(p.life, 0)

        plist = []
        for x in range(2, 102):
            plist.append(particles.Particle(x, x, x - 1))

        engine = particles.ParticleEngine()
        engine.createfunc = cfunc
        engine.updatefunc = ufunc
        engine.deletefunc = dfunc
        world = {"runs": 1}
        engine.process(world, plist)
        world["runs"] = 2
        engine.process(world, plist)


if __name__ == '__main__':
    sys.exit(unittest.main())
