import sys
import os

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QRegExpValidator, QCloseEvent


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heaven's Vault Dictionary Companion")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(759, 645)

        app_path = os.path.dirname(os.path.abspath(__file__))
        QFontDatabase.addApplicationFont(app_path+"/Noto & Ancient Runes Reloaded/NotoSans&AncientRunesReloaded-Regular.ttf")
        ancient_font = QFont("Noto Sans & Ancient Runes Reloaded", 14)
        self.setFont(ancient_font)

        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._main_layout = QHBoxLayout()
        self._main_layout.setAlignment(Qt.AlignLeft)
        self._central_widget.setLayout(self._main_layout)
        self._create_display()

        self._create_menu()

        self.keyboard = Keyboard(ancient_font)

    def _create_display(self):
        self.dictionary_panel = DictionaryPanel()
        self.definition_panel = DefinitionPanel()
        self.edit_panel = EditPanel()

        self.closed_panel = QFrame()
        self.closed_panel.setFixedSize(377, 610)
        self.closed_panel.setFrameStyle(QFrame.Box)
        self.closed_panel.setFrameShadow(QFrame.Sunken)

        self._main_layout.addWidget(self.dictionary_panel)
        self._main_layout.addWidget(self.definition_panel)
        self._main_layout.addWidget(self.edit_panel)
        self._main_layout.addWidget(self.closed_panel)
        self.closed_mode()

        self._main_layout.setContentsMargins(1,1,0,0)
        self._main_layout.setSpacing(1)

    def _create_menu(self):
        self.file = self.menuBar().addMenu("File")
        self.fileOpen = self.file.addAction("Open")
        self.fileSave = self.file.addAction("Save")
        self.file.addSeparator()
        self.file.addAction("Exit", self.close_app)
        self.menuBar().addAction("\u2328", self.show_keyboard)

    def edit_mode(self):
        self.definition_panel.hide()
        self.closed_panel.hide()
        self.edit_panel.show()

    def read_mode(self):
        self.edit_panel.hide()
        self.closed_panel.hide()
        self.definition_panel.show()

    def closed_mode(self):
        self.edit_panel.hide()
        self.definition_panel.hide()
        self.closed_panel.show()

    def show_keyboard(self):
        self.keyboard.show()

    def close_app(self):
        self.keyboard.close()
        self.close()

    def closeEvent(self, event: QCloseEvent):
        self.close_app()


class DictionaryPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(377, 610)
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)

        self._word_list = {}

        self._create_display()

    def _create_display(self):
        search_bar_wrapper = QFrame()
        search_bar_layout = QHBoxLayout()
        search_bar_layout.setContentsMargins(0,0,0,0)
        search_bar_wrapper.setLayout(search_bar_layout)
        self.search_bar = QLineEdit()
        search_bar_layout.addWidget(self.search_bar)
        search_bar_layout.addWidget(QLabel("\U0001f50d"))

        self.new_word_btn = QPushButton("New Word")

        self._word_list_frame = QFrame()
        self._word_list_frame.setFixedWidth(339)
        self._word_list_layout = QVBoxLayout()
        self._word_list_layout.setContentsMargins(3,3,3,3)
        self._word_list_layout.setSpacing(4)
        self._word_list_layout.setAlignment(Qt.AlignTop)

        self._word_list_frame.setLayout(self._word_list_layout)
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setWidget(self._word_list_frame)

        self._layout.addWidget(search_bar_wrapper)
        self._layout.addWidget(self.new_word_btn)
        self._layout.addWidget(scroll_area)

    def add_word(self, word, translation):
        word_btn = QPushButton(word+"\n"+translation)
        self._word_list[word] = word_btn
        self._word_list_layout.addWidget(word_btn)
        self._word_list_frame.adjustSize()
        return word_btn

    def remove_word(self, word):
        word_btn = self._word_list.pop(word)
        word_btn.deleteLater()
        self._word_list_frame.adjustSize()

    def clear_words(self):
        for word in self._word_list:
            self.remove_word(word)


class EditPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(377, 610)
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self._create_display()

    def _create_display(self):
        word_wrapper = QFrame()
        word_layout = QHBoxLayout()
        word_layout.setContentsMargins(0,0,0,0)
        word_wrapper.setLayout(word_layout)
        word_layout.addWidget(QLabel("Spelling:"))
        self.word_edit = QLineEdit()
        rx = QRegExp("^[\ue000-\ue02c]+$")
        validator = QRegExpValidator(rx, self.word_edit)
        self.word_edit.setValidator(validator)
        word_layout.addWidget(self.word_edit)

        translation_wrapper = QFrame()
        translation_layout = QHBoxLayout()
        translation_layout.setContentsMargins(0,0,0,0)
        translation_wrapper.setLayout(translation_layout)
        translation_layout.addWidget(QLabel("Translation:"))
        self.translation_edit = QLineEdit()
        translation_layout.addWidget(self.translation_edit)

        confidence_wrapper = QGroupBox()
        confidence_layout = QGridLayout()
        confidence_wrapper.setLayout(confidence_layout)
        self.confidence_unsp_btn = QRadioButton("Unspecified")
        self.confidence_low_btn = QRadioButton("Low")
        self.confidence_med_btn = QRadioButton("Medium")
        self.confidence_high_btn = QRadioButton("High")
        confidence_wrapper.setTitle("Confidence:")
        confidence_layout.addWidget(self.confidence_unsp_btn,0,0)
        confidence_layout.addWidget(self.confidence_low_btn,1,0)
        confidence_layout.addWidget(self.confidence_med_btn,0,1)
        confidence_layout.addWidget(self.confidence_high_btn,1,1)
        self.confidence_unsp_btn.setChecked(True)

        self.notes_edit = QTextEdit()

        btns_wrapper = QFrame()
        btns_layout = QHBoxLayout()
        btns_layout.setContentsMargins(0,0,0,0)
        btns_wrapper.setLayout(btns_layout)
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btns_layout.addWidget(self.save_btn)
        btns_layout.addWidget(self.cancel_btn)

        self._layout.setSpacing(8)
        self._layout.addWidget(word_wrapper)
        self._layout.addWidget(translation_wrapper)
        self._layout.addWidget(confidence_wrapper)
        self._layout.addWidget(QLabel("Notes:"))
        self._layout.addWidget(self.notes_edit)
        self._layout.addWidget(btns_wrapper)

    def empty_panel(self):
        self.fill_panel("", "", 0, "")

    def fill_panel(self, word, translation, confidence, notes):
        self.word_edit.setText(word)
        self.translation_edit.setText(translation)
        if confidence == 0:
            self.confidence_unsp_btn.setChecked(True)
        elif confidence == 1:
            self.confidence_low_btn.setChecked(True)
        elif confidence == 2:
            self.confidence_med_btn.setChecked(True)
        elif confidence == 3:
            self.confidence_high_btn.setChecked(True)
        self.notes_edit.setText(notes)


class DefinitionPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(377, 610)
        self._layout = QVBoxLayout(self)
        self._layout.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self._create_display()

    def _create_display(self):
        self.word = QLabel()

        self.translation = QLabel()

        self.confidence = QLabel()

        self.notes = QLabel()
        self.notes.setWordWrap(True)

        self.edit_btn = QPushButton("Edit")

        self._layout.setSpacing(8)
        self._layout.addWidget(self.word)
        self._layout.addWidget(self.translation)
        self._layout.addWidget(self.confidence)
        self._layout.addWidget(QLabel("Notes:"))
        self._layout.addWidget(self.notes)
        self._layout.addWidget(self.edit_btn)

    def fill_panel(self, word, translation, confidence, notes):
        self.word.setText(word)
        self.translation.setText(translation)
        if confidence == 0:
            self.confidence.setText("Confidence: Unspecified")
        elif confidence == 1:
            self.confidence.setText("Confidence: Low")
        elif confidence == 2:
            self.confidence.setText("Confidence: Medium")
        elif confidence == 3:
            self.confidence.setText("Confidence: High")
        self.notes.setText(notes)


class Keyboard(QDialog):
    def __init__(self, font):
        super().__init__()
        self.setWindowTitle("Ancient Runes Keyboard")
        self.setFont(font)
        self.setFixedSize(440, 230)

        self._layout = QGridLayout()
        self.setLayout(self._layout)
        self._create_display(self._layout)

    def _create_display(self, layout: QGridLayout):
        self.buttons = {}
        base_char = ord("\ue000")
        for i in range(48):
            btn_text = chr(base_char+i)
            xpos = i//10
            ypos = i%10
            self.buttons[btn_text] = QPushButton(btn_text)
            self.buttons[btn_text].setFixedSize(40,40)
            layout.addWidget(self.buttons[btn_text], xpos, ypos)


def main():
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
