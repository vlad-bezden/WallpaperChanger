import struct
import sys
import ctypes


SPI_SETDESKWALLPAPER = 0x0014
WALLPAPER_PATH = 'D:\\Temp\\20091215_222748_Tamila.jpg'


def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper(file_path):
    """Changes desktop wallpaper. """
    sys_parameters_info = get_sys_parameters_info()
    result = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, file_path, 3)

    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not result:
        raise ValueError(ctypes.WinError())


def turn_on_or_off(argv):
    """
    Check if wallpaper has to be turn on or off
    :param argv: passed parameters by user
    :return: true if wallpaper has to be turned on
    """
    return False if len(argv) == 1 else argv[1].lower() in ('true', '1', 'yes', 'on')


def main():
    """
    Checks if wallpaper has to be on or off and determines based on that wallpaper file path
    :return: None
    """
    if_turn_on = turn_on_or_off(sys.argv)
    file_path = WALLPAPER_PATH if if_turn_on else ''
    change_wallpaper(file_path)


if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print('Unexpected Error: ', str(e))
        sys.exit(1)