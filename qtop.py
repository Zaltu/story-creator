from qtheader import *
from chargui import char_creator
from pergui import per_creator
from slcontextgui import SL_creator
from supgui import sup_ui

class OP(QWidget):

    def __init__(self, mainframe):
        QWidget.__init__(self)
        self.mainframe = mainframe
        print "Application started"
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(QPalette.Background, Qt.black)
        self.setPalette(p)
        self.initUI()

    def initUI(self):
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

        quit = QPushButton(intframe, text="Quit")
        quit.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        quit.clicked.connect(self.quit)
        bGrid.addWidget(quit, 4, 0)

    def actionE(self):
        print "Changed frame to Support/Contact"
        self.mainframe.changeState(sup_ui(self.mainframe, self))

    def actionP(self):
        print "Changed frame to Persona creator"
        self.mainframe.changeState(per_creator(self.mainframe, self))

    def actionC(self):
        print "Changed frame to Character creator"
        self.mainframe.changeState(char_creator(self.mainframe, self))

    def actionS(self):
        print "Changed frame to SL creator"
        self.mainframe.changeState(SL_creator(self.mainframe, self))

    def quit(self):
        print "Exiting..."
        self.mainframe.close()
