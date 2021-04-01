import sys

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QRegExpValidator

QFontDatabase.addApplicationFont(":/Noto & Ancient Runes Reloaded/NotoSans&AncientRunesReloaded-Regular.ttf")
ancient_font = QFont("Noto Sans & Ancient Runes Reloaded", 11)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Heaven's Vault Dictionary Companion")
        self.setFont(ancient_font)
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(759, 639)

        self.__centralWidget = QWidget(self)
        self.setCentralWidget(self.__centralWidget)
        self.mainLayout = QHBoxLayout()
        self.__centralWidget.setLayout(self.mainLayout)
        self.__createDisplay()

        self.__createMenu()

        self.keyboard = Keyboard()

    def __createDisplay(self):
        self.dictionaryPanel = DictionaryPanel()
        #self.definitionPanel = DefinitionPanel()
        self.editPanel = EditPanel()
        self.mainLayout.addWidget(self.dictionaryPanel)
        #self.mainLayout.addWidget(self.definitionPanel)
        self.mainLayout.addWidget(self.editPanel)
        self.mainLayout.setContentsMargins(1,1,0,0)
        self.mainLayout.setSpacing(1)

    def __createMenu(self):
        self.file = self.menuBar().addMenu("File")
        self.fileOpen = self.file.addAction("Open")
        self.fileSave = self.file.addAction("Save")
        self.file.addSeparator()
        self.file.addAction("Exit", self.closeApp)
        self.menuBar().addAction("\u2328", self.showKeyboard)

    def showKeyboard(self):
        self.keyboard.show()

    def closeApp(self):
        self.keyboard.close()
        self.close()


class DictionaryPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(377, 610)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)

        self.wordList = {}

        self.__createDisplay()

    def __createDisplay(self):
        searchBarWrapper = QFrame()
        searchBarLayout = QHBoxLayout()
        searchBarLayout.setContentsMargins(0,0,0,0)
        searchBarWrapper.setLayout(searchBarLayout)
        self.searchBar = QLineEdit()
        searchBarLayout.addWidget(self.searchBar)
        searchBarLayout.addWidget(QLabel("\U0001f50d"))

        self.newWordBtn = QPushButton("New Word")

        self.wordListFrame = QFrame()
        self.wordListFrame.setFixedWidth(339)
        self.wordListLayout = QVBoxLayout()
        self.wordListLayout.setContentsMargins(3,3,3,3)
        self.wordListLayout.setSpacing(4)
        self.wordListLayout.setAlignment(Qt.AlignTop)

        self.wordListFrame.setLayout(self.wordListLayout)
        scrollArea = QScrollArea()
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scrollArea.setWidget(self.wordListFrame)

        self.layout.addWidget(searchBarWrapper)
        self.layout.addWidget(self.newWordBtn)
        self.layout.addWidget(scrollArea)

    def addWord(self, word, translation):
        wordButton = QPushButton(word+"\n"+translation)
        self.wordList[word] = wordButton
        self.wordListLayout.addWidget(wordButton)
        self.wordListFrame.adjustSize()
        return wordButton

    def removeWord(self, word):
        wordButton = self.wordList.pop(word)
        wordButton.deleteLater()
        self.wordListFrame.adjustSize()

    def clearWords(self):
        for word in self.wordList:
            self.removeWord(word)


class EditPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(377, 610)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.setFrameStyle(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.__createDisplay()

    def __createDisplay(self):
        self.wordWrapper = QFrame()
        self.wordLayout = QHBoxLayout()
        self.wordLayout.setContentsMargins(0,0,0,0)
        self.wordWrapper.setLayout(self.wordLayout)
        self.wordLayout.addWidget(QLabel("Spelling:"))
        self.wordEdit = QLineEdit()
        rx = QRegExp("^[\ue000-\ue02c]+$")
        validator = QRegExpValidator(rx, self.wordEdit)
        self.wordEdit.setValidator(validator)
        self.wordLayout.addWidget(self.wordEdit)

        self.translationWrapper = QFrame()
        self.translationLayout = QHBoxLayout()
        self.translationLayout.setContentsMargins(0,0,0,0)
        self.translationWrapper.setLayout(self.translationLayout)
        self.translationLayout.addWidget(QLabel("Translation:"))
        self.translationEdit = QLineEdit()
        self.translationLayout.addWidget(self.translationEdit)

        self.confidenceWrapper = QGroupBox()
        self.confidenceLayout = QVBoxLayout()
        self.confidenceWrapper.setLayout(self.confidenceLayout)
        self.confidenceUnspecifiedButton = QRadioButton("Unspecified")
        self.confidenceLowButton = QRadioButton("Low")
        self.confidenceMediumButton = QRadioButton("Medium")
        self.confidenceHighButton = QRadioButton("High")
        self.confidenceWrapper.setTitle("Confidence:")
        self.confidenceLayout.addWidget(self.confidenceUnspecifiedButton)
        self.confidenceLayout.addWidget(self.confidenceLowButton)
        self.confidenceLayout.addWidget(self.confidenceMediumButton)
        self.confidenceLayout.addWidget(self.confidenceHighButton)
        self.confidenceUnspecifiedButton.setChecked(True)

        self.notesEditor = QTextEdit()

        self.saveButton = QPushButton("Save")

        self.layout.setSpacing(8)
        self.layout.addWidget(self.wordWrapper)
        self.layout.addWidget(self.translationWrapper)
        self.layout.addWidget(self.confidenceWrapper)
        self.layout.addWidget(QLabel("Notes:"))
        self.layout.addWidget(self.notesEditor)
        self.layout.addWidget(self.saveButton)


class Keyboard(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ancient Runes Keyboard")
        self.setFont(ancient_font)
        self.setFixedSize(440, 230)

        self.generalLayout = QGridLayout()
        self.setLayout(self.generalLayout)
        self.__createButtons(self.generalLayout)

    def __createButtons(self, layout: QGridLayout):
        self.buttons = {
                "\ue000": (0,0),
                "\ue001": (0,1),
                "\ue002": (0,2),
                "\ue003": (0,3),
                "\ue004": (0,4),
                "\ue005": (0,5),
                "\ue006": (0,6),
                "\ue007": (0,7),
                "\ue008": (0,8),
                "\ue009": (0,9),
                "\ue00a": (1,0),
                "\ue00b": (1,1),
                "\ue00c": (1,2),
                "\ue00d": (1,3),
                "\ue00e": (1,4),
                "\ue00f": (1,5),
                "\ue010": (1,6),
                "\ue011": (1,7),
                "\ue012": (1,8),
                "\ue013": (1,9),
                "\ue014": (2,0),
                "\ue015": (2,1),
                "\ue016": (2,2),
                "\ue017": (2,3),
                "\ue018": (2,4),
                "\ue019": (2,5),
                "\ue01a": (2,6),
                "\ue01b": (2,7),
                "\ue01c": (2,8),
                "\ue01d": (2,9),
                "\ue01e": (3,0),
                "\ue01f": (3,1),
                "\ue020": (3,2),
                "\ue021": (3,3),
                "\ue022": (3,4),
                "\ue023": (3,5),
                "\ue024": (3,6),
                "\ue025": (3,7),
                "\ue026": (3,8),
                "\ue027": (3,9),
                "\ue028": (4,0),
                "\ue029": (4,1),
                "\ue02a": (4,2),
                "\ue02b": (4,3),
                "\ue02c": (4,4),
                "\ue02d": (4,5),
                "\ue02e": (4,6),
                "\ue02f": (4,7),
                }
        for btnText, pos in self.buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40,40)
            layout.addWidget(self.buttons[btnText], pos[0], pos[1])


def main():
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
