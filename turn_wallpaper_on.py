import argparse
import struct
import ctypes


SPI_SETDESKWALLPAPER = 0x0014


def is_64_windows():
    """Find out how many bits is OS. """
    return struct.calcsize('P') * 8 == 64


def get_sys_parameters_info():
    """Based on if this is 32bit or 64bit returns correct version of SystemParametersInfo function. """
    return ctypes.windll.user32.SystemParametersInfoW if is_64_windows() \
        else ctypes.windll.user32.SystemParametersInfoA


def change_wallpaper(activate, file_path):
    """Changes desktop wallpaper. """
    sys_parameters_info = get_sys_parameters_info()
    result = sys_parameters_info(SPI_SETDESKWALLPAPER, 0, file_path, 3)

    # When the SPI_SETDESKWALLPAPER flag is used,
    # SystemParametersInfo returns TRUE
    # unless there is an error (like when the specified file doesn't exist).
    if not result:
        raise ValueError(ctypes.WinError())


def turn_on_or_off(activate):
    """
    Check if wallpaper has to be turn on or off
    :param activate: passed parameters by user
    :return: true if wallpaper has to be turned on
    """
    return True if activate == 'on' else False


def main(turn_on, file_path):
    """
    Checks if wallpaper has to be on or off and determines based on that wallpaper file path
    :return: None
    """
    activate = turn_on_or_off(turn_on)
    if activate and file_path == '':
        print('Invalid file path for desktop background. File path is required for turning wallpaper on')
        return
    change_wallpaper(activate, file_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Turnes Descktop wallpaer background on or off')
    parser.add_argument(
        '-a',
        '--activate',
        choices=['on', 'off'],
        default='off',
        help='Turn wallpaer on or turn it off.'
    )
    parser.add_argument(
        '-f',
        '--file',
        default='',
        help='Fully qualified path to image that needs to be displayed when wallpaper needs to be turn on'
    )
    try:
        args = parser.parse_args()
        main(args.activate, args.file)
    except Exception as e:
        print('Unexpected Error: ', str(e))
