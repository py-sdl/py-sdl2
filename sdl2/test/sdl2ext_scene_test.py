import sys
import unittest
from ..ext.events import EventHandler
from ..ext import scene


class SDL2ExtSceneTest(unittest.TestCase):
    __tags__ = ["scene", "sdl2ext"]

    def test_SceneManager(self):
        mgr = scene.SceneManager()
        self.assertIsInstance(mgr, scene.SceneManager)
        self.assertEqual(mgr.scenes, [])
        self.assertIsNone(mgr.next)
        self.assertIsNone(mgr.current)

    def test_SceneManager_push_pop(self):
        scene1 = scene.Scene()
        scene2 = scene.Scene()
        mgr = scene.SceneManager()
        mgr.push(scene1)
        self.assertEqual(mgr.next, scene1)
        self.assertIsNone(mgr.current)
        self.assertEqual(mgr.scenes, [])
        mgr.pop()
        self.assertEqual(mgr.next, scene1)
        self.assertIsNone(mgr.current)
        self.assertEqual(mgr.scenes, [])
        mgr.push(scene2)
        mgr.push(scene2)
        mgr.push(scene2)
        mgr.pop()
        mgr.pop()
        mgr.pop()
        self.assertEqual(mgr.next, scene2)
        self.assertIsNone(mgr.current)
        self.assertEqual(mgr.scenes, [])

        mgr.update()
        self.assertEqual(mgr.current, scene2)
        self.assertIsNone(mgr.next)
        self.assertEqual(mgr.scenes, [])
        mgr.push(scene1)
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, scene1)
        self.assertEqual(mgr.scenes, [scene2])
        mgr.push(scene1)
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, scene1)
        self.assertEqual(mgr.scenes, [scene2, scene2])
        mgr.push(scene1)
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, scene1)
        self.assertEqual(mgr.scenes, [scene2, scene2, scene2])
        mgr.pop()
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, scene2)
        self.assertEqual(mgr.scenes, [scene2, scene2])

    def test_SceneManager_pause_unpause_update(self):
        scene1 = scene.Scene("Scene 1")
        scene2 = scene.Scene("Scene 2")
        mgr = scene.SceneManager()

        paused = []
        unpaused = []
        started = []
        ended = []

        def pause_cb(scene):
            paused.append(scene)

        def unpause_cb(scene):
            unpaused.append(scene)

        def started_cb(scene):
            started.append(scene)

        def ended_cb(scene):
            ended.append(scene)

        for s in (scene1, scene2):
            s.started += started_cb
            s.paused += pause_cb
            s.unpaused += unpause_cb
            s.ended += ended_cb

        mgr.push(scene1)
        self.assertEqual(scene1.state, scene.SCENE_ENDED)
        self.assertTrue(scene1.has_ended)
        mgr.update()
        self.assertEqual(scene1.state, scene.SCENE_RUNNING)
        self.assertTrue(scene1.is_running)
        self.assertEqual(started[0], scene1)

        mgr.pause()
        self.assertEqual(scene1.state, scene.SCENE_PAUSED)
        self.assertTrue(scene1.is_paused)
        self.assertEqual(paused[0], scene1)
        self.assertEqual(started[0], scene1)

        mgr.unpause()
        self.assertEqual(scene1.state, scene.SCENE_RUNNING)
        self.assertTrue(scene1.is_running)
        self.assertEqual(paused[0], scene1)
        self.assertEqual(started[0], scene1)
        self.assertEqual(unpaused[0], scene1)

        mgr.push(scene2)
        self.assertEqual(scene1.state, scene.SCENE_RUNNING)
        self.assertTrue(scene1.is_running)
        self.assertEqual(mgr.current, scene1)
        self.assertEqual(mgr.next, scene2)

        paused = []
        started = []
        unpaused = []

        mgr.update()
        self.assertEqual(scene1.state, scene.SCENE_ENDED)
        self.assertTrue(scene1.has_ended)
        self.assertEqual(started[0], scene2)
        self.assertEqual(scene2.state, scene.SCENE_RUNNING)
        self.assertTrue(scene2.is_running)
        self.assertEqual(ended[0], scene1)
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, None)

        paused = []
        started = []
        unpaused = []
        ended = []

        mgr.pop()
        self.assertEqual(mgr.current, scene2)
        self.assertEqual(mgr.next, scene1)
        mgr.update()
        self.assertEqual(scene2.state, scene.SCENE_ENDED)
        self.assertTrue(scene2.has_ended)
        self.assertEqual(ended[0], scene2)
        self.assertEqual(scene1.state, scene.SCENE_RUNNING)
        self.assertTrue(scene1.is_running)
        self.assertEqual(started[0], scene1)

    def test_Scene(self):
        sc = scene.Scene()
        self.assertIsInstance(sc, scene.Scene)
        self.assertIsNone(sc.name)
        self.assertEqual(sc.state, scene.SCENE_ENDED)
        self.assertIsInstance(sc.started, EventHandler)
        self.assertIsInstance(sc.paused, EventHandler)
        self.assertIsInstance(sc.unpaused, EventHandler)
        self.assertIsInstance(sc.ended, EventHandler)

        sc = scene.Scene("test")
        self.assertIsInstance(sc, scene.Scene)
        self.assertEqual(sc.name, "test")

    def test_Scene_start_pause_unpause_end(self):
        sc = scene.Scene()
        self.assertEqual(sc.state, scene.SCENE_ENDED)

        # Starting
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)

        # Restart
        sc.end()
        self.assertEqual(sc.state, scene.SCENE_ENDED)
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)
        sc.end()
        self.assertEqual(sc.state, scene.SCENE_ENDED)

        # Pause/start
        sc.pause()
        self.assertEqual(sc.state, scene.SCENE_ENDED)
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)
        sc.pause()
        self.assertEqual(sc.state, scene.SCENE_PAUSED)
        sc.start()
        self.assertEqual(sc.state, scene.SCENE_PAUSED)
        sc.unpause()
        self.assertEqual(sc.state, scene.SCENE_RUNNING)
        sc.end()
        self.assertEqual(sc.state, scene.SCENE_ENDED)

    def test_Scene_is_running_is_paused_has_ended(self):
        sc = scene.Scene()
        self.assertEqual(sc.state, scene.SCENE_ENDED)
        self.assertFalse(sc.is_running)
        self.assertFalse(sc.is_paused)
        self.assertTrue(sc.has_ended)
        sc.start()
        self.assertTrue(sc.is_running)
        self.assertFalse(sc.is_paused)
        self.assertFalse(sc.has_ended)
        sc.pause()
        self.assertFalse(sc.is_running)
        self.assertTrue(sc.is_paused)
        self.assertFalse(sc.has_ended)
        sc.unpause()
        self.assertTrue(sc.is_running)
        self.assertFalse(sc.is_paused)
        self.assertFalse(sc.has_ended)
        sc.end()
        self.assertFalse(sc.is_running)
        self.assertFalse(sc.is_paused)
        self.assertTrue(sc.has_ended)


if __name__ == '__main__':
    sys.exit(unittest.main())
