from ctypes import Structure, Union, POINTER, c_int, c_uint, c_float, c_char_p
from .dll import _bind
from .stdinc import Uint8, Uint16, Uint32, Sint16, Sint32
from .joystick import SDL_Joystick

class SDL_Haptic(Structure):
    pass

SDL_HAPTIC_CONSTANT = 1 << 0
SDL_HAPTIC_SINE = 1 << 1
SDL_HAPTIC_SQUARE = 1 << 2
SDL_HAPTIC_TRIANGLE = 1 << 3
SDL_HAPTIC_SAWTOOTHUP = 1 << 4
SDL_HAPTIC_SAWTOOTHDOWN = 1 << 5
SDL_HAPTIC_RAMP = 1 << 6
SDL_HAPTIC_SPRING = 1 << 7
SDL_HAPTIC_DAMPER = 1 << 8
SDL_HAPTIC_INERTIA = 1 << 9
SDL_HAPTIC_FRICTION = 1 << 10
SDL_HAPTIC_CUSTOM = 1 << 11
SDL_HAPTIC_GAIN = 1 << 12
SDL_HAPTIC_AUTOCENTER = 1 << 13
SDL_HAPTIC_STATUS = 1 << 14
SDL_HAPTIC_PAUSE = 1 << 15
SDL_HAPTIC_POLAR = 0
SDL_HAPTIC_CARTESIAN = 1
SDL_HAPTIC_SPHERICAL = 2
SDL_HAPTIC_INFINITY = 4294967295L

class SDL_HapticDirection(Structure):
    _fields_ = [("type", Uint8), ("dir", (Sint32 * 3))]

class SDL_HapticConstant(Structure):
    _fields_ = [("type", Uint16),
                ("direction", SDL_HapticDirection),
                ("length", Uint32),
                ("delay", Uint16),
                ("button", Uint16),
                ("interval", Uint16),
                ("level", Sint16),
                ("attack_length", Uint16),
                ("attack_level", Uint16),
                ("fade_length", Uint16),
                ("fade_level", Uint16),
                ]


class SDL_HapticPeriodic(Structure):
    _fields_ = [("type", Uint16),
                ("direction", SDL_HapticDirection),
                ("length", Uint32),
                ("delay", Uint16),
                ("button", Uint16),
                ("interval", Uint16),
                ("period", Uint16),
                ("magnitude", Sint16),
                ("offset", Sint16),
                ("phase", Uint16),
                ("attack_length", Uint16),
                ("attack_level", Uint16),
                ("fade_length", Uint16),
                ("fade_level", Uint16),
                ]


class SDL_HapticCondition(Structure):
    """A conditionally running effect."""
    _fields_ = [("type", Uint16),
                ("direction", SDL_HapticDirection),
                ("length", Uint32),
                ("delay", Uint16),
                ("button", Uint16),
                ("interval", Uint16),
                ("right_sat", (Uint16 * 3)),
                ("left_sat", (Uint16 * 3)),
                ("right_coeff", (Sint16 * 3)),
                ("left_coeff", (Sint16 * 3)),
                ("deadband", (Uint16 * 3)),
                ("center", (Sint16 * 3)),
                ]


class SDL_HapticRamp(Structure):
    """A ramp-like effect."""
    _fields_ = [("type", Uint16),
                ("direction", SDL_HapticDirection),
                ("length", Uint32),
                ("delay", Uint16),
                ("button", Uint16),
                ("interval", Uint16),
                ("start", Sint16),
                ("end", Sint16),
                ("attack_length", Uint16),
                ("attack_level", Uint16),
                ("fade_length", Uint16),
                ("fade_level", Uint16),
                ]


class SDL_HapticCustom(Structure):
    """A custom effect."""
    _fields_ = [("type", Uint16),
                ("direction", SDL_HapticDirection),
                ("length", Uint32),
                ("delay", Uint16),
                ("button", Uint16),
                ("interval", Uint16),
                ("channels", Uint8),
                ("period", Uint16),
                ("samples", Uint16),
                ("data", POINTER(Uint16)),
                ("attack_length", Uint16),
                ("attack_level", Uint16),
                ("fade_length", Uint16),
                ("fade_level", Uint16),
                ]


class SDL_HapticEffect(Union):
    """A generic haptic effect, containing the concrete haptic effect."""
    _fields_ = [("type", Uint16),
                ("constant", SDL_HapticConstant),
                ("periodic", SDL_HapticPeriodic),
                ("condition", SDL_HapticCondition),
                ("ramp", SDL_HapticRamp),
                ("custom", SDL_HapticCustom),
                ]

SDL_NumHaptics = _bind("SDL_NumHaptics", None, c_int)
SDL_HapticName = _bind("SDL_HapticName", [c_int], c_char_p)
SDL_HapticOpen = _bind("SDL_HapticOpen", [c_int], POINTER(SDL_Haptic))
SDL_HapticOpened = _bind("SDL_HapticOpened", [c_int], c_int)
SDL_HapticIndex = _bind("SDL_HapticIndex", [POINTER(SDL_Haptic)], c_int)
SDL_MouseIsHaptic = _bind("SDL_MouseIsHaptic", None, c_int)
SDL_HapticOpenFromMouse = _bind("SDL_HapticOpenFromMouse", None, POINTER(SDL_Haptic))
SDL_JoystickIsHaptic = _bind("SDL_JoystickIsHaptic", [POINTER(SDL_Joystick)], c_int)
SDL_HapticOpenFromJoystick = _bind("SDL_HapticOpenFromJoystick", [POINTER(SDL_Joystick)], POINTER(SDL_Haptic))
SDL_HapticClose = _bind("SDL_HapticClose", [POINTER(SDL_Haptic)])
SDL_HapticNumEffects = _bind("SDL_HapticNumEffects", [POINTER(SDL_Haptic)], c_int)
SDL_HapticNumEffectsPlaying = _bind("SDL_HapticNumEffectsPlaying", [POINTER(SDL_Haptic)], c_int)
SDL_HapticQuery = _bind("SDL_HapticQuery", [POINTER(SDL_Haptic)], c_uint)
SDL_HapticNumAxes = _bind("SDL_HapticNumAxes", [POINTER(SDL_Haptic)], c_int)
SDL_HapticEffectSupported = _bind("SDL_HapticEffectSupported", [POINTER(SDL_Haptic), POINTER(SDL_HapticEffect)], c_int)
SDL_HapticNewEffect = _bind("SDL_HapticNewEffect", [POINTER(SDL_Haptic), POINTER(SDL_HapticEffect)], c_int)
SDL_HapticUpdateEffect = _bind("SDL_HapticUpdateEffect", [POINTER(SDL_Haptic), c_int, POINTER(SDL_HapticEffect)], c_int)
SDL_HapticRunEffect = _bind("SDL_HapticRunEffect", [POINTER(SDL_Haptic), c_int, Uint32], c_int)
SDL_HapticStopEffect = _bind("SDL_HapticStopEffect", [POINTER(SDL_Haptic), c_int], c_int)
SDL_HapticDestroyEffect = _bind("SDL_HapticDestroyEffect", [POINTER(SDL_Haptic), c_int])
SDL_HapticGetEffectStatus = _bind("SDL_HapticGetEffectStatus", [POINTER(SDL_Haptic), c_int], c_int)
SDL_HapticSetGain = _bind("SDL_HapticSetGain", [POINTER(SDL_Haptic), c_int], c_int)
SDL_HapticSetAutocenter = _bind("SDL_HapticSetAutocenter", [POINTER(SDL_Haptic), c_int], c_int)
SDL_HapticPause = _bind("SDL_HapticPause", [POINTER(SDL_Haptic)], c_int)
SDL_HapticUnpause = _bind("SDL_HapticUnpause", [POINTER(SDL_Haptic)], c_int)
SDL_HapticStopAll = _bind("SDL_HapticStopAll", [POINTER(SDL_Haptic)], c_int)
SDL_HapticRumbleSupported = _bind("SDL_HapticRumbleSupported", [POINTER(SDL_Haptic)], c_int)
SDL_HapticRumbleInit = _bind("SDL_HapticRumbleInit", [POINTER(SDL_Haptic)], c_int)
SDL_HapticRumblePlay = _bind("SDL_HapticRumblePlay", [POINTER(SDL_Haptic), c_float, Uint32], c_int)
SDL_HapticRumbleStop = _bind("SDL_HapticRumbleStop", [POINTER(SDL_Haptic)], c_int)
