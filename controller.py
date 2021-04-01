import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QKeyEvent
from functools import partial

from model import *
from view import *

class Controller:
    def __init__(self, app, dictionary, window):
        self.app = app
        self.dictionary = dictionary
        self.window = window
        self.connectButtons()
        self.window.show()

    def connectButtons(self):
        self.connectKeyboard()

    def connectKeyboard(self):
        for key, button in self.window.keyboard.buttons.items():
            button.clicked.connect(partial(self.keyboardButtonPressed, key))

    def keyboardButtonPressed(self, key):
        event = QKeyEvent(QEvent.KeyPress, 0, Qt.NoModifier, key)
        self.app.postEvent(self.window.focusWidget(), event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller(app, Dictionary(), MainWindow())
    sys.exit(app.exec_())
