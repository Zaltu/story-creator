"""
Module containing the main opening screen of the app.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QSizePolicy
from PySide2.QtGui import QPalette, QPixmap
from PySide2.QtCore import Qt
from gui.char_creator.chargui import CharUI
from gui.per_creator.pergui import per_creator
from gui.sl_creator.slcontextgui import SL_creator
from gui.supgui import SupportUI
from libs import json_reader

class OP(QWidget):
    """
    Main opening screen of the application. Can be used to pass to the Character creator, Persona creator or
    Social Link creator.

    :param MainFrame mainframe: the mainframe of the app
    """
    def __init__(self, mainframe):
        QWidget.__init__(self)
        self.mainframe = mainframe
        print("Application started")
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.black)
        self.setPalette(palette)
        self.initUI()

    def initUI(self):
        """
        Initialize the UI of this view.
        Does a lot of stuff.
        """
        self.mainframe.setWindowTitle("Story Creator")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        imageLabel = QLabel(self)
        logo = QPixmap(json_reader.buildPath("creator_logo.png"))
        imageLabel.setPixmap(logo)
        self.grid.addWidget(imageLabel, 0, 0)

        intframe = QWidget()
        self.grid.addWidget(intframe, 0, 1)

        bGrid = QGridLayout()
        intframe.setLayout(bGrid)

        createSL = QPushButton(intframe, text="Create Social Link")
        createSL.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        createSL.clicked.connect(self.actionS)
        bGrid.addWidget(createSL, 0, 0)

        createPersona = QPushButton(intframe, text="Create Persona")
        createPersona.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        createPersona.clicked.connect(self.actionP)
        bGrid.addWidget(createPersona, 1, 0)

        createChar = QPushButton(intframe, text="Create Character")
        createChar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        createChar.clicked.connect(self.actionC)
        bGrid.addWidget(createChar, 2, 0)

        support = QPushButton(intframe, text="Support/Contact")
        support.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        support.clicked.connect(self.actionE)
        bGrid.addWidget(support, 3, 0)

        quitbutt = QPushButton(intframe, text="Quit")
        quitbutt.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        quitbutt.clicked.connect(self.quit)
        bGrid.addWidget(quitbutt, 4, 0)

    def actionE(self):
        """
        Change the view to the Help/Support view.
        """
        print("Changed frame to Support/Contact")
        self.mainframe.changeState(SupportUI(self.mainframe, self))

    def actionP(self):
        """
        Change the view to the Persona creator view.
        """
        print("Changed frame to Persona creator")
        self.mainframe.changeState(per_creator(self.mainframe, self))

    def actionC(self):
        """
        Change the view to the Character creator view.
        """
        print("Changed frame to Character creator")
        self.mainframe.changeState(CharUI(self.mainframe, self))

    def actionS(self):
        """
        Change the view to the Social Link creator view.
        """
        print("Changed frame to SL creator")
        self.mainframe.changeState(SL_creator(self.mainframe, self))

    def quit(self):
        """
        Quit the application.
        """
        print("Exiting...")
        self.mainframe.close()
