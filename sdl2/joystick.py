from ctypes import Structure, c_int, c_char_p, POINTER
from .dll import _bind, nullfunc
from .stdinc import Sint16, Sint32, Uint16, Uint8, SDL_bool

__all__ = ["SDL_Joystick", "SDL_JoystickGUID", "SDL_JoystickID",
           "SDL_NumJoysticks", "SDL_JoystickNameForIndex", "SDL_JoystickOpen",
           "SDL_JoystickName", "SDL_JoystickGetDeviceGUID",
           "SDL_JoystickGetGUID", "SDL_JoystickGetGUIDString",
           "SDL_JoystickGetGUIDFromString", "SDL_JoystickGetAttached",
           "SDL_JoystickInstanceID", "SDL_JoystickNumAxes",
           "SDL_JoystickNumBalls", "SDL_JoystickNumHats",
           "SDL_JoystickNumButtons", "SDL_JoystickUpdate",
           "SDL_JoystickEventState", "SDL_JoystickGetAxis", "SDL_HAT_CENTERED",
           "SDL_HAT_UP", "SDL_HAT_RIGHT", "SDL_HAT_DOWN", "SDL_HAT_LEFT",
           "SDL_HAT_RIGHTUP", "SDL_HAT_RIGHTDOWN", "SDL_HAT_LEFTUP",
           "SDL_HAT_LEFTDOWN", "SDL_JoystickGetHat", "SDL_JoystickGetBall",
           "SDL_JoystickGetButton", "SDL_JoystickClose",
           "SDL_JOYSTICK_POWER_UNKNOWN", "SDL_JOYSTICK_POWER_EMPTY",
           "SDL_JOYSTICK_POWER_LOW", "SDL_JOYSTICK_POWER_MEDIUM",
           "SDL_JOYSTICK_POWER_FULL", "SDL_JOYSTICK_POWER_WIRED",
           "SDL_JOYSTICK_POWER_MAX", "SDL_JoystickPowerLevel",
           "SDL_JoystickCurrentPowerLevel", "SDL_JoystickFromInstanceID",
           "SDL_JoystickGetVendor", "SDL_JoystickGetProductVersion",
           "SDL_JoystickGetProduct", "SDL_JoystickGetAxisInitialState",
           "SDL_JoystickType", "SDL_JOYSTICK_TYPE_UNKNOWN",
           "SDL_JOYSTICK_TYPE_GAMECONTROLLER", "SDL_JOYSTICK_TYPE_WHEEL",
           "SDL_JOYSTICK_TYPE_ARCADE_STICK", "SDL_JOYSTICK_TYPE_FLIGHT_STICK",
           "SDL_JOYSTICK_TYPE_DANCE_PAD", "SDL_JOYSTICK_TYPE_GUITAR",
           "SDL_JOYSTICK_TYPE_DRUM_KIT", "SDL_JOYSTICK_TYPE_ARCADE_PAD",
           "SDL_JOYSTICK_TYPE_THROTTLE",
           "SDL_JoystickGetDeviceType", "SDL_JoystickGetType",
           "SDL_JoystickGetDeviceInstanceID", "SDL_LockJoysticks",
           "SDL_UnlockJoysticks"
          ]

SDL_JoystickPowerLevel = c_int

SDL_JOYSTICK_POWER_UNKNOWN = -1
SDL_JOYSTICK_POWER_EMPTY = 0
SDL_JOYSTICK_POWER_LOW = 1
SDL_JOYSTICK_POWER_MEDIUM = 2
SDL_JOYSTICK_POWER_FULL = 3
SDL_JOYSTICK_POWER_WIRED = 4
SDL_JOYSTICK_POWER_MAX = 5

SDL_JoystickType = c_int

SDL_JOYSTICK_TYPE_UNKNOWN = 0
SDL_JOYSTICK_TYPE_GAMECONTROLLER = 1
SDL_JOYSTICK_TYPE_WHEEL = 2
SDL_JOYSTICK_TYPE_ARCADE_STICK = 3
SDL_JOYSTICK_TYPE_FLIGHT_STICK = 4
SDL_JOYSTICK_TYPE_DANCE_PAD = 5
SDL_JOYSTICK_TYPE_GUITAR = 6
SDL_JOYSTICK_TYPE_DRUM_KIT = 7
SDL_JOYSTICK_TYPE_ARCADE_PAD = 8
SDL_JOYSTICK_TYPE_THROTTLE = 9


class SDL_Joystick(Structure):
    pass

class SDL_JoystickGUID(Structure):
    _fields_ = [("data", (Uint8 * 16))]

SDL_JoystickID = Sint32

SDL_NumJoysticks = _bind("SDL_NumJoysticks", None, c_int)
SDL_JoystickNameForIndex = _bind("SDL_JoystickNameForIndex", [c_int], c_char_p)
SDL_JoystickOpen = _bind("SDL_JoystickOpen", [c_int], POINTER(SDL_Joystick))
SDL_JoystickName = _bind("SDL_JoystickName", [POINTER(SDL_Joystick)], c_char_p)
SDL_JoystickGetDeviceGUID = _bind("SDL_JoystickGetDeviceGUID", [c_int], SDL_JoystickGUID)
SDL_JoystickGetGUID = _bind("SDL_JoystickGetGUID", [POINTER(SDL_Joystick)], SDL_JoystickGUID)
SDL_JoystickGetGUIDString = _bind("SDL_JoystickGetGUIDString", [SDL_JoystickGUID, c_char_p, c_int])
SDL_JoystickGetGUIDFromString = _bind("SDL_JoystickGetGUIDFromString", [c_char_p], SDL_JoystickGUID)
SDL_JoystickGetAttached = _bind("SDL_JoystickGetAttached", [POINTER(SDL_Joystick)], SDL_bool)
SDL_JoystickInstanceID = _bind("SDL_JoystickInstanceID", [POINTER(SDL_Joystick)], SDL_JoystickID)
SDL_JoystickNumAxes = _bind("SDL_JoystickNumAxes", [POINTER(SDL_Joystick)], c_int)
SDL_JoystickNumBalls = _bind("SDL_JoystickNumBalls", [POINTER(SDL_Joystick)], c_int)
SDL_JoystickNumHats = _bind("SDL_JoystickNumHats", [POINTER(SDL_Joystick)], c_int)
SDL_JoystickNumButtons = _bind("SDL_JoystickNumButtons", [POINTER(SDL_Joystick)], c_int)
SDL_JoystickUpdate = _bind("SDL_JoystickUpdate")
SDL_JoystickEventState = _bind("SDL_JoystickEventState", [c_int], c_int)
SDL_JoystickGetAxis = _bind("SDL_JoystickGetAxis", [POINTER(SDL_Joystick), c_int], Sint16)
SDL_HAT_CENTERED = 0x00
SDL_HAT_UP = 0x01
SDL_HAT_RIGHT = 0x02
SDL_HAT_DOWN = 0x04
SDL_HAT_LEFT = 0x08
SDL_HAT_RIGHTUP = SDL_HAT_RIGHT | SDL_HAT_UP
SDL_HAT_RIGHTDOWN = SDL_HAT_RIGHT | SDL_HAT_DOWN
SDL_HAT_LEFTUP = SDL_HAT_LEFT | SDL_HAT_UP
SDL_HAT_LEFTDOWN = SDL_HAT_LEFT | SDL_HAT_DOWN
SDL_JoystickGetHat = _bind("SDL_JoystickGetHat", [POINTER(SDL_Joystick), c_int], Uint8)
SDL_JoystickGetBall = _bind("SDL_JoystickGetBall", [POINTER(SDL_Joystick), c_int, POINTER(c_int), POINTER(c_int)], c_int)
SDL_JoystickGetButton = _bind("SDL_JoystickGetButton", [POINTER(SDL_Joystick), c_int], Uint8)
SDL_JoystickClose = _bind("SDL_JoystickClose", [POINTER(SDL_Joystick)])
SDL_JoystickCurrentPowerLevel = _bind("SDL_JoystickCurrentPowerLevel", [POINTER(SDL_Joystick)], SDL_JoystickPowerLevel)
SDL_JoystickFromInstanceID = _bind("SDL_JoystickFromInstanceID", [SDL_JoystickID], POINTER(SDL_Joystick))
SDL_JoystickGetVendor = _bind("SDL_JoystickGetVendor", [POINTER(SDL_Joystick)], Uint16)
SDL_JoystickGetProduct = _bind("SDL_JoystickGetProduct", [POINTER(SDL_Joystick)], Uint16)
SDL_JoystickGetProductVersion = _bind("SDL_JoystickGetProductVersion", [POINTER(SDL_Joystick)], Uint16)
SDL_JoystickGetAxisInitialState = _bind("SDL_JoystickGetAxisInitialState", [POINTER(SDL_Joystick), c_int, POINTER(Sint16)], SDL_bool)
SDL_JoystickGetType = _bind("SDL_JoystickGetType", [POINTER(SDL_Joystick)], SDL_JoystickType)
SDL_JoystickGetDeviceVendor = _bind("SDL_JoystickGetDeviceVendor", [c_int], Uint16)
SDL_JoystickGetDeviceProduct = _bind("SDL_JoystickGetDeviceProduct", [c_int], Uint16)
SDL_JoystickGetDeviceProductVersion = _bind("SDL_JoystickGetDeviceProductVersion", [c_int], Uint16)
SDL_JoystickGetDeviceType = _bind("SDL_JoystickGetDeviceType", [c_int], SDL_JoystickType)
SDL_JoystickGetDeviceInstanceID = _bind("SDL_JoystickGetDeviceInstanceID", [c_int], SDL_JoystickID)
SDL_LockJoysticks = _bind("SDL_LockJoysticks", None, None, nullfunc)
SDL_UnlockJoysticks = _bind("SDL_UnlockJoysticks", None, None, nullfunc)
