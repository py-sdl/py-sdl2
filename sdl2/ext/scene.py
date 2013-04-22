"""
A simple scene system.

sdl2.ext.scene implements a simple scene system, which combines different
scenes or screens and allows you to switch between them.
"""
from .events import EventHandler

__all__ = ["Scene", "SceneManager", "SCENE_ENDED", "SCENE_RUNNING",
           "SCENE_PAUSED"
           ]


SCENE_ENDED = 0
SCENE_RUNNING = 1
SCENE_PAUSED = 2


class SceneManager(object):
    """A scene management system.

    The SceneManager takes care of scene transitions, preserving scene
    states and everything else to maintain and ensure the control flow
    between different scenes.
    """
    def __init__(self):
        """Creates a new SceneManager."""
        self.scenes = []
        self.next = None
        self.current = None
        self.switched = EventHandler(self)

    def push(self, scene):
        """Pushes a new scene to the scene stack.

        The current scene will be put on the scene stack for later
        execution, while the passed scene will be set as current one.
        Once the newly pushed scene has ended or was paused, the
        previous scene will continue its execution.
        """
        self.next = scene
        if self.current:
            self.scenes.append(self.current)

    def pop(self):
        """Pops a scene from the scene stack, bringing it into place for
        being executed on the next update."""
        if len(self.scenes) == 0:
            return
        self.next = self.scenes.pop()

    def pause(self):
        """Pauses the currently running scene."""
        if self.current:
            self.current.pause()

    def unpause(self):
        """Unpauses the current scene."""
        if self.current:
            self.current.unpause()

    def update(self):
        """Updates the scene state.

        Updates the scene state and switches to the next scene, if any
        has been pushed into place.
        """
        if self.next:
            # A scene is about to be started, finish the old one
            if self.current and self.current.is_running:
                self.current.end()
                self.current.manager = None
            self.current = self.next
            self.current.manager = self
            self.next = None
            self.switched()
        if self.current and self.current.has_ended:
            self.current.start()


class Scene(object):
    """A simple scene state object used to maintain the application workflow
    based on the presentation of an application.
    """
    def __init__(self, name=None):
        """Creates a new Scene."""
        self.name = name
        self.manager = None
        self.state = SCENE_ENDED
        self.started = EventHandler(self)
        self.paused = EventHandler(self)
        self.unpaused = EventHandler(self)
        self.ended = EventHandler(self)

    def __repr__(self):
        states = ("ENDED", "RUNNING", "PAUSED")
        return "Scene(name='%s', state='%s')" % (self.name, states[self.state])

    def start(self):
        """Executed, whenever the scene starts.

        This is usually invoked by the SceneManager and will update the
        scene's internal state and executes the started event.
        """
        if self.state not in (SCENE_RUNNING, SCENE_PAUSED):
            self.state = SCENE_RUNNING
            self.started()

    def pause(self):
        """Executed, whenever the scene is paused.

        This is usually invoked by the SceneManager and will update the
        scene's internal state and executes the paused event.
        """
        if self.state == SCENE_RUNNING:
            self.state = SCENE_PAUSED
            self.paused()

    def unpause(self):
        """Executed, whenever the scene is unpaused.

        This is usually invoked by the SceneManager and will update the
        scene's internal state and executes the unpaused event.
        """
        if self.state == SCENE_PAUSED:
            self.state = SCENE_RUNNING
            self.unpaused()

    def end(self):
        """Executed, whenever the scene ends.

        This is usually invoked by the SceneManager and will update the
        scene's internal state and executes the ended event.
        """
        if self.state != SCENE_ENDED:
            self.state = SCENE_ENDED
            self.ended()

    @property
    def is_running(self):
        """True, if the scene is currently running, False otherwise."""
        return self.state == SCENE_RUNNING

    @property
    def is_paused(self):
        """True, if the scene is currently paused, False otherwise."""
        return self.state == SCENE_PAUSED

    @property
    def has_ended(self):
        """True, if the scene has ended, False otherwise."""
        return self.state == SCENE_ENDED
