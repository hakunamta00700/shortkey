import json
import multiprocessing
import os
import pprint
import signal
import sys
from functools import partial
from pathlib import Path

import pystray
from loguru import logger
from PIL import Image
from pynput import keyboard
from pynput.keyboard import Controller, Key
from pystray import MenuItem as menu_item

logger.add("/Users/david/app.log")


def is_pyinstaller_bundle():
    """PyInstaller 환경인지 확인하는 함수"""
    return getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS")


# PyInstaller 환경과 Poetry 환경을 구분
if is_pyinstaller_bundle():
    # PyInstaller 환경일 경우
    application_path = sys._MEIPASS
else:
    # Poetry 환경 또는 일반적인 Python 환경일 경우
    application_path = Path(__file__).parent.parent


ICON_PATH = os.path.join(application_path, "resources", "icon.png")
KEY_PATH = os.path.join(application_path, "resources", "keys.json")

is_active = True


def create_image(imgFilePath, width, height):
    # 이미지 파일을 엽니다
    image = Image.open(imgFilePath)

    # 이미지 크기를 지정된 너비와 높이로 조정합니다
    resized_image = image.resize((width, height))

    return resized_image


def launch(param):
    global is_active
    if is_active:
        logger.info(f"launch {param}")
        os.system(param)


def parse_keys(defined_keys_strings):
    keys = defined_keys_strings.split("+")
    for key in keys:
        key.replace("<", "").replace(">", "")
    return keys


def send_key(in_keys):
    keys = parse_keys(in_keys)
    keyboard = Controller()
    for key in keys:
        if key == "cmd":
            keyboard.press(Key.cmd)
        else:
            keyboard.press(key)

    for key in reversed(keys):
        if key == "cmd":
            keyboard.release(Key.cmd)
        else:
            keyboard.release(key)


def toggle_activation():
    global is_active
    is_active = not is_active
    if is_active:
        logger.info("Program re-activated")
    else:
        logger.info("Program suspended")


def main(key_path):
    keyDict = {}

    with open(key_path, "r") as fp:
        keys = json.load(fp)
        logger.info(pprint.pformat(keys))
    for item in keys:
        if item["type"] == "launch":
            keyDict[item["key"]] = partial(launch, item["cmd"])

    keyDict["<cmd>+<109>"] = toggle_activation

    with keyboard.GlobalHotKeys(keyDict) as h:
        h.join()
    logger.info("current_Dir", os.getcwd())


def signal_handler(signum, frame):
    """SIGTERM 신호 처리"""
    print("SIGTERM received, shutting down...")
    sys.exit(0)


class MyIcon(pystray.Icon):
    def __init__(self):
        menu = (menu_item("start", self.on_start), menu_item("quit", self.on_quit))
        super().__init__("ShortKey", create_image(ICON_PATH, 64, 64), "ShortKey", menu)

    def run_main(self):
        main(KEY_PATH)

    def on_start(self, item):
        logger.info("on_start")
        self.hotkey_thread = multiprocessing.Process(target=main, args=(KEY_PATH,))
        self.hotkey_thread.start()

    def on_quit(self, item):
        logger.info("on_quit")
        self.hotkey_thread.terminate()
        self.stop()


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    icon = MyIcon()
    icon.run()
