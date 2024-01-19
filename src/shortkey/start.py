import json
import os
import pprint
from functools import partial

from loguru import logger
from pynput import keyboard
from pynput.keyboard import Controller, Key
from .res_path import KEY_PATH

is_active = True


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


class Application:
    @classmethod
    def start(cls, key_path):
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



def main():
    logger.info(f"KEY_PATH:{KEY_PATH}")
    Application.start(KEY_PATH)
if __name__ == "__main__":
    logger.info(f"run start.py")
    Application.start()
