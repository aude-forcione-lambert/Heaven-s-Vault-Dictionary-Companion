from typing import List, Dict

import sys
import os

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QKeyEvent
from functools import partial

from model import *
from view import *

class Controller:
    '''
    Controller part of the application. This class requires an instance of the Dictionary class from the model library and an instance of the MainWindow class from the view library.
    '''
    def __init__(self, app: QApplication, dictionary: Dictionary, window: MainWindow):
        '''
        app: QApplication instance
        dictionary: Dictionary instance
        window: MainWindow instance
        '''
        self.app = app
        self.dictionary = dictionary
        self.window = window
        self._connect_btns()
        self.window.show()
        self._focused_word = None

    def _connect_btns(self):
        '''
        Connects the buttons from the window to the appropriate function.
        '''
        self._connect_keyboard()

        self.window.dictionary_panel.new_word_btn.clicked.connect(self.new_word_edit)

        self.window.edit_panel.save_btn.clicked.connect(self.save_word)
        self.window.edit_panel.cancel_btn.clicked.connect(self.close_edit_word)

        self.window.definition_panel.edit_btn.clicked.connect(self.edit_word)

    def _connect_keyboard(self):
        '''
        Connects the buttons from the keyboard dialog to the appropriate event posting function.
        '''
        for key, button in self.window.keyboard.buttons.items():
            button.clicked.connect(partial(self.keyboard_btn_pressed, key))

    def keyboard_btn_pressed(self, key: chr):
        '''
        Function sending a key pressed event to the main window.
        key: unicode character to be sent in the event
        '''
        event = QKeyEvent(QEvent.KeyPress, 0, Qt.NoModifier, key)
        self.app.postEvent(self.window.focusWidget(), event)

    def new_word_edit(self):
        '''
        Instructs the window to enter edit mode for a new word.
        '''
        self._focused_word = None
        self.window.edit_mode()
        self.window.edit_panel.empty_panel()

    def save_word(self):
        '''
        Saves a word from the window's edit panel to the dictionary. If a word is in focus (editing an existing word), the word in the dictionary is replaced. Else (editing a new word), a new word is created in the dictionary.
        '''
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
        self._focused_word = word
        self.close_edit_word()

    def close_edit_word(self):
        '''
        Closes the window's edit mode. Returns to read mode for the focused word or to closed mode if no word is in focus. Does not save edit mode's modifications.
        '''
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
        '''
        Enters edit mode for an existing word.
        '''
        word = self._focused_word
        translation = self.dictionary.entries[self._focused_word].translation
        confidence = self.dictionary.entries[self._focused_word].confidence
        notes = self.dictionary.entries[self._focused_word].notes
        self.window.definition_panel.fill_panel(word, translation, confidence, notes)
        self.window.edit_mode()

    def update_word_dict(self, words: Dict[str, str]=None):
        '''
        Empties and repopulates the dictionary display.
        words: ancient words to display along with their translations. If None all words from the dictionary are displayed
        '''
        self.window.dictionary_panel.clearWords()
        if not words:
            words = self.dictionary.entries
        for word, translation in entries.items():
            button = self.window.dictionary_panel.add_word(word, translation)
            #TODO

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller(app, Dictionary(), MainWindow())
    sys.exit(app.exec_())
