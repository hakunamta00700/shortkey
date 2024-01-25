import os
import sys
from pathlib import Path


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
START_EXE = os.path.join(application_path, "resources", "start")
