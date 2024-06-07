import os
import sys


def resource_path(relative_path) -> str | bytes:
    """ Get the absolute path to the resource, works for both dev and PyInstaller/py2app """
    try:
        # If PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        try:
            # If py2app creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    absolute_path = resource_path("cards")
    print(absolute_path)
