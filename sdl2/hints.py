from ctypes import CFUNCTYPE, c_int, c_char_p, c_void_p
from .dll import _bind, SDLFunc, AttributeDict
from .stdinc import SDL_bool

__all__ = [
    # Constants
    "SDL_HINT_ACCELEROMETER_AS_JOYSTICK",
    "SDL_HINT_ALLOW_ALT_TAB_WHILE_GRABBED",
    "SDL_HINT_ALLOW_TOPMOST",
    "SDL_HINT_ANDROID_APK_EXPANSION_MAIN_FILE_VERSION",
    "SDL_HINT_ANDROID_APK_EXPANSION_PATCH_FILE_VERSION",
    "SDL_HINT_ANDROID_BLOCK_ON_PAUSE",
    "SDL_HINT_ANDROID_BLOCK_ON_PAUSE_PAUSEAUDIO",
    "SDL_HINT_ANDROID_SEPARATE_MOUSE_AND_TOUCH",
    "SDL_HINT_ANDROID_TRAP_BACK_BUTTON",
    "SDL_HINT_APP_NAME",
    "SDL_HINT_APPLE_TV_CONTROLLER_UI_EVENTS",
    "SDL_HINT_APPLE_TV_REMOTE_ALLOW_ROTATION",
    "SDL_HINT_AUDIO_CATEGORY",
    "SDL_HINT_AUDIO_DEVICE_APP_NAME",
    "SDL_HINT_AUDIO_DEVICE_STREAM_NAME",
    "SDL_HINT_AUDIO_DEVICE_STREAM_ROLE",
    "SDL_HINT_AUDIO_RESAMPLING_MODE",
    "SDL_HINT_AUTO_UPDATE_JOYSTICKS",
    "SDL_HINT_AUTO_UPDATE_SENSORS",
    "SDL_HINT_BMP_SAVE_LEGACY_FORMAT",
    "SDL_HINT_DISPLAY_USABLE_BOUNDS",
    "SDL_HINT_EMSCRIPTEN_ASYNCIFY",
    "SDL_HINT_EMSCRIPTEN_KEYBOARD_ELEMENT",
    "SDL_HINT_ENABLE_STEAM_CONTROLLERS",
    "SDL_HINT_EVENT_LOGGING",
    "SDL_HINT_FORCE_RAISEWINDOW",
    "SDL_HINT_FRAMEBUFFER_ACCELERATION",
    "SDL_HINT_GAMECONTROLLERCONFIG",
    "SDL_HINT_GAMECONTROLLERCONFIG_FILE",
    "SDL_HINT_GAMECONTROLLERTYPE",
    "SDL_HINT_GAMECONTROLLER_IGNORE_DEVICES",
    "SDL_HINT_GAMECONTROLLER_IGNORE_DEVICES_EXCEPT",
    "SDL_HINT_GAMECONTROLLER_USE_BUTTON_LABELS",
    "SDL_HINT_GRAB_KEYBOARD",
    "SDL_HINT_IDLE_TIMER_DISABLED",
    "SDL_HINT_IME_INTERNAL_EDITING",
    "SDL_HINT_IME_SHOW_UI",
    "SDL_HINT_IME_SUPPORT_EXTENDED_TEXT",
    "SDL_HINT_IOS_HIDE_HOME_INDICATOR",
    "SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS",
    "SDL_HINT_JOYSTICK_HIDAPI",
    "SDL_HINT_JOYSTICK_HIDAPI_GAMECUBE",
    "SDL_HINT_JOYSTICK_GAMECUBE_RUMBLE_BRAKE",
    "SDL_HINT_JOYSTICK_HIDAPI_JOY_CONS",
    "SDL_HINT_JOYSTICK_HIDAPI_COMBINE_JOY_CONS",
    "SDL_HINT_JOYSTICK_HIDAPI_LUNA",
    "SDL_HINT_JOYSTICK_HIDAPI_NINTENDO_CLASSIC",
    "SDL_HINT_JOYSTICK_HIDAPI_SHIELD",
    "SDL_HINT_JOYSTICK_HIDAPI_PS4",
    "SDL_HINT_JOYSTICK_HIDAPI_PS4_RUMBLE",
    "SDL_HINT_JOYSTICK_HIDAPI_PS5",
    "SDL_HINT_JOYSTICK_HIDAPI_PS5_PLAYER_LED",
    "SDL_HINT_JOYSTICK_HIDAPI_PS5_RUMBLE",
    "SDL_HINT_JOYSTICK_HIDAPI_STADIA",
    "SDL_HINT_JOYSTICK_HIDAPI_STEAM",
    "SDL_HINT_JOYSTICK_HIDAPI_SWITCH",
    "SDL_HINT_JOYSTICK_HIDAPI_SWITCH_HOME_LED",
    "SDL_HINT_JOYSTICK_HIDAPI_JOYCON_HOME_LED",
    "SDL_HINT_JOYSTICK_HIDAPI_SWITCH_PLAYER_LED",
    "SDL_HINT_JOYSTICK_HIDAPI_XBOX",
    "SDL_HINT_JOYSTICK_RAWINPUT",
    "SDL_HINT_JOYSTICK_RAWINPUT_CORRELATE_XINPUT",
    "SDL_HINT_JOYSTICK_HIDAPI_CORRELATE_XINPUT",
    "SDL_HINT_JOYSTICK_ROG_CHAKRAM",
    "SDL_HINT_JOYSTICK_THREAD",
    "SDL_HINT_KMSDRM_REQUIRE_DRM_MASTER",
    "SDL_HINT_JOYSTICK_DEVICE",
    "SDL_HINT_LINUX_DIGITAL_HATS",
    "SDL_HINT_LINUX_HAT_DEADZONES",
    "SDL_HINT_LINUX_JOYSTICK_CLASSIC",
    "SDL_HINT_LINUX_JOYSTICK_DEADZONES",
    "SDL_HINT_MAC_BACKGROUND_APP",
    "SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK",
    "SDL_HINT_MAC_OPENGL_ASYNC_DISPATCH",
    "SDL_HINT_MOUSE_DOUBLE_CLICK_RADIUS",
    "SDL_HINT_MOUSE_DOUBLE_CLICK_TIME",
    "SDL_HINT_MOUSE_FOCUS_CLICKTHROUGH",
    "SDL_HINT_MOUSE_NORMAL_SPEED_SCALE",
    "SDL_HINT_MOUSE_RELATIVE_MODE_CENTER",
    "SDL_HINT_MOUSE_RELATIVE_MODE_WARP",
    "SDL_HINT_MOUSE_RELATIVE_SCALING",
    "SDL_HINT_MOUSE_RELATIVE_SPEED_SCALE",
    "SDL_HINT_MOUSE_RELATIVE_WARP_MOTION",
    "SDL_HINT_MOUSE_TOUCH_EVENTS",
    "SDL_HINT_MOUSE_AUTO_CAPTURE",
    "SDL_HINT_NO_SIGNAL_HANDLERS",
    "SDL_HINT_OPENGL_ES_DRIVER",
    "SDL_HINT_ORIENTATIONS",
    "SDL_HINT_POLL_SENTINEL",
    "SDL_HINT_PREFERRED_LOCALES",
    "SDL_HINT_QTWAYLAND_CONTENT_ORIENTATION",
    "SDL_HINT_QTWAYLAND_WINDOW_FLAGS",
    "SDL_HINT_RENDER_BATCHING",
    "SDL_HINT_RENDER_LINE_METHOD",
    "SDL_HINT_RENDER_DIRECT3D11_DEBUG",
    "SDL_HINT_RENDER_DIRECT3D_THREADSAFE",
    "SDL_HINT_RENDER_DRIVER",
    "SDL_HINT_RENDER_LOGICAL_SIZE_MODE",
    "SDL_HINT_RENDER_OPENGL_SHADERS",
    "SDL_HINT_RENDER_SCALE_QUALITY",
    "SDL_HINT_RENDER_VSYNC",
    "SDL_HINT_RETURN_KEY_HIDES_IME",
    "SDL_HINT_RPI_VIDEO_LAYER",
    "SDL_HINT_SCREENSAVER_INHIBIT_ACTIVITY_NAME",
    "SDL_HINT_THREAD_FORCE_REALTIME_TIME_CRITICAL",
    "SDL_HINT_THREAD_PRIORITY_POLICY",
    "SDL_HINT_THREAD_STACK_SIZE",
    "SDL_HINT_TIMER_RESOLUTION",
    "SDL_HINT_TOUCH_MOUSE_EVENTS",
    "SDL_HINT_VITA_TOUCH_MOUSE_DEVICE",
    "SDL_HINT_TV_REMOTE_AS_JOYSTICK",
    "SDL_HINT_VIDEO_ALLOW_SCREENSAVER",
    "SDL_HINT_VIDEO_DOUBLE_BUFFER",
    "SDL_HINT_VIDEO_EGL_ALLOW_TRANSPARENCY",
    "SDL_HINT_VIDEO_EXTERNAL_CONTEXT",
    "SDL_HINT_VIDEO_HIGHDPI_DISABLED",
    "SDL_HINT_VIDEO_MAC_FULLSCREEN_SPACES",
    "SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS",
    "SDL_HINT_VIDEO_WAYLAND_ALLOW_LIBDECOR",
    "SDL_HINT_VIDEO_WAYLAND_PREFER_LIBDECOR",
    "SDL_HINT_VIDEO_WAYLAND_MODE_EMULATION",
    "SDL_HINT_VIDEO_WINDOW_SHARE_PIXEL_FORMAT",
    "SDL_HINT_VIDEO_FOREIGN_WINDOW_OPENGL",
    "SDL_HINT_VIDEO_FOREIGN_WINDOW_VULKAN",
    "SDL_HINT_VIDEO_WIN_D3DCOMPILER",
    "SDL_HINT_VIDEO_X11_FORCE_EGL",
    "SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR",
    "SDL_HINT_VIDEO_X11_NET_WM_PING",
    "SDL_HINT_VIDEO_X11_WINDOW_VISUALID",
    "SDL_HINT_VIDEO_X11_XINERAMA",
    "SDL_HINT_VIDEO_X11_XRANDR",
    "SDL_HINT_VIDEO_X11_XVIDMODE",
    "SDL_HINT_WAVE_FACT_CHUNK", 
    "SDL_HINT_WAVE_RIFF_CHUNK_SIZE",
    "SDL_HINT_WAVE_TRUNCATION",
    "SDL_HINT_WINDOWS_DISABLE_THREAD_NAMING",
    "SDL_HINT_WINDOWS_ENABLE_MESSAGELOOP",
    "SDL_HINT_WINDOWS_FORCE_MUTEX_CRITICAL_SECTIONS",
    "SDL_HINT_WINDOWS_FORCE_SEMAPHORE_KERNEL",
    "SDL_HINT_WINDOWS_INTRESOURCE_ICON",
    "SDL_HINT_WINDOWS_INTRESOURCE_ICON_SMALL",
    "SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4",
    "SDL_HINT_WINDOWS_USE_D3D9EX",
    "SDL_HINT_WINDOWS_DPI_AWARENESS",
    "SDL_HINT_WINDOWS_DPI_SCALING",
    "SDL_HINT_WINDOW_FRAME_USABLE_WHILE_CURSOR_HIDDEN",
    "SDL_HINT_WINDOW_NO_ACTIVATION_WHEN_SHOWN",
    "SDL_HINT_WINRT_HANDLE_BACK_BUTTON",
    "SDL_HINT_WINRT_PRIVACY_POLICY_LABEL",
    "SDL_HINT_WINRT_PRIVACY_POLICY_URL",
    "SDL_HINT_X11_FORCE_OVERRIDE_REDIRECT",
    "SDL_HINT_XINPUT_ENABLED",
    "SDL_HINT_XINPUT_USE_OLD_JOYSTICK_MAPPING",
    "SDL_HINT_AUDIO_INCLUDE_MONITORS",
    "SDL_HINT_X11_WINDOW_TYPE",
    "SDL_HINT_QUIT_ON_LAST_WINDOW_CLOSE",
    "SDL_HINT_VIDEODRIVER",
    "SDL_HINT_AUDIODRIVER",

    # Enums
    "SDL_HintPriority",
    "SDL_HINT_DEFAULT", "SDL_HINT_NORMAL", "SDL_HINT_OVERRIDE",

    # Callback Functions
    "SDL_HintCallback",
]


# General Runtime Hints

SDL_HINT_APP_NAME = b"SDL_APP_NAME"
SDL_HINT_BMP_SAVE_LEGACY_FORMAT = b"SDL_BMP_SAVE_LEGACY_FORMAT"
SDL_HINT_EVENT_LOGGING = b"SDL_EVENT_LOGGING"
SDL_HINT_NO_SIGNAL_HANDLERS = b"SDL_NO_SIGNAL_HANDLERS"
SDL_HINT_POLL_SENTINEL = b"SDL_POLL_SENTINEL"
SDL_HINT_PREFERRED_LOCALES = b"SDL_PREFERRED_LOCALES"
SDL_HINT_QUIT_ON_LAST_WINDOW_CLOSE = b"SDL_QUIT_ON_LAST_WINDOW_CLOSE"
SDL_HINT_SCREENSAVER_INHIBIT_ACTIVITY_NAME = b"SDL_SCREENSAVER_INHIBIT_ACTIVITY_NAME"
SDL_HINT_THREAD_FORCE_REALTIME_TIME_CRITICAL = b"SDL_THREAD_FORCE_REALTIME_TIME_CRITICAL"
SDL_HINT_THREAD_PRIORITY_POLICY = b"SDL_THREAD_PRIORITY_POLICY"
SDL_HINT_THREAD_STACK_SIZE = b"SDL_THREAD_STACK_SIZE"
SDL_HINT_TIMER_RESOLUTION = b"SDL_TIMER_RESOLUTION"


# Video & Rendering Hints

SDL_HINT_FRAMEBUFFER_ACCELERATION = b"SDL_FRAMEBUFFER_ACCELERATION"
SDL_HINT_OPENGL_ES_DRIVER = b"SDL_OPENGL_ES_DRIVER"
SDL_HINT_RENDER_BATCHING  = b"SDL_RENDER_BATCHING"
SDL_HINT_RENDER_LINE_METHOD = b"SDL_RENDER_LINE_METHOD"
SDL_HINT_RENDER_DRIVER = b"SDL_RENDER_DRIVER"
SDL_HINT_RENDER_LOGICAL_SIZE_MODE = b"SDL_RENDER_LOGICAL_SIZE_MODE"
SDL_HINT_RENDER_OPENGL_SHADERS = b"SDL_RENDER_OPENGL_SHADERS"
SDL_HINT_RENDER_SCALE_QUALITY = b"SDL_RENDER_SCALE_QUALITY"
SDL_HINT_RENDER_VSYNC = b"SDL_RENDER_VSYNC"
SDL_HINT_VIDEODRIVER = b"SDL_VIDEODRIVER"
SDL_HINT_VIDEO_ALLOW_SCREENSAVER = b"SDL_VIDEO_ALLOW_SCREENSAVER"
SDL_HINT_VIDEO_DOUBLE_BUFFER = b"SDL_VIDEO_DOUBLE_BUFFER"
SDL_HINT_VIDEO_EGL_ALLOW_TRANSPARENCY = b"SDL_VIDEO_EGL_ALLOW_TRANSPARENCY"
SDL_HINT_VIDEO_EXTERNAL_CONTEXT = b"SDL_VIDEO_EXTERNAL_CONTEXT"
SDL_HINT_VIDEO_FOREIGN_WINDOW_OPENGL = b"SDL_VIDEO_FOREIGN_WINDOW_OPENGL"
SDL_HINT_VIDEO_FOREIGN_WINDOW_VULKAN = b"SDL_VIDEO_FOREIGN_WINDOW_VULKAN"
SDL_HINT_VIDEO_WAYLAND_ALLOW_LIBDECOR = b"SDL_VIDEO_WAYLAND_ALLOW_LIBDECOR"
SDL_HINT_VIDEO_WAYLAND_PREFER_LIBDECOR = b"SDL_VIDEO_WAYLAND_PREFER_LIBDECOR"
SDL_HINT_VIDEO_WAYLAND_MODE_EMULATION = b"SDL_VIDEO_WAYLAND_MODE_EMULATION"
SDL_HINT_VIDEO_WINDOW_SHARE_PIXEL_FORMAT = b"SDL_VIDEO_WINDOW_SHARE_PIXEL_FORMAT"
SDL_HINT_VIDEO_X11_FORCE_EGL = b"SDL_VIDEO_X11_FORCE_EGL"
SDL_HINT_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR = b"SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"
SDL_HINT_VIDEO_X11_NET_WM_PING = b"SDL_VIDEO_X11_NET_WM_PING"
SDL_HINT_VIDEO_X11_WINDOW_VISUALID = b"SDL_VIDEO_X11_WINDOW_VISUALID"
SDL_HINT_VIDEO_X11_XINERAMA = b"SDL_VIDEO_X11_XINERAMA"
SDL_HINT_VIDEO_X11_XRANDR = b"SDL_VIDEO_X11_XRANDR"
SDL_HINT_VIDEO_X11_XVIDMODE = b"SDL_VIDEO_X11_XVIDMODE"
SDL_HINT_X11_FORCE_OVERRIDE_REDIRECT = b"SDL_X11_FORCE_OVERRIDE_REDIRECT"
SDL_HINT_X11_WINDOW_TYPE = b"SDL_X11_WINDOW_TYPE"


# Audio Hints

SDL_HINT_AUDIODRIVER = b"SDL_AUDIODRIVER"
SDL_HINT_AUDIO_CATEGORY = b"SDL_AUDIO_CATEGORY"
SDL_HINT_AUDIO_DEVICE_APP_NAME = b"SDL_AUDIO_DEVICE_APP_NAME"
SDL_HINT_AUDIO_DEVICE_STREAM_NAME = b"SDL_AUDIO_DEVICE_STREAM_NAME"
SDL_HINT_AUDIO_DEVICE_STREAM_ROLE = b"SDL_AUDIO_DEVICE_STREAM_ROLE"
SDL_HINT_AUDIO_INCLUDE_MONITORS = b"SDL_AUDIO_INCLUDE_MONITORS"
SDL_HINT_AUDIO_RESAMPLING_MODE = b"SDL_AUDIO_RESAMPLING_MODE"
SDL_HINT_WAVE_FACT_CHUNK = b"SDL_WAVE_FACT_CHUNK"
SDL_HINT_WAVE_RIFF_CHUNK_SIZE = b"SDL_WAVE_RIFF_CHUNK_SIZE"
SDL_HINT_WAVE_TRUNCATION = b"SDL_WAVE_TRUNCATION"


# Window Behaviour Hints

SDL_HINT_ALLOW_ALT_TAB_WHILE_GRABBED = b"SDL_ALLOW_ALT_TAB_WHILE_GRABBED"
SDL_HINT_ALLOW_TOPMOST = b"SDL_ALLOW_TOPMOST"
SDL_HINT_DISPLAY_USABLE_BOUNDS = b"SDL_DISPLAY_USABLE_BOUNDS"
SDL_HINT_FORCE_RAISEWINDOW = b"SDL_HINT_FORCE_RAISEWINDOW"
SDL_HINT_QTWAYLAND_CONTENT_ORIENTATION = b"SDL_QTWAYLAND_CONTENT_ORIENTATION"
SDL_HINT_QTWAYLAND_WINDOW_FLAGS = b"SDL_QTWAYLAND_WINDOW_FLAGS"
SDL_HINT_VIDEO_HIGHDPI_DISABLED = b"SDL_VIDEO_HIGHDPI_DISABLED"
SDL_HINT_VIDEO_MINIMIZE_ON_FOCUS_LOSS = b"SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS"
SDL_HINT_WINDOW_FRAME_USABLE_WHILE_CURSOR_HIDDEN = b"SDL_WINDOW_FRAME_USABLE_WHILE_CURSOR_HIDDEN"
SDL_HINT_WINDOW_NO_ACTIVATION_WHEN_SHOWN = b"SDL_WINDOW_NO_ACTIVATION_WHEN_SHOWN"


# Mouse & Keyboard Hints

SDL_HINT_GRAB_KEYBOARD = b"SDL_GRAB_KEYBOARD"
SDL_HINT_IME_INTERNAL_EDITING = b"SDL_IME_INTERNAL_EDITING"
SDL_HINT_IME_SHOW_UI = b"SDL_IME_SHOW_UI"
SDL_HINT_IME_SUPPORT_EXTENDED_TEXT = b"SDL_IME_SUPPORT_EXTENDED_TEXT"
SDL_HINT_MOUSE_AUTO_CAPTURE = b"SDL_MOUSE_AUTO_CAPTURE"
SDL_HINT_MOUSE_DOUBLE_CLICK_RADIUS = b"SDL_MOUSE_DOUBLE_CLICK_RADIUS"
SDL_HINT_MOUSE_DOUBLE_CLICK_TIME = b"SDL_MOUSE_DOUBLE_CLICK_TIME"
SDL_HINT_MOUSE_FOCUS_CLICKTHROUGH = b"SDL_MOUSE_FOCUS_CLICKTHROUGH"
SDL_HINT_MOUSE_NORMAL_SPEED_SCALE = b"SDL_MOUSE_NORMAL_SPEED_SCALE"
SDL_HINT_MOUSE_RELATIVE_MODE_CENTER = b"SDL_MOUSE_RELATIVE_MODE_CENTER"
SDL_HINT_MOUSE_RELATIVE_MODE_WARP = b"SDL_MOUSE_RELATIVE_MODE_WARP"
SDL_HINT_MOUSE_RELATIVE_SCALING = b"SDL_MOUSE_RELATIVE_SCALING"
SDL_HINT_MOUSE_RELATIVE_SPEED_SCALE = b"SDL_MOUSE_RELATIVE_SPEED_SCALE"
SDL_HINT_MOUSE_RELATIVE_WARP_MOTION = b"SDL_MOUSE_RELATIVE_WARP_MOTION"
SDL_HINT_MOUSE_TOUCH_EVENTS = b"SDL_MOUSE_TOUCH_EVENTS"
SDL_HINT_TOUCH_MOUSE_EVENTS = b"SDL_TOUCH_MOUSE_EVENTS"


# Joystick & Gamepad Hints

SDL_HINT_AUTO_UPDATE_JOYSTICKS = b"SDL_AUTO_UPDATE_JOYSTICKS"
SDL_HINT_AUTO_UPDATE_SENSORS = b"SDL_AUTO_UPDATE_SENSORS"
SDL_HINT_ENABLE_STEAM_CONTROLLERS = b"SDL_ENABLE_STEAM_CONTROLLERS"
SDL_HINT_GAMECONTROLLERCONFIG = b"SDL_GAMECONTROLLERCONFIG"
SDL_HINT_GAMECONTROLLERCONFIG_FILE = b"SDL_GAMECONTROLLERCONFIG_FILE"
SDL_HINT_GAMECONTROLLERTYPE = b"SDL_GAMECONTROLLERTYPE"
SDL_HINT_GAMECONTROLLER_IGNORE_DEVICES = b"SDL_GAMECONTROLLER_IGNORE_DEVICES"
SDL_HINT_GAMECONTROLLER_IGNORE_DEVICES_EXCEPT = b"SDL_GAMECONTROLLER_IGNORE_DEVICES_EXCEPT"
SDL_HINT_GAMECONTROLLER_USE_BUTTON_LABELS = b"SDL_GAMECONTROLLER_USE_BUTTON_LABELS"
SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS = b"SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"
SDL_HINT_JOYSTICK_HIDAPI = b"SDL_JOYSTICK_HIDAPI"
SDL_HINT_JOYSTICK_HIDAPI_CORRELATE_XINPUT = b"SDL_JOYSTICK_HIDAPI_CORRELATE_XINPUT"
SDL_HINT_JOYSTICK_HIDAPI_GAMECUBE = b"SDL_JOYSTICK_HIDAPI_GAMECUBE"
SDL_HINT_JOYSTICK_GAMECUBE_RUMBLE_BRAKE = b"SDL_JOYSTICK_GAMECUBE_RUMBLE_BRAKE"
SDL_HINT_JOYSTICK_HIDAPI_JOY_CONS = b"SDL_JOYSTICK_HIDAPI_JOY_CONS"
SDL_HINT_JOYSTICK_HIDAPI_COMBINE_JOY_CONS = b"SDL_JOYSTICK_HIDAPI_COMBINE_JOY_CONS"
SDL_HINT_JOYSTICK_HIDAPI_LUNA = b"SDL_JOYSTICK_HIDAPI_LUNA"
SDL_HINT_JOYSTICK_HIDAPI_NINTENDO_CLASSIC = b"SDL_JOYSTICK_HIDAPI_NINTENDO_CLASSIC"
SDL_HINT_JOYSTICK_HIDAPI_SHIELD = b"SDL_JOYSTICK_HIDAPI_SHIELD"
SDL_HINT_JOYSTICK_HIDAPI_PS4 = b"SDL_JOYSTICK_HIDAPI_PS4"
SDL_HINT_JOYSTICK_HIDAPI_PS4_RUMBLE = b"SDL_JOYSTICK_HIDAPI_PS4_RUMBLE"
SDL_HINT_JOYSTICK_HIDAPI_PS5 = b"SDL_JOYSTICK_HIDAPI_PS5"
SDL_HINT_JOYSTICK_HIDAPI_PS5_PLAYER_LED = b"SDL_JOYSTICK_HIDAPI_PS5_PLAYER_LED"
SDL_HINT_JOYSTICK_HIDAPI_PS5_RUMBLE = b"SDL_JOYSTICK_HIDAPI_PS5_RUMBLE"
SDL_HINT_JOYSTICK_HIDAPI_STADIA = b"SDL_JOYSTICK_HIDAPI_STADIA"
SDL_HINT_JOYSTICK_HIDAPI_STEAM = b"SDL_JOYSTICK_HIDAPI_STEAM"
SDL_HINT_JOYSTICK_HIDAPI_SWITCH = b"SDL_JOYSTICK_HIDAPI_SWITCH"
SDL_HINT_JOYSTICK_HIDAPI_SWITCH_HOME_LED = b"SDL_JOYSTICK_HIDAPI_SWITCH_HOME_LED"
SDL_HINT_JOYSTICK_HIDAPI_JOYCON_HOME_LED = b"SDL_JOYSTICK_HIDAPI_JOYCON_HOME_LED"
SDL_HINT_JOYSTICK_HIDAPI_SWITCH_PLAYER_LED = b"SDL_JOYSTICK_HIDAPI_SWITCH_PLAYER_LED"
SDL_HINT_JOYSTICK_HIDAPI_XBOX = b"SDL_JOYSTICK_HIDAPI_XBOX"
SDL_HINT_JOYSTICK_RAWINPUT = b"SDL_JOYSTICK_RAWINPUT"
SDL_HINT_JOYSTICK_RAWINPUT_CORRELATE_XINPUT = b"SDL_JOYSTICK_RAWINPUT_CORRELATE_XINPUT"
SDL_HINT_JOYSTICK_ROG_CHAKRAM = b"SDL_JOYSTICK_ROG_CHAKRAM"
SDL_HINT_JOYSTICK_THREAD = b"SDL_JOYSTICK_THREAD"
SDL_HINT_JOYSTICK_DEVICE = b"SDL_JOYSTICK_DEVICE"


# Platform Specific Hints

SDL_HINT_EMSCRIPTEN_ASYNCIFY = b"SDL_EMSCRIPTEN_ASYNCIFY"
SDL_HINT_EMSCRIPTEN_KEYBOARD_ELEMENT = b"SDL_EMSCRIPTEN_KEYBOARD_ELEMENT"
SDL_HINT_KMSDRM_REQUIRE_DRM_MASTER = b"SDL_KMSDRM_REQUIRE_DRM_MASTER"
SDL_HINT_LINUX_DIGITAL_HATS = b"SDL_LINUX_DIGITAL_HATS"
SDL_HINT_LINUX_HAT_DEADZONES = b"SDL_LINUX_HAT_DEADZONES"
SDL_HINT_LINUX_JOYSTICK_CLASSIC = b"SDL_LINUX_JOYSTICK_CLASSIC"
SDL_HINT_LINUX_JOYSTICK_DEADZONES = b"SDL_LINUX_JOYSTICK_DEADZONES"
SDL_HINT_MAC_BACKGROUND_APP = b"SDL_MAC_BACKGROUND_APP"
SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK = b"SDL_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK"
SDL_HINT_MAC_OPENGL_ASYNC_DISPATCH = b"SDL_MAC_OPENGL_ASYNC_DISPATCH"
SDL_HINT_RPI_VIDEO_LAYER = b"SDL_RPI_VIDEO_LAYER"
SDL_HINT_RENDER_DIRECT3D11_DEBUG = b"SDL_RENDER_DIRECT3D11_DEBUG"
SDL_HINT_RENDER_DIRECT3D_THREADSAFE = b"SDL_RENDER_DIRECT3D_THREADSAFE"
SDL_HINT_VIDEO_MAC_FULLSCREEN_SPACES = b"SDL_VIDEO_MAC_FULLSCREEN_SPACES"
SDL_HINT_VIDEO_WIN_D3DCOMPILER = b"SDL_VIDEO_WIN_D3DCOMPILER"
SDL_HINT_WINDOWS_NO_CLOSE_ON_ALT_F4 = b"SDL_WINDOWS_NO_CLOSE_ON_ALT_F4"
SDL_HINT_WINDOWS_DISABLE_THREAD_NAMING = b"SDL_WINDOWS_DISABLE_THREAD_NAMING"
SDL_HINT_WINDOWS_ENABLE_MESSAGELOOP = b"SDL_WINDOWS_ENABLE_MESSAGELOOP"
SDL_HINT_WINDOWS_FORCE_MUTEX_CRITICAL_SECTIONS = b"SDL_WINDOWS_FORCE_MUTEX_CRITICAL_SECTIONS"
SDL_HINT_WINDOWS_FORCE_SEMAPHORE_KERNEL = b"SDL_WINDOWS_FORCE_SEMAPHORE_KERNEL"
SDL_HINT_WINDOWS_INTRESOURCE_ICON = b"SDL_WINDOWS_INTRESOURCE_ICON"
SDL_HINT_WINDOWS_INTRESOURCE_ICON_SMALL = b"SDL_WINDOWS_INTRESOURCE_ICON_SMALL"
SDL_HINT_WINDOWS_USE_D3D9EX = b"SDL_WINDOWS_USE_D3D9EX"
SDL_HINT_WINDOWS_DPI_AWARENESS = b"SDL_WINDOWS_DPI_AWARENESS"
SDL_HINT_WINDOWS_DPI_SCALING = b"SDL_WINDOWS_DPI_SCALING"
SDL_HINT_XINPUT_ENABLED = b"SDL_XINPUT_ENABLED"
SDL_HINT_XINPUT_USE_OLD_JOYSTICK_MAPPING = b"SDL_XINPUT_USE_OLD_JOYSTICK_MAPPING"


# Mobile Specific Hints

SDL_HINT_ACCELEROMETER_AS_JOYSTICK = b"SDL_ACCELEROMETER_AS_JOYSTICK"
SDL_HINT_TV_REMOTE_AS_JOYSTICK = b"SDL_TV_REMOTE_AS_JOYSTICK"
SDL_HINT_ORIENTATIONS = b"SDL_IOS_ORIENTATIONS"
SDL_HINT_RETURN_KEY_HIDES_IME = b"SDL_RETURN_KEY_HIDES_IME"
SDL_HINT_ANDROID_APK_EXPANSION_MAIN_FILE_VERSION = b"SDL_ANDROID_APK_EXPANSION_MAIN_FILE_VERSION"
SDL_HINT_ANDROID_APK_EXPANSION_PATCH_FILE_VERSION = b"SDL_ANDROID_APK_EXPANSION_PATCH_FILE_VERSION"
SDL_HINT_ANDROID_SEPARATE_MOUSE_AND_TOUCH = b"SDL_ANDROID_SEPARATE_MOUSE_AND_TOUCH" # removed in 2.0.10
SDL_HINT_ANDROID_TRAP_BACK_BUTTON = b"SDL_ANDROID_TRAP_BACK_BUTTON"
SDL_HINT_ANDROID_BLOCK_ON_PAUSE = b"SDL_ANDROID_BLOCK_ON_PAUSE"
SDL_HINT_ANDROID_BLOCK_ON_PAUSE_PAUSEAUDIO = b"SDL_ANDROID_BLOCK_ON_PAUSE_PAUSEAUDIO"
SDL_HINT_APPLE_TV_CONTROLLER_UI_EVENTS = b"SDL_APPLE_TV_CONTROLLER_UI_EVENTS"
SDL_HINT_APPLE_TV_REMOTE_ALLOW_ROTATION = b"SDL_APPLE_TV_REMOTE_ALLOW_ROTATION"
SDL_HINT_IDLE_TIMER_DISABLED = b"SDL_IOS_IDLE_TIMER_DISABLED"
SDL_HINT_IOS_HIDE_HOME_INDICATOR = "SDL_IOS_HIDE_HOME_INDICATOR"
SDL_HINT_VITA_TOUCH_MOUSE_DEVICE = b"SDL_HINT_VITA_TOUCH_MOUSE_DEVICE"
SDL_HINT_WINRT_PRIVACY_POLICY_URL = b"SDL_WINRT_PRIVACY_POLICY_URL"
SDL_HINT_WINRT_PRIVACY_POLICY_LABEL = b"SDL_WINRT_PRIVACY_POLICY_LABEL"
SDL_HINT_WINRT_HANDLE_BACK_BUTTON = b"SDL_WINRT_HANDLE_BACK_BUTTON"


# Constants & enums

SDL_HintPriority = c_int
SDL_HINT_DEFAULT = 0
SDL_HINT_NORMAL = 1
SDL_HINT_OVERRIDE = 2


# Callback function definitions

SDL_HintCallback = CFUNCTYPE(None, c_void_p, c_char_p, c_char_p, c_char_p)


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_SetHintWithPriority", [c_char_p, c_char_p, SDL_HintPriority], SDL_bool),
    SDLFunc("SDL_SetHint", [c_char_p, c_char_p], SDL_bool),
    SDLFunc("SDL_GetHint", [c_char_p], c_char_p),
    SDLFunc("SDL_ResetHint", [c_char_p], SDL_bool, added='2.24.0'),
    SDLFunc("SDL_ResetHints", None, None, added='2.26.0'),
    SDLFunc("SDL_GetHintBoolean", [c_char_p, SDL_bool], SDL_bool, added='2.0.5'),
    SDLFunc("SDL_ClearHints"),
    SDLFunc("SDL_AddHintCallback", [c_char_p, SDL_HintCallback, c_void_p]),
    SDLFunc("SDL_DelHintCallback",[c_char_p, SDL_HintCallback, c_void_p]),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)
    __all__.append(f.name) # Add all bound functions to module namespace


# Aliases for ctypes bindings

SDL_SetHintWithPriority = _ctypes["SDL_SetHintWithPriority"]
SDL_SetHint = _ctypes["SDL_SetHint"]
SDL_GetHint = _ctypes["SDL_GetHint"]
SDL_ResetHint = _ctypes["SDL_ResetHint"]
SDL_ResetHints = _ctypes["SDL_ResetHints"]
SDL_GetHintBoolean = _ctypes["SDL_GetHintBoolean"]
SDL_ClearHints = _ctypes["SDL_ClearHints"]
SDL_AddHintCallback = _ctypes["SDL_AddHintCallback"]
SDL_DelHintCallback = _ctypes["SDL_DelHintCallback"]
