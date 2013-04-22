.. module:: sdl2.ext.scene
   :synopsis: Scene management.

sdl2.ext.scene - Scene management
=================================

.. class:: SceneManager()

   The SceneManager takes care of scene transitions, preserving scene
   states and everything else to maintain and ensure the control flow
   between different scenes.

   .. attribute:: name

      The name of the :class:`Scene`.

   .. attribute:: scenes

      The scene stack.

   .. attribute:: next

      The next :class:`Scene` to run on calling :meth:`update()`.

   .. attribute:: current

      The currently running/active :class:`Scene`.

   .. attribute:: switched
   
      A :class:`mule.events.EventHandler` that is invoked, when a new
      :class:`Scene` is started.
      
   .. method:: push(scene : Scene) -> None

      Pushes a new :class:`Scene` to the scene stack.

      The :attr:`current` scene will be put on the scene stack for later
      execution, while the passed *scene* will be set as current one.
      Once the newly pushed scene has ended or was paused, the previous
      scene will continue its execution.

   .. method:: pop() -> None

      Pops a scene from the scene stack, bringing it into place for
      being executed on the next update.

   .. method:: pause() -> None

      Pauses the :attr:`current` scene.

   .. method:: unpause() -> None

      Continues the :attr:`current` scene.

   .. method:: update() -> None

      Updates the scene state and switches to the next scene, if any has
      been pushed into place.

.. class:: Scene([name=None])

   A simple scene state object used to maintain the application workflow
   based on the presentation of an application.

   .. attribute:: manager
   
      The :class:`SceneManager`, the :class:`Scene` is currently executed on.
      
      .. note::
      
         This will be set automatically on starting the :class:`Scene` by the
         :class:`SceneManager`. If the :class:`Scene` is ended, it will be
         reset.
   
   .. attribute:: state

      The current scene state.

   .. attribute:: started

      A :class:`mule.events.EventHandler` that is invoked, when the
      :class:`Scene` starts.

   .. attribute:: paused

      A :class:`mule.events.EventHandler` that is invoked, when the
      :class:`Scene` is paused.

   .. attribute:: unpaused

      A :class:`mule.events.EventHandler` that is invoked, when the
      :class:`Scene` is unpaused.

   .. attribute:: ended

      A :class:`mule.events.EventHandler` that is invoked, when the
      :class:`Scene` ends.

   .. attribute:: is_running

      Indicates, if the scene is currently running.

   .. attribute:: is_paused

      Indicates, if the scene is currently paused.

   .. attribute:: has_ended

      Indicates, if the scene has ended.

   .. method:: start() -> None

      Starts the :class:`Scene`. If the :class:`Scene` is running or paused,
      nothing will be done.

   .. method:: pause() -> None

      Pauses the :class:`Scene`. If the :class:`Scene` is not running,
      nothing will be done.

   .. method:: unpause() -> None

      Continues the :class:`Scene`. If the :class:`Scene` is not paused,
      nothing will be done.

   .. method:: end() -> None

      Ends the :class:`Scene`. If the :class:`Scene` has ended already,
      nothing will be done.
