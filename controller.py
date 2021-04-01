import sys
from PyQt5.QtWidgets import QApplication, QPushButton

from model import *
from view import *

class Controller:
    def __init__(self, dictionary, window):
        self.dictionary = dictionary
        self.window = window
        self.connectButtons()
        self.window.show()

    def connectButtons(self):
        self.connectKeyboard()

    def connectKeyboard(self):
        for key, button in self.window.keyboard.buttons.items():
            button.clicked.connect(lambda key: self.keyboardButtonPressed)

    def keyboardButtonPressed(self, key):
        print(key)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller(Dictionary(), MainWindow())
    sys.exit(app.exec_())
