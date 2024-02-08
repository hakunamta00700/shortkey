import json
import pprint

from loguru import logger
from pynput import keyboard

from . import config
from .commands import toggle_activation
from .res_path import KEY_PATH
from .util import parse_defined_keys


def try_quit():
    config.IS_QUIT = True


def console():
    key_path = KEY_PATH
    logger.info(f"console is_quit:{config.IS_QUIT}")

    pressed_keys = set()
    with open(key_path, "r") as fp:
        json_key_list = json.load(fp)
    logger.info(pprint.pformat(json_key_list))
    # 이벤트 처리
    parsed_defined_keys = parse_defined_keys(json_key_list)
    with keyboard.Events() as events:
        for event in events:
            if config.IS_QUIT == True:
                logger.info("is Quit -- ")
                break
            if event.key == keyboard.Key.esc:
                config.IS_QUIT = True
                logger.info("will finished")
                continue
            elif isinstance(event, keyboard.Events.Press):
                pressed_keys.add(event.key)
                for key, defined_keyDict in parsed_defined_keys.items():
                    if all(
                        _key in pressed_keys for _key in defined_keyDict["parsed_key"]
                    ):
                        logger.info(f"pressed - key:{defined_keyDict['parsed_key']}")
                        defined_keyDict["cmd"]()
                        break
                if all(
                    _key in pressed_keys
                    for _key in [keyboard.Key.cmd, keyboard.Key.f10]
                ):
                    toggle_activation()
                if all(
                    _key in pressed_keys
                    for _key in [keyboard.Key.cmd, keyboard.Key.f11]
                ):
                    try_quit()
            elif isinstance(event, keyboard.Events.Release):
                try:
                    pressed_keys.remove(event.key)
                except KeyError:
                    pass
            else:
                pass
