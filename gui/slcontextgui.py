from PySide.QtGui import QWidget, QGridLayout, QComboBox, QPushButton, QLabel, QPixmap, QLineEdit
from PySide.QtCore import Qt
from gui.qtslgui import SLFrame
from gui.slinfo import LinkInfo
from gui.popup import popup
from libs.sls import SocialLink
from libs import json_reader


class SL_creator(QWidget):

    def __init__(self, mainframe, op):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.initUI()

    def initUI(self):
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
        self.grid.addWidget(self.card, 0, 0)

        self.text = QLabel(self, text="")
        self.text.setFixedSize(400, 250)
        self.text.setWordWrap(True)
        self.text.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.text, 1, 0, 4, 1)

    def infoF(self):
        if self.arcSel.currentText() == "Select Arcana":
            return
        self.mainframe.changeState(LinkInfo(self.mainframe, self, SocialLink(self.arcSel.currentText())))

    def context(self):
        self.destroyContext()
        if self.arcSel.currentText() == "Select Arcana":
            return
        levs = []
        for x in range(1, 11):
            levs.append("Level " + str(x))
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
        try:
                self.delang.close()
        except:
            print "Failed to close delang"
        self.angs = []
        try:
            tempLink = json_reader.readLink(str(self.arcSel.currentText()))
            for decon in tempLink["cutscenes"]:
                if str(decon)[:str(decon).index("_")] == self.levelOM.currentText()[str(self.levelOM.currentText()).index(" ") + 1:]:
                    self.angs.append("Angle " + str(decon)[str(decon).index("_") + 1:])
        except:
            pass
        if self.angs:
            print "There are angles for this level"
            self.delang = QPushButton(self, text="Delete Angle")
            self.delang.clicked.connect(self.deleteangle)
            self.grid.addWidget(self.delang, 4, 2, 1, 2)
        else:
            self.angs.append("No angles")
        self.angleOM.clear()
        self.angleOM.addItems(self.angs)
        self.angleOM.setCurrentIndex(0)

    def addAngle(self):
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
        except Exception as e:
            print e
            popup("The Angle must be an integer", "Critical")
            print "Angle must be an integer"

    def deleteangle(self):
        if not popup("WARNING!!!\n\nThis will COMPLETELY ERASE this cutscene. It is HIGHLY RECOMMENDED that you back up your data by going to the Support/Contact page and choose \"Export\".", "Warning"):
            return
        link = SocialLink(self.arcSel.currentText())
        print link.cutscenes
        key = self.levelOM.currentText()[self.levelOM.currentText().index(" ")+1:] + "_" + self.angleOM.currentText()[self.angleOM.currentText().index(" ")+1:]
        print key
        if key in link.cutscenes:
            link.cutscenes.pop(key)
            link.save()
        self.angleOM.removeItem(self.angleOM.currentIndex())
        if self.angleOM.count() == 0:
            self.angleOM.addItem("No angles")
            self.delang.close()
        print link.cutscenes
        print "Deleted"

    def showText(self):
        temp = [self.arcSel.itemText(i) for i in range(self.arcSel.count())]
        if "Select Arcana" in temp:
            self.arcSel.removeItem(temp.index("Select Arcana"))
        self.text.setText(json_reader.readArcDesc(str(self.arcSel.currentText())))
        self.card.setPixmap(QPixmap(json_reader.buildPath("int/cards/"+str(self.arcSel.currentText())+".png")))
        self.destroyContext()

    def destroyContext(self):
        try:
            self.levelOM.close()
            self.angleOM.close()
            self.addAngB.close()
            self.newAng.close()
            self.go.close()
            self.delang.close()
        except:
            pass

    def begin(self):
        if self.angleOM.currentText() == "No angles":
            popup("An Angle must be selected.\nCreate angles by entering a number in the text box below and clicking \"Add Angle\"", "Critical")
            return
        enter_level = str(self.levelOM.currentText())[str(self.levelOM.currentText()).index(" ")+1:]
        enter_angle = str(self.angleOM.currentText())[str(self.angleOM.currentText()).index(" ")+1:]
        print "Entered SL creation mode for arcana " + str(self.arcSel.currentText())
        #self.destroyContext()
        self.mainframe.changeState(SLFrame(self.mainframe, self, str(self.arcSel.currentText()), (int)(enter_level), (int)(enter_angle)))

    def back(self):
        print "Returned to main screen"
        self.mainframe.changeState(self.op)
