"""
This module contains the stepping stone view for the user to select an arcana/level/angle to edit/create.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout, QComboBox, QPushButton, QLabel, QLineEdit
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt
from gui.sl_creator.qtslgui import SLFrame
from gui.sl_creator.slinfo import LinkInfo
from gui.popup import popup
from libs.sls import SocialLink
from libs import json_reader


class SLUI(QWidget):
    """
    Widget containing all arcanas, descriptions of them, and the level/angles available.

    :param MainFrame mainframe: application mainframe
    :param QWidget op: parent widget
    """
    def __init__(self, mainframe, op):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op

        # Initialized gui items...
        self.levelOM = None
        self.angleOM = None
        self.addAngB = None
        self.newAng = None
        self.go = None
        self.delang = None
        self.angs = None

        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        Does a lot of stuff.
        """
        self.mainframe.setWindowTitle("Social Link Creator")
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        arcanaList = json_reader.data_list("arcanas")

        self.arcSel = QComboBox(self)
        self.arcSel.addItem("Select Arcana")
        self.arcSel.activated.connect(self.showText)
        self.arcSel.addItems(arcanaList)
        self.arcSel.setCurrentIndex(0)
        self.grid.addWidget(self.arcSel, 1, 1)

        select = QPushButton(self, text="Select")
        select.clicked.connect(self.context)
        self.grid.addWidget(select, 2, 1)

        info = QPushButton(self, text="Info")
        info.clicked.connect(self.infoF)
        self.grid.addWidget(info, 3, 1)

        back = QPushButton(self, text="Back")
        back.clicked.connect(self.back)
        self.grid.addWidget(back, 4, 1)

        self.card = QLabel(self)
        defaultCard = QPixmap(json_reader.buildPath("int/cards/card.png"))
        self.card.setPixmap(defaultCard)
        self.card.setAlignment(Qt.AlignHCenter)
        #self.grid.addWidget(self.card, 0, 0)

        self.text = QLabel(self, text="")
        self.text.setFixedSize(400, 250)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.text, 1, 0, 4, 1)

    def infoF(self):
        """
        Enter the social link edit gui.
        """
        if self.arcSel.currentText() == "Select Arcana":
            return
        self.mainframe.changeState(LinkInfo(self.mainframe, self, SocialLink(self.arcSel.currentText())))

    def context(self):
        """
        Once an arcana is selected, spawn this view to add the level/angle information as an additional
        widget.
        """
        self.destroyContext()
        if self.arcSel.currentText() == "Select Arcana":
            return
        levs = []
        for i in range(1, 11):
            levs.append("Level " + str(i))
        self.levelOM = QComboBox(self)
        self.levelOM.addItems(levs)
        self.levelOM.setCurrentIndex(0)
        self.levelOM.activated.connect(self.fetchangles)
        self.grid.addWidget(self.levelOM, 1, 2, 1, 2)

        self.angleOM = QComboBox(self)
        self.fetchangles()
        self.grid.addWidget(self.angleOM, 2, 2, 1, 2)

        self.addAngB = QPushButton(self, text="Add Angle")
        self.addAngB.clicked.connect(self.addAngle)
        self.grid.addWidget(self.addAngB, 3, 2)

        self.newAng = QLineEdit(self)
        self.newAng.setFixedSize(20, 20)
        self.grid.addWidget(self.newAng, 3, 3)

        self.go = QPushButton(self, text="Go")
        self.go.clicked.connect(self.begin)
        self.grid.addWidget(self.go, 5, 2, 1, 2)

    def fetchangles(self):
        """
        Fetch the angles at a certain level for the display.
        """
        try:
            self.delang.close()
        except:  #pylint: disable=bare-except
            print("Failed to close delang")
        self.angs = []
        try:
            tempLink = json_reader.readLink(str(self.arcSel.currentText()))
            for decon in tempLink["cutscenes"]:
                if str(decon)[:str(decon).index("_")] == \
                   self.levelOM.currentText()[str(self.levelOM.currentText()).index(" ") + 1:]:
                    self.angs.append("Angle " + str(decon)[str(decon).index("_") + 1:])
        except:  #pylint: disable=bare-except
            pass
        if self.angs:
            print("There are angles for this level")
            self.delang = QPushButton(self, text="Delete Angle")
            self.delang.clicked.connect(self.deleteangle)
            self.grid.addWidget(self.delang, 4, 2, 1, 2)
        else:
            self.angs.append("No angles")
        self.angleOM.clear()
        self.angleOM.addItems(self.angs)
        self.angleOM.setCurrentIndex(0)

    def addAngle(self):
        """
        Add a potential angle to this link/level.
        """
        try:
            (int)(self.newAng.text())
            if self.angs[0] == "No angles":
                self.angleOM.clear()
                self.delang = QPushButton(self, text="Delete Angle")
                self.delang.clicked.connect(self.deleteangle)
                self.grid.addWidget(self.delang, 4, 2, 1, 2)
            self.angleOM.addItem("Angle "+str(self.newAng.text()))
            self.angleOM.setCurrentIndex(self.angleOM.count()-1)
            self.newAng.clear()
        except ValueError:
            popup("The Angle must be an integer", "Critical")

    def deleteangle(self):
        """
        Completely delete a certain level/angle combo. This will remove all info, the cutscene, etc.
        Dangerous.
        """
        if not popup("WARNING!!!\n\nThis will COMPLETELY ERASE this cutscene. It is HIGHLY RECOMMENDED that "
                     "you back up your data by going to the Support/Contact page and choose \"Export\".",
                     "Warning"):
            return
        link = SocialLink(self.arcSel.currentText())
        print(link.cutscenes)
        key = self.levelOM.currentText()[self.levelOM.currentText().index(" ")+1:] + \
              "_" + \
              self.angleOM.currentText()[self.angleOM.currentText().index(" ")+1:]
        print(key)
        if key in link.cutscenes:
            link.cutscenes.pop(key)
            link.save()
        self.angleOM.removeItem(self.angleOM.currentIndex())
        if self.angleOM.count() == 0:
            self.angleOM.addItem("No angles")
            self.delang.close()
        print(link.cutscenes)
        print("Deleted")

    def showText(self):
        """
        Show the arcana's descriptive text upon selection.
        """
        temp = [self.arcSel.itemText(i) for i in range(self.arcSel.count())]
        if "Select Arcana" in temp:
            self.arcSel.removeItem(temp.index("Select Arcana"))
        self.text.setText(json_reader.readArcDesc(str(self.arcSel.currentText())))
        self.card.setPixmap(QPixmap(
            json_reader.buildPath("int/cards/" + str(self.arcSel.currentText()) + ".png")
        ))
        self.destroyContext()

    def destroyContext(self):
        """
        Make sure all widgets are close when leaving the context.
        """
        try:
            self.levelOM.close()
            self.angleOM.close()
            self.addAngB.close()
            self.newAng.close()
            self.go.close()
            self.delang.close()
        except:  #pylint: disable=bare-except
            pass

    def begin(self):
        """
        Enter the social link cutscene editor.
        """
        if self.angleOM.currentText() == "No angles":
            popup("An Angle must be selected.\nCreate angles by entering a number in the text box below and "
                  "clicking \"Add Angle\"", "Critical")
            return
        enter_level = str(self.levelOM.currentText())[str(self.levelOM.currentText()).index(" ")+1:]
        enter_angle = str(self.angleOM.currentText())[str(self.angleOM.currentText()).index(" ")+1:]
        print("Entered SL creation mode for arcana " + str(self.arcSel.currentText()))
        self.mainframe.changeState(SLFrame(
            self.mainframe,
            self,
            str(self.arcSel.currentText()),
            int(enter_level),
            int(enter_angle)
        ))

    def back(self):
        """
        Return to the parent widget.
        """
        print("Returned to main screen")
        self.mainframe.changeState(self.op)
