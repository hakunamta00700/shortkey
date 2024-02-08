from functools import partial

from pynput import keyboard

from .commands import launch


def is_alpha_numeric(char):
    # 길이가 1인 문자열인지 확인
    if len(char) == 1:
        # 알파벳 또는 숫자인지 확인
        return char.isalnum()
    else:
        return False


def parse_keys(item):
    keys = item.split("+")
    key_values = []
    for key in keys:
        key = key.replace("<", "").replace(">", "")
        if key in keyboard.Key.__members__.keys():
            key_values.append(keyboard.Key.__members__[key])
        elif is_alpha_numeric(key):
            key_values.append(keyboard.KeyCode(char=key))
    return key_values


def parse_defined_keys(keyList):
    key_dict = {}
    for item in keyList:
        if item["type"] == "launch":
            value = parse_keys(item["key"])
            key_dict[item["key"]] = {
                "parsed_key": value,
                "cmd": partial(launch, item["cmd"]),
            }
    return key_dict
