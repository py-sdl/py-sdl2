from ctypes import c_char_p, c_int, c_float, c_void_p
from ctypes import POINTER as _P
from .dll import _bind
from .stdinc import Uint32


__all__ = [
    # Structs
    "SDL_Sensor",

    # Defines
    "SDL_SensorID", "SDL_STANDARD_GRAVITY",

    # Enums
    "SDL_SensorType",
    "SDL_SENSOR_INVALID", "SDL_SENSOR_UNKNOWN", "SDL_SENSOR_ACCEL",
    "SDL_SENSOR_GYRO",

    # Functions
    "SDL_LockSensors", "SDL_UnlockSensors", "SDL_NumSensors",
    "SDL_SensorGetDeviceName", "SDL_SensorGetDeviceType",
    "SDL_SensorGetDeviceNonPortableType", "SDL_SensorGetDeviceInstanceID",
    "SDL_SensorOpen", "SDL_SensorFromInstanceID", "SDL_SensorGetName",
    "SDL_SensorGetType", "SDL_SensorGetNonPortableType",
    "SDL_SensorGetInstanceID", "SDL_SensorGetData", "SDL_SensorClose",
    "SDL_SensorUpdate"
]


# Constants & enums

SDL_SensorType = c_int
SDL_SENSOR_INVALID = -1
SDL_SENSOR_UNKNOWN = 0
SDL_SENSOR_ACCEL = 1
SDL_SENSOR_GYRO = 2

SDL_STANDARD_GRAVITY = 9.80665


# Structs & typedefs

SDL_SensorID = Uint32

class SDL_Sensor(c_void_p):
    pass



SDL_LockSensors = _bind("SDL_LockSensors", None, None, added='2.0.14')
SDL_UnlockSensors = _bind("SDL_UnlockSensors", None, None, added='2.0.14')
SDL_NumSensors = _bind("SDL_NumSensors", None, c_int, added='2.0.9')
SDL_SensorGetDeviceName = _bind("SDL_SensorGetDeviceName", [c_int], c_char_p, added='2.0.9')
SDL_SensorGetDeviceType = _bind("SDL_SensorGetDeviceType", [c_int], SDL_SensorType, added='2.0.9')
SDL_SensorGetDeviceNonPortableType = _bind("SDL_SensorGetDeviceNonPortableType", [c_int], c_int, added='2.0.9')
SDL_SensorGetDeviceInstanceID = _bind("SDL_SensorGetDeviceInstanceID", [c_int], SDL_SensorID, added='2.0.9')
SDL_SensorOpen = _bind("SDL_SensorOpen", [c_int], _P(SDL_Sensor), added='2.0.9')
SDL_SensorFromInstanceID = _bind("SDL_SensorFromInstanceID", [SDL_SensorID], _P(SDL_Sensor), added='2.0.9')
SDL_SensorGetName = _bind("SDL_SensorGetName", [_P(SDL_Sensor)], c_char_p, added='2.0.9')
SDL_SensorGetType = _bind("SDL_SensorGetType", [_P(SDL_Sensor)], SDL_SensorType, added='2.0.9')
SDL_SensorGetNonPortableType = _bind("SDL_SensorGetNonPortableType", [_P(SDL_Sensor)], c_int, added='2.0.9')
SDL_SensorGetInstanceID = _bind("SDL_SensorGetInstanceID", [_P(SDL_Sensor)], SDL_SensorID, added='2.0.9')
SDL_SensorGetData = _bind("SDL_SensorGetData", [_P(SDL_Sensor), _P(c_float), c_int], c_int, added='2.0.9') # Needs testing
SDL_SensorClose = _bind("SDL_SensorClose", [_P(SDL_Sensor)], None, added='2.0.9')
SDL_SensorUpdate = _bind("SDL_SensorUpdate", None, None, added='2.0.9')
