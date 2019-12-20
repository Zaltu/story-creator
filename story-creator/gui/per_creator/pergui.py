#pylint: disable=no-name-in-module
import os
from PySide2.QtWidgets import QWidget, QGridLayout, QListWidget, QPushButton, QLabel, QLineEdit, QComboBox, QTextEdit
from gui.popup import popup
from libs.creatures import Persona
from libs import json_reader


class per_creator(QWidget):

    def __init__(self, mainframe, op):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.listP = None
        self.listLS = None
        self.listEL1 = None
        self.listEL2 = None

        self.nameT = None
        self.levelT = None
        self.textT = None
        self.strT = None
        self.magT = None
        self.endT = None
        self.agiT = None
        self.luckT = None

        self.createFrame = None

        self.initUI(True)

    def initUI(self, infoDump):
        self.mainframe.setWindowTitle("Persona Creator")

        if not infoDump:
            self.createFrameDraw()

        self.initButtonFrame(infoDump)

        self.listP = QListWidget(self)
        self.grid.addWidget(self.listP, 0, 3, 2, 1)
        temp = json_reader.readPerNames()
        self.listP.addItems(temp)

    def initButtonFrame(self, infoDump):
        self.buttonFrame = QWidget(self)
        self.bfgrid = QGridLayout()
        self.buttonFrame.setLayout(self.bfgrid)

        self.grid.addWidget(self.buttonFrame, 3, 0, 1, 4)


        new = QPushButton(self.buttonFrame, text="New")
        new.clicked.connect(self.new)
        self.bfgrid.addWidget(new, 4, 0)

        back = QPushButton(self.buttonFrame, text="Back")
        back.clicked.connect(self.back)
        self.bfgrid.addWidget(back, 4, 4)

        remove = QPushButton(self.buttonFrame, text="Remove")
        remove.clicked.connect(self.remove)
        self.bfgrid.addWidget(remove, 4, 3)

        edit = QPushButton(self.buttonFrame, text="Edit")
        edit.clicked.connect(self.edit)
        self.bfgrid.addWidget(edit, 4, 2)

        if not infoDump:
            save = QPushButton(self.buttonFrame, text="Save")
            save.clicked.connect(self.save)
            self.bfgrid.addWidget(save, 4, 1)


    def createFrameDraw(self):
        self.createFrame = QWidget(self)
        self.cfgrid = QGridLayout()
        self.createFrame.setLayout(self.cfgrid)
        self.grid.addWidget(self.createFrame, 0, 0, 2, 2)

        self.lsdic = {}

        nameL = QLabel(self.createFrame, text="Name:")
        self.cfgrid.addWidget(nameL, 0, 0)
        self.nameT = QLineEdit(self.createFrame)
        self.nameT.setFixedSize(100, 20)
        self.cfgrid.addWidget(self.nameT, 0, 1)

        strL = QLabel(self.createFrame, text="Str")
        self.cfgrid.addWidget(strL, 0, 2)
        self.strT = QLineEdit(self.createFrame)
        self.strT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.strT, 0, 3)
        magL = QLabel(self.createFrame, text="Mag")
        self.cfgrid.addWidget(magL, 1, 2)
        self.magT = QLineEdit(self.createFrame)
        self.magT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.magT, 1, 3)
        endL = QLabel(self.createFrame, text="End")
        self.cfgrid.addWidget(endL, 2, 2)
        self.endT = QLineEdit(self.createFrame)
        self.endT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.endT, 2, 3)
        agiL = QLabel(self.createFrame, text="Agi")
        self.cfgrid.addWidget(agiL, 3, 2)
        self.agiT = QLineEdit(self.createFrame)
        self.agiT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.agiT, 3, 3)
        luckL = QLabel(self.createFrame, text="Luck")
        self.cfgrid.addWidget(luckL, 4, 2)
        self.luckT = QLineEdit(self.createFrame)
        self.luckT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.luckT, 4, 3)

        resList = json_reader.data_list("resistances")
        resL = QLabel(self.createFrame, text="Resistance:")
        self.cfgrid.addWidget(resL, 0, 5)
        slashL = QLabel(self.createFrame, text="Slash")
        self.cfgrid.addWidget(slashL, 1, 5)
        self.slashO = QComboBox(self.createFrame)
        self.slashO.addItems(resList)
        self.slashO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.slashO, 1, 6)
        strikeL = QLabel(self.createFrame, text="Strike")
        self.cfgrid.addWidget(strikeL, 2, 5)
        self.strikeO = QComboBox(self.createFrame)
        self.strikeO.addItems(resList)
        self.strikeO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.strikeO, 2, 6)
        pierceL = QLabel(self.createFrame, text="Pierce")
        self.cfgrid.addWidget(pierceL, 3, 5)
        self.pierceO = QComboBox(self.createFrame)
        self.pierceO.addItems(resList)
        self.pierceO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.pierceO, 3, 6)
        fireL = QLabel(self.createFrame, text="Fire")
        self.cfgrid.addWidget(fireL, 4, 5)
        self.fireO = QComboBox(self.createFrame)
        self.fireO.addItems(resList)
        self.fireO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.fireO, 4, 6)
        iceL = QLabel(self.createFrame, text="Ice")
        self.cfgrid.addWidget(iceL, 5, 5)
        self.iceO = QComboBox(self.createFrame)
        self.iceO.addItems(resList)
        self.iceO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.iceO, 5, 6)
        elecL = QLabel(self.createFrame, text="Elec")
        self.cfgrid.addWidget(elecL, 6, 5)
        self.elecO = QComboBox(self.createFrame)
        self.elecO.addItems(resList)
        self.elecO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.elecO, 6, 6)
        windL = QLabel(self.createFrame, text="Wind")
        self.cfgrid.addWidget(windL, 7, 5)
        self.windO = QComboBox(self.createFrame)
        self.windO.addItems(resList)
        self.windO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.windO, 7, 6)
        lightL = QLabel(self.createFrame, text="Light")
        self.cfgrid.addWidget(lightL, 8, 5)
        self.lightO = QComboBox(self.createFrame)
        self.lightO.addItems(resList)
        self.lightO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.lightO, 8, 6)
        darkL = QLabel(self.createFrame, text="Dark")
        self.cfgrid.addWidget(darkL, 9, 5)
        self.darkO = QComboBox(self.createFrame)
        self.darkO.addItems(resList)
        self.darkO.setCurrentIndex(1)
        self.cfgrid.addWidget(self.darkO, 9, 6)

        spellList = json_reader.data_list("spells")
        self.listLS = QListWidget(self.createFrame)
        self.listLS.setFixedSize(200, 300)
        self.cfgrid.addWidget(self.listLS, 3, 7, 8, 2)

        newLS = QPushButton(self.createFrame, text="+")
        newLS.clicked.connect(self.addLS)
        self.cfgrid.addWidget(newLS, 2, 7)
        delLS = QPushButton(self.createFrame, text="DEL")
        delLS.clicked.connect(self.delLS)
        self.cfgrid.addWidget(delLS, 2, 8)

        LSL = QLabel(self.createFrame, text="Learned Spells:")
        self.cfgrid.addWidget(LSL, 0, 7, 1, 2)

        arcanaL = QLabel(self.createFrame, text="Arcana:")
        self.cfgrid.addWidget(arcanaL, 1, 0)
        list = json_reader.data_list("arcanas")
        self.arcO = QComboBox(self.createFrame)
        self.arcO.addItems(list)
        self.arcO.setCurrentIndex(0)
        self.cfgrid.addWidget(self.arcO, 1, 1)

        levelL = QLabel(self.createFrame, text="Level:")
        self.cfgrid.addWidget(levelL, 2, 0)
        self.levelT = QLineEdit(self.createFrame)
        self.levelT.setFixedSize(20, 20)
        self.cfgrid.addWidget(self.levelT, 2, 1)

        heritageL = QLabel(self.createFrame, text="Inherits:")
        self.cfgrid.addWidget(heritageL, 3, 0, 1, 2)

        elements = json_reader.data_list("elements")
        elements.append("Support")
        self.listEL1 = QComboBox(self.createFrame)
        self.listEL1.addItems(elements)
        self.cfgrid.addWidget(self.listEL1, 4, 0)
        self.listEL2 = QComboBox(self.createFrame)
        self.listEL2.addItems(elements)
        self.cfgrid.addWidget(self.listEL2, 4, 1)

        iSpellL = QLabel(self.createFrame, text="Initial Spells:")
        self.cfgrid.addWidget(iSpellL, 5, 0, 1, 2)
        self.iSpellOs = []
        for i in range(6, 9):
            temp = QComboBox(self.createFrame)
            temp.addItems(spellList)
            temp2 = QComboBox(self.createFrame)
            temp2.addItems(spellList)
            self.cfgrid.addWidget(temp, i, 0, 1, 2)
            self.cfgrid.addWidget(temp2, i, 2, 1, 2)
            self.iSpellOs.extend([temp, temp2])

        textL = QLabel(self.createFrame, text="Info:")
        self.cfgrid.addWidget(textL, 10, 0)
        self.textT = QTextEdit(self.createFrame)
        self.textT.setFixedSize(300, 100)
        self.cfgrid.addWidget(self.textT, 10, 1, 1, 5)

        self.lslevel = QLineEdit(self.createFrame)
        self.lslevel.setFixedSize(40, 20)
        self.lsSpellO = QComboBox(self.createFrame)
        self.lsSpellO.addItems(spellList)

        self.cfgrid.addWidget(self.lsSpellO, 1, 7)
        self.cfgrid.addWidget(self.lslevel, 1, 8)

    def addLS(self):
        print("Adding learned spell")
        self.chosenSpell = self.lsSpellO.currentText()
        try:
            self.lstext = (int)(self.lslevel.text())
            if self.lstext <= (int)(self.levelT.text()):
                raise Exception("")
            if not (self.chosenSpell == ""):
                print("Ok")
                self.lsdic[self.chosenSpell] = self.lslevel.text()
                self.listLS.addItem(self.chosenSpell + " at level " + self.lslevel.text())
                self.lslevel.setText("")
                self.lsSpellO.setCurrentIndex(0)
                return
        except:
            popup("You must enter a level that is greater than the Persona's level.", "Critical")
            print("Not an integer or level smaller than Persona's level, not saved")
            return
        popup("You must choose a spell", "Critical")
        print("You must choose a spell")


    def delLS(self):
        print("Deleting learned spell")
        key = ""
        i = 0
        while len(self.listLS.currentItem().text()) > i:
            if self.listLS.currentItem().text()[i] == " " and self.listLS.currentItem().text()[i+1] == "a" and self.listLS.currentItem().text()[i+2] == "t":
                break
            key += self.listLS.currentItem().text()[i]
            i = i + 1
        print(key)
        print(self.lsdic.pop(key))
        self.listLS.takeItem(self.listLS.currentRow())


    def loadPer(self, name):
        data = json_reader.readOne(name, 'pers')
        self.nameT.setText(data["name"])
        self.textT.setText(data["desc"])
        self.strT.setText(data["stats"][0])
        self.magT.setText(data["stats"][1])
        self.endT.setText(data["stats"][2])
        self.agiT.setText(data["stats"][3])
        self.luckT.setText(data["stats"][4])
        self.levelT.setText(data["level"])

        self.arcO.setCurrentIndex([self.arcO.itemText(i) for i in range(self.arcO.count())].index(data["arcana"]))

        self.listEL1.setCurrentIndex([self.listEL1.itemText(i) for i in range(self.listEL1.count())].index(data["heritage"][0]))
        self.listEL2.setCurrentIndex([self.listEL2.itemText(i) for i in range(self.listEL2.count())].index(data["heritage"][1]))

        self.slashO.setCurrentIndex([self.slashO.itemText(i) for i in range(self.slashO.count())].index(data["resistance"][0]))
        self.strikeO.setCurrentIndex([self.strikeO.itemText(i) for i in range(self.strikeO.count())].index(data["resistance"][1]))
        self.pierceO.setCurrentIndex([self.pierceO.itemText(i) for i in range(self.pierceO.count())].index(data["resistance"][2]))
        self.fireO.setCurrentIndex([self.fireO.itemText(i) for i in range(self.fireO.count())].index(data["resistance"][3]))
        self.iceO.setCurrentIndex([self.iceO.itemText(i) for i in range(self.iceO.count())].index(data["resistance"][4]))
        self.elecO.setCurrentIndex([self.elecO.itemText(i) for i in range(self.elecO.count())].index(data["resistance"][5]))
        self.windO.setCurrentIndex([self.windO.itemText(i) for i in range(self.windO.count())].index(data["resistance"][6]))
        self.lightO.setCurrentIndex([self.lightO.itemText(i) for i in range(self.lightO.count())].index(data["resistance"][7]))
        self.darkO.setCurrentIndex([self.darkO.itemText(i) for i in range(self.darkO.count())].index(data["resistance"][8]))

        i = 0
        for combobox in self.iSpellOs:
            combobox.setCurrentIndex([combobox.itemText(j) for j in range(combobox.count()-1)].index(data["spellDeck"][i]))
            i += 1

        self.lsdic = data["spellLearn"]
        self.listLS.clear()
        for spell, level in self.lsdic.items():
            self.listLS.addItem(spell + " at level " + level)

        print("Loaded " + data["name"])

    def edit(self):
        try:
            if self.listP.currentItem().text() != "":
                if self.createFrame and not popup("Override any unsaved changes?", "Warning"):
                    return
                self.loadPer(self.listP.currentItem().text())
        except AttributeError:#To initialize createFrame UI before load
            if self.listP.currentItem().text() != "":
                temp = self.listP.currentItem().text()
                self.buttonFrame.close()
                self.initUI(False)
                self.loadPer(temp)
            else:
                return
        self.createFrame.show()
        self.mainframe.center()
        print("Changed to edit frame")

    def save(self):
        if os.path.exists(json_reader.buildPath("data/pers/"+self.nameT.text()+".json")):
            if not popup("Override existing Persona "+self.nameT.text()+"?", "Question"):
                return
        print("Saving")
        spellDeck = []
        for combobox in self.iSpellOs:
            spellDeck.append(combobox.currentText())
        stats = [self.strT.text(), self.magT.text(), self.endT.text(), self.agiT.text(), self.luckT.text()]
        res = [self.slashO.currentText(), self.strikeO.currentText(), self.pierceO.currentText(), self.fireO.currentText(), self.iceO.currentText(), self.elecO.currentText(), self.windO.currentText(), self.lightO.currentText(), self.darkO.currentText()]
        try:
            (int)(self.levelT.text())
            (int)(self.strT.text())
            (int)(self.magT.text())
            (int)(self.endT.text())
            (int)(self.agiT.text())
            (int)(self.luckT.text())
        except:
            popup("There is a number entry that isn't valid.\nEntries requiring numbers are:\nLEVEL\nSTR\nMAG\nEND\nAGI\nLUCK", "Critical")
            print("Not Saved")
            return
        if not (self.nameT.text() and not self.nameT.text().isspace()):
            popup("No name entered for your Persona. Name is a required field.", "Critical")
            print("No Name, not saved")
            return
        toWrite = Persona(self.nameT.text(), self.arcO.currentText(), self.levelT.text(), self.textT.toPlainText(), spellDeck, self.lsdic, stats, res, [self.listEL1.currentText(), self.listEL2.currentText()])
        json_reader.writeOne(toWrite, 'pers')
        temp = self.nameT.text()
        if (temp not in [self.listP.item(i).text() for i in range(self.listP.count())]):
            self.listP.addItem(temp)
        self.loadPer(temp)
        print("Saved Persona")

    def remove(self):
        if self.listP.currentItem().text() == "":
            return
        if not popup("Are you certain you want to completely remove this Persona?\n(Cannot be undone)", "Warning"):
            return
        print("Removing Persona " + self.listP.currentItem().text())
        json_reader.deletePer(self.listP.currentItem().text())
        self.listP.takeItem([self.listP.item(i).text() for i in range(self.listP.count())].index(self.listP.currentItem().text()))


    def new(self):
        if self.createFrame and not popup("Override any unsaved changes?", "Warning"):
            return
        self.buttonFrame.close()
        self.initUI(False)
        self.createFrame.show()
        self.mainframe.center()
        print("Created")

    def back(self):
        print("Returned to main screen")
        self.mainframe.changeState(self.op)
