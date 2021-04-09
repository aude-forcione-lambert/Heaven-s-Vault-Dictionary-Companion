import sys
import os

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
        self._connect_btns()
        self.window.show()
        self._focused_word = None

    def _connect_btns(self):
        self._connect_keyboard()

        self.window.dictionary_panel.new_word_btn.clicked.connect(self.new_word)

        self.window.edit_panel.save_btn.clicked.connect(self.save_word)
        self.window.edit_panel.cancel_btn.clicked.connect(self.cancel_edit_word)

        self.window.definition_panel.edit_btn.clicked.connect(self.edit_word)

    def _connect_keyboard(self):
        for key, button in self.window.keyboard.buttons.items():
            button.clicked.connect(partial(self.keyboard_btn_pressed, key))

    def keyboard_btn_pressed(self, key):
        event = QKeyEvent(QEvent.KeyPress, 0, Qt.NoModifier, key)
        self.app.postEvent(self.window.focusWidget(), event)

    def new_word(self):
        self._focused_word = None
        self.window.edit_mode()
        self.window.edit_panel.empty_panel()

    def save_word(self):
        word = self.window.edit_panel.word_edit.text()
        translation = self.window.edit_panel.translation_edit.text()
        confidence = 0
        if self.window.edit_panel.confidence_low_btn.isChecked():
            confidence = 1
        elif self.window.edit_panel.confidence_med_btn.isChecked():
            confidence = 2
        elif self.window.edit_panel.confidence_high_btn.isChecked():
            confidence = 3
        notes = self.window.edit_panel.notes_edit.text()
        #TODO

    def cancel_edit_word(self):
        if self._focused_word:
            word = self._focused_word
            translation = self.dictionary.entries[self._focused_word].translation
            confidence = self.dictionary.entries[self._focused_word].confidence
            notes = self.dictionary.entries[self._focused_word].notes
            self.window.dictionary_panel.fill_panel(word, translation, confidence, notes)
            self.window.read_mode()
        else:
            self.window.closed_mode()

    def edit_word(self):
        word = self._focused_word
        translation = self.dictionary.entries[self._focused_word].translation
        confidence = self.dictionary.entries[self._focused_word].confidence
        notes = self.dictionary.entries[self._focused_word].notes
        self.window.definition_panel.fill_panel(word, translation, confidence, notes)
        self.window.edit_mode()

    def updateWordDict(self):
        self.window.dictionary_panel.clearWords()
        words = self.dictionary.entries
        for word, translation in entries.items():
            self.window.dictionary_panel.add_word(word, translation)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller(app, Dictionary(), MainWindow())
    sys.exit(app.exec_())
