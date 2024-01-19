import multiprocessing

from loguru import logger
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from shortkey.res_path import ICON_PATH, KEY_PATH
from shortkey.start import Application


class MyProcess:
    @classmethod
    def start(cls):
        cls.process = multiprocessing.Process(target=Application.start, args=(KEY_PATH,))
        cls.process.start()

    @classmethod
    def kill(cls):
        cls.process.kill()


class MyApplication(QApplication):
    @staticmethod
    def quit():
        try:
            MyProcess.kill()
        except Exception as err:
            logger.error(err)
        QApplication.quit()


class MyTrayIcon(QSystemTrayIcon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        icon = QIcon(ICON_PATH)
        self.setIcon(icon)
        self.setVisible(True)
        self.menu = QMenu()
        self.quit = QAction("Quit")
        self.start = QAction("start")
        self.start.triggered.connect(self.onStartApp)
        self.quit.triggered.connect(self.onQuitApp)
        self.menu.addAction(self.quit)
        self.menu.addAction(self.start)
        self.setContextMenu(self.menu)

    def onStartApp(self):
        print("-->>11onStartApp")
        MyProcess.start()

    def onQuitApp(self):
        MyApplication.quit()


if __name__ == "__main__":
    app = MyApplication()
    app.setQuitOnLastWindowClosed(False)
    tray = MyTrayIcon(app)
    app.exec_()
