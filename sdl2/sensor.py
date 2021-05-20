from ctypes import POINTER, c_char_p, c_int, c_float, c_void_p
from .dll import _bind
from .stdinc import Uint32

# NOTE: Designed for mobile devices, but support for required backend added in
# macOS 10.15 so might eventually be useful for pysdl2


class SDL_Sensor(c_void_p):
    pass

SDL_SensorID = Uint32

SDL_SensorType = c_int
SDL_SENSOR_INVALID = -1
SDL_SENSOR_UNKNOWN = 0
SDL_SENSOR_ACCEL = 1
SDL_SENSOR_GYRO = 2

SDL_STANDARD_GRAVITY = 9.80665

SDL_NumSensors = _bind("SDL_NumSensors", None, c_int, added='2.0.9')
SDL_SensorGetDeviceName = _bind("SDL_SensorGetDeviceName", [c_int], c_char_p, added='2.0.9')
SDL_SensorGetDeviceType = _bind("SDL_SensorGetDeviceType", [c_int], SDL_SensorType, added='2.0.9')
SDL_SensorGetDeviceNonPortableType = _bind("SDL_SensorGetDeviceNonPortableType", [c_int], c_int, added='2.0.9')
SDL_SensorGetDeviceInstanceID = _bind("SDL_SensorGetDeviceInstanceID", [c_int], SDL_SensorID, added='2.0.9')
SDL_SensorOpen = _bind("SDL_SensorOpen", [c_int], POINTER(SDL_Sensor), added='2.0.9')
SDL_SensorFromInstanceID = _bind("SDL_SensorFromInstanceID", [SDL_SensorID], POINTER(SDL_Sensor), added='2.0.9')
SDL_SensorGetName = _bind("SDL_SensorGetName", [POINTER(SDL_Sensor)], c_char_p, added='2.0.9')
SDL_SensorGetType = _bind("SDL_SensorGetType", [POINTER(SDL_Sensor)], SDL_SensorType, added='2.0.9')
SDL_SensorGetNonPortableType = _bind("SDL_SensorGetNonPortableType", [POINTER(SDL_Sensor)], c_int, added='2.0.9')
SDL_SensorGetInstanceID = _bind("SDL_SensorGetInstanceID", [POINTER(SDL_Sensor)], SDL_SensorID, added='2.0.9')
SDL_SensorGetData = _bind("SDL_SensorGetData", [POINTER(SDL_Sensor), POINTER(c_float), c_int], SDL_SensorID, added='2.0.9') # Needs testing
SDL_SensorClose = _bind("SDL_SensorClose", [POINTER(SDL_Sensor)], None, added='2.0.9')
SDL_SensorUpdate = _bind("SDL_SensorUpdate", None, None, added='2.0.9')
