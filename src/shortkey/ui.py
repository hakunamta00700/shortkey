import sys
import threading

import pystray
from loguru import logger
from PIL import Image
from pynput import keyboard
from pynput.keyboard import Controller
from pystray import MenuItem as menu_item

from . import config
from .res_path import ICON_PATH, KEY_PATH
from .start import console


def create_image(imgFilePath, width, height):
    image = Image.open(imgFilePath)
    resized_image = image.resize((width, height))
    return resized_image


class MyIcon(pystray.Icon):
    def __init__(self):
        menu = (menu_item("start", self.on_start), menu_item("quit", self.on_quit))
        super().__init__("ShortKey", create_image(ICON_PATH, 64, 64), "ShortKey", menu)
        self.hotkey_thread = threading.Thread(target=console, args=(KEY_PATH,))

    def run_main(self):
        console()

    def on_start(self, item):
        logger.info("on_start")
        console()
        self.hotkey_thread.start()

    def on_quit(self, item):
        logger.info("on_quit")
        config.IS_QUIT = True
        _keyboard = Controller()
        _keyboard.press(keyboard.Key.cmd)
        _keyboard.press(keyboard.Key.f13)
        _keyboard.release(keyboard.Key.cmd)
        _keyboard.release(keyboard.Key.f13)
        self.hotkey_thread.join()
        self.stop()
        sys.exit(1)
