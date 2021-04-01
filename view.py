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
        self.setFixedSize(759, 639)

        appPath = os.path.dirname(os.path.abspath(__file__))
        QFontDatabase.addApplicationFont(appPath+"/Noto & Ancient Runes Reloaded/NotoSans&AncientRunesReloaded-Regular.ttf")
        ancientFont = QFont("Noto Sans & Ancient Runes Reloaded", 14)
        self.setFont(ancientFont)

        self.__centralWidget = QWidget(self)
        self.setCentralWidget(self.__centralWidget)
        self.mainLayout = QHBoxLayout()
        self.__centralWidget.setLayout(self.mainLayout)
        self.__createDisplay()

        self.__createMenu()

        self.keyboard = Keyboard(ancientFont)

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

    def closeEvent(self, event: QCloseEvent):
        self.closeApp()


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
        self.confidenceLayout = QGridLayout()
        self.confidenceWrapper.setLayout(self.confidenceLayout)
        self.confidenceUnspecifiedButton = QRadioButton("Unspecified")
        self.confidenceLowButton = QRadioButton("Low")
        self.confidenceMediumButton = QRadioButton("Medium")
        self.confidenceHighButton = QRadioButton("High")
        self.confidenceWrapper.setTitle("Confidence:")
        self.confidenceLayout.addWidget(self.confidenceUnspecifiedButton,0,0)
        self.confidenceLayout.addWidget(self.confidenceLowButton,1,0)
        self.confidenceLayout.addWidget(self.confidenceMediumButton,0,1)
        self.confidenceLayout.addWidget(self.confidenceHighButton,1,1)
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
    def __init__(self, font):
        super().__init__()
        self.setWindowTitle("Ancient Runes Keyboard")
        self.setFont(font)
        self.setFixedSize(440, 230)

        self.generalLayout = QGridLayout()
        self.setLayout(self.generalLayout)
        self.__createButtons(self.generalLayout)

    def __createButtons(self, layout: QGridLayout):
        self.buttons = {}
        baseChar = ord("\ue000")
        for i in range(48):
            btnText = chr(baseChar+i)
            xpos = i//10
            ypos = i%10
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40,40)
            layout.addWidget(self.buttons[btnText], xpos, ypos)


def main():
    app = QApplication(sys.argv)
    view = MainWindow()
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
