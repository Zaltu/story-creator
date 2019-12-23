"""
Module containing the Character creator view.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox,
                               QComboBox)
from libs.creatures import Character
from libs import json_reader
from gui.popup import popup

class CharUI(QWidget):
    """
    Main widget for the Character creator view.

    :param MainFrame mainframe: the application mainframe
    :param QWidget op: parent widget
    """
    def __init__(self, mainframe, op):
        print("Starting...")
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.nameT = None
        self.infoT = None
        self.importantB = None
        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        Does a lot of stuff.
        """
        self.mainframe.setWindowTitle("Character Creator")

        grid = QGridLayout()
        self.setLayout(grid)

        nameL = QLabel(self, text="Name:")
        grid.addWidget(nameL, 1, 1)

        self.nameT = QLineEdit(self)
        self.nameT.setFixedSize(200, 20)
        grid.addWidget(self.nameT, 1, 2, 1, 2)

        self.importantB = QCheckBox(self, text="Important?")
        grid.addWidget(self.importantB, 1, 4)

        infoL = QLabel(self, text="Info:")
        grid.addWidget(infoL, 2, 1)

        self.infoT = QTextEdit(self)
        self.infoT.setFixedSize(300, 150)
        grid.addWidget(self.infoT, 2, 2, 1, 3)

        save = QPushButton(self, text="Save")
        save.clicked.connect(self.save)
        grid.addWidget(save, 4, 1)

        remove = QPushButton(self, text="Remove")
        remove.clicked.connect(self.remove)
        grid.addWidget(remove, 4, 2)

        back = QPushButton(self, text="Back")
        back.clicked.connect(self.back)
        grid.addWidget(back, 4, 3)

        names = json_reader.readCharNames()
        names.append("New")
        self.allChars = QComboBox(self)
        self.allChars.activated.connect((lambda: self.loadChar(self.allChars.currentText())))
        self.allChars.addItems(names)
        self.allChars.setCurrentIndex(self.allChars.count()-1)
        grid.addWidget(self.allChars, 4, 4)

    def loadChar(self, name):
        """
        Load one character from file based on the name.

        :param str name: name of character to load
        """
        print("Loading...")
        if self.importantB.isChecked():
            self.importantB.toggle()
        self.nameT.clear()
        self.infoT.clear()
        if name == "New":
            return
        characterL = json_reader.readOne(name, 'chars')
        charTL = Character(characterL["name"], characterL["desc"], characterL["important"])
        if charTL.getImportant():
            self.importantB.toggle()
        self.nameT.setText(charTL.getName())
        self.infoT.setText(charTL.getDesc())
        print("Loaded character " + self.allChars.currentText())

    def remove(self):
        """
        Remove a character from the list, and remove them from disk.
        """
        if not popup("Are you certain you want to completely remove this character?\n(Cannot be undone)",
                     "Warning"):
            return
        print("Removing character " + self.allChars.currentText())
        json_reader.deleteChar(self.allChars.currentText())
        self.allChars.removeItem(self.allChars.currentIndex())
        self.allChars.setCurrentIndex(self.allChars.count()-1)
        self.loadChar("New")

    def save(self):
        """
        Save a character to disk from the information entered in the GUI.
        """
        if self.nameT.text() in ["New", ""]:
            popup("Sorry, your character cannot be called \""+self.nameT.text()+"\". That is a reserved "
                  "keyword (and it's also a dumb name)", "Critical")
            return
        print("Saving")
        try:
            toWrite = Character(self.nameT.text(), self.infoT.toPlainText(), self.importantB.isChecked())
        except UnicodeEncodeError as e:
            print(e)
            print(type(e))
            popup("Sorry, unicode characters are not supported.", "Critical")
            return
        json_reader.writeOne(toWrite, 'chars')
        if toWrite.getName() not in [self.allChars.itemText(i) for i in range(self.allChars.count())]:
            self.allChars.insertItem(self.allChars.count()-1, self.nameT.text())
            self.allChars.setCurrentIndex(self.allChars.count()-2)
        print("Saved")

    def back(self):
        """
        Return the view to the calling widget.
        """
        self.mainframe.changeState(self.op)
