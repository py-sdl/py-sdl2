"""Particle simulation"""
import sys
import ctypes
import random

# Try to import SDL2. The import might fail, if the SDL2 DLL could
# not be loaded. In that case, just print the error and exit with a
# proper error code.
try:
    import sdl2.ext as sdl2ext
    import sdl2.events as sdlevents
    import sdl2.mouse as sdlmouse
    import sdl2.timer as sdltimer
    import sdl2.render as sdlrender
    import sdl2.rect as sdlrect
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import the particles module, so we have access to all relevant parts
# for dealing with particles.
import sdl2.ext.particles as particles
# We will create some systems and an entity for creating the particle
# simulation. Hence we will need some things from the ebs module.
from sdl2.ext.ebs import Entity, System, World


# Import the resources, so we have easy access to the example images.
from sdl2.ext.resources import Resources
RESOURCES = Resources(__file__, "resources")


# The Particle class offered by sdl2.ext.particles only contains the life
# time information of the particle, which will be decreased by one each
# time the particle engine processes it as well as a x- and
# y-coordinate. This is not enough for us, since we want them to have a
# velocity as well to make moving them around easier. Also, each
# particle can look different for us, so we also store some information
# about the image to display on rendering in ptype.
#
# If particles run out of life, we want to remove them, since we do not
# want to flood our world with unused entities. Thus, we store a
# reference to the entity, the particle belongs to, too. This allows use
# to remove them easily later on.
class CParticle(particles.Particle):
    def __init__(self, entity, x, y, vx, vy, ptype, life):
        super(CParticle, self).__init__(x, y, life)
        self.entity = entity
        self.type = ptype
        self.vx = vx
        self.vy = vy


# A simple Entity class, that contains the particle information. This
# represents our living particle object.
class EParticle(Entity):
    def __init__(self, world, x, y, vx, vy, ptype, life):
        self.cparticle = CParticle(self, x, y, vx, vy, ptype, life)


# A callback function for creating new particles. It is needed by the
# ParticleEngine and the requirements are explained below.
def createparticles(world, deadones, count=None):
    if deadones is not None:
        count = len(deadones)
    # Create a replacement for each particle that died. The particle
    # will be created at the current mouse cursor position (explained
    # below) with a random velocity, life time, and image to be
    # displayed.
    for c in range(count):
        x = world.mousex
        y = world.mousey
        vx = random.random() * 3 - 1
        vy = random.random() * 3 - 1
        life = random.randint(20, 100)
        ptype = random.randint(0, 2)  # 0-2 denote the image to be used
        # We do not need to assign the particle to a variable, since it
        # will be added to the World and we do not need to do perform
        # any post-creation operations.
        EParticle(world, x, y, vx, vy, ptype, life)


# A callback function for updating particles. It is needed by the
# ParticleEngine and the requirements are explained below.
def updateparticles(world, particles):
    # For each existing, living particle, move it to a new location,
    # based on its velocity.
    for p in particles:
        p.x += p.vx
        p.y += p.vy


# A callback function for deleting particles. It is neede by the
# ParticleEngine and the requirements are explained below.
def deleteparticles(world, deadones):
    # As written in the comment for the CParticle class, we will use the
    # stored entity reference of the dead particle components to delete
    # the dead particles from the world.
    world.delete_entities(p.entity for p in deadones)


# Create a simple rendering system for particles. This is somewhat
# similar to the TextureSprinteRenderer from mule.video. Since we
# operate on particles rather than sprites, we need to provide our own
# rendering logic.
class ParticleRenderer(System):
    def __init__(self, renderer, images):
        # Create a new particle renderer. The surface argument will be
        # the targets surface to do the rendering on. images is a set of
        # images to be used for rendering the particles.
        super(ParticleRenderer, self).__init__()
        # Define, what component instances are processed by the
        # ParticleRenderer.
        self.componenttypes = (CParticle,)
        self.renderer = renderer
        self.images = images

    def process(self, world, components):
        # Processing code that will render all existing CParticle
        # components that currently exist in the world. We have a 1:1
        # mapping between the created particle entities and associated
        # particle components; that said, we render all created
        # particles here.

        # We deal with quite a set of items, so we create some shortcuts
        # to save Python the time to look things up.
        #
        # The SDL_Rect is used for the blit operation below and is used
        # as destination position for rendering the particle.
        r = sdlrect.SDL_Rect()

        # The SDL2 blit function to use. This will take an image
        # (SDL_Texture) as source and copies it on the target.
        dorender = sdlrender.SDL_RenderCopy

        # And some more shortcuts.
        sdlrenderer = self.renderer.renderer
        images = self.images
        # Before rendering all particles, make sure the old ones are
        # removed from the window by filling it with a black color.
        self.renderer.clear(0x0)

        # Render all particles.
        for particle in components:
            # Set the correct destination position for the particle
            r.x = int(particle.x)
            r.y = int(particle.y)

            # Select the correct image for the particle.
            img = images[particle.type]
            r.w, r.h = img.size
            # Render (or blit) the particle by using the designated image.
            dorender(sdlrenderer, img.texture, None, r)
        self.renderer.present()

def run():
    # Create the environment, in which our particles will exist.
    world = World()

    # Set up the globally available information about the current mouse
    # position. We use that information to determine the emitter
    # location for new particles.
    world.mousex = 400
    world.mousey = 300

    # Create the particle engine. It is just a simple System that uses
    # callback functions to update a set of components.
    engine = particles.ParticleEngine()

    # Bind the callback functions to the particle engine. The engine
    # does the following on processing:
    # 1) reduce the life time of each particle by one
    # 2) create a list of particles, which's life time is 0 or below.
    # 3) call createfunc() with the world passed to process() and
    #    the list of dead particles
    # 4) call updatefunc() with the world passed to process() and the
    #    set of particles, which still are alive.
    # 5) call deletefunc() with the world passed to process() and the
    #    list of dead particles. deletefunc() is respsonible for
    #    removing the dead particles from the world.
    engine.createfunc = createparticles
    engine.updatefunc = updateparticles
    engine.deletefunc = deleteparticles
    world.add_system(engine)

    # We create all particles at once before starting the processing.
    # We also could create them in chunks to have a visually more
    # appealing effect, but let's keep it simple.
    createparticles(world, None, 300)

    # Initialize the video subsystem, create a window and make it visible.
    sdl2ext.init()
    window = sdl2ext.Window("Particles", size=(800, 600))
    window.show()

    renderer = sdl2ext.RenderContext(window)
    factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)

    # Create a set of images to be used as particles on rendering. The
    # images are used by the ParticleRenderer created below.
    images = (factory.from_image(RESOURCES.get_path("circle.png")),
              factory.from_image(RESOURCES.get_path("square.png")),
              factory.from_image(RESOURCES.get_path("star.png"))
              )

    # Center the mouse on the window. We use the SDL2 functions directly
    # here. Since the SDL2 functions do not know anything about the
    # video.Window class, we have to pass the window's SDL_Window to it.
    sdlmouse.SDL_WarpMouseInWindow(window.window, world.mousex, world.mousey)

    # Hide the mouse cursor, os it does not show up - just show the
    # particles.
    sdlmouse.SDL_ShowCursor(0)

    # Create the rendering system for the particles. This is somewhat
    # similar to the SoftSpriteRenderer, but since we only operate with
    # hundreds of particles (and not sprites with all their overhead),
    # we need an own rendering system.
    particlerenderer = ParticleRenderer(renderer, images)
    world.add_system(particlerenderer)

    # The almighty event loop. You already know several parts of it.
    running = True
    while running:
        for event in sdl2ext.get_events():
            if event.type == sdlevents.SDL_QUIT:
                running = False
                break

            if event.type == sdlevents.SDL_MOUSEMOTION:
                # Take care of the mouse motions here. Every time the
                # mouse is moved, we will make that information globally
                # available to our application environment by updating
                # the world attributes created earlier.
                world.mousex = event.motion.x
                world.mousey = event.motion.y
                # We updated the mouse coordinates once, ditch all the
                # other ones. Since world.process() might take several
                # milliseconds, new motion events can occur on the event
                # queue (10ths to 100ths!), and we do not want to handle
                # each of them. For this example, it is enough to handle
                # one per update cycle.
                sdlevents.SDL_FlushEvent(sdlevents.SDL_MOUSEMOTION)
                break
        world.process()

    sdl2ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
