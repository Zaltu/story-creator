from PySide.QtGui import QWidget, QGridLayout, QLabel, QComboBox, QTextEdit, QLineEdit, QPushButton
from PySide.QtCore import Qt
from gui.popup import popup
from libs import json_reader

class LinkInfo(QWidget):

    def __init__(self, mainframe, op, link, linklevel=None, linkangle=None):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.link = link
        self.linklevel = linklevel
        self.linkangle = linkangle
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.levang = {}
        elev = []

        for key, cutscene in self.link.cutscenes.iteritems():
            if key[:key.index("_")] in self.levang:
                self.levang[key[:key.index("_")]].append(key[key.index("_")+1:])
            else:
                self.levang[key[:key.index("_")]] = [key[key.index("_")+1:]]
            if key[:key.index("_")] not in elev:
                elev.append(key[:key.index("_")])
        for level, angle in self.levang.iteritems():
            angle.sort(key=lambda angle: (int)(angle))
        elev.sort(key=lambda level: (int)(level))
        infoL = QLabel(self, text="Social Link Information")
        self.grid.addWidget(infoL, 0, 0, 1, 12)

        self.level = QComboBox(self)
        if len(elev) != 0:
            elev.insert(0, "")
            self.level.addItems(elev)
            self.level.activated.connect(self.recs)
            if self.linklevel:
                self.level.setCurrentIndex((int)(self.linklevel))
                self.recs()
        else:
            self.level.addItems(["No cutscenes have been created"])
        self.grid.addWidget(self.level, 1, 1, 1, 1)

        atlevel = QLabel(self, text="At " + self.link.arcana + " level ")
        self.grid.addWidget(atlevel, 1, 0, 1, 1)

        arcanainfo = QLabel(self, text=self.link.arcana + " Social Link info")
        self.aitext = QTextEdit(self)
        self.aitext.setText(self.link.info)
        self.aitext.setFixedSize(300, 100)

        self.save = QPushButton(self, text="Save")
        self.back = QPushButton(self, text="Back")
        self.save.clicked.connect(self.saveinfo)
        self.back.clicked.connect(self.endedit)

        if self.linklevel and self.linkangle:
            self.grid.addWidget(arcanainfo, 4, 0, 1, 6)
            self.grid.addWidget(self.aitext, 5, 0, 1, 6)

            thisinfo = QLabel(self, text=self.link.arcana + " info for level: " + self.linklevel + ", angle: " + self.linkangle)
            self.grid.addWidget(thisinfo, 4, 6, 1, 6)

            self.titext = QTextEdit(self)
            self.titext.setFixedSize(300, 100)
            try:
                self.titext.setText(self.link.cutinfo[self.level.currentText()+"_"+str(self.linkangle)])
            except:
                pass
            self.grid.addWidget(self.titext, 5, 6, 1, 6)

            self.grid.setAlignment(thisinfo, Qt.AlignHCenter)
            self.grid.setAlignment(self.titext, Qt.AlignHCenter)
        else:
            self.grid.addWidget(arcanainfo, 4, 0, 1, 12)
            self.grid.addWidget(self.aitext, 5, 0, 1, 12)


        pseudoL = QLabel(self, text="Social Link's Pseudoname")
        youhave = QLabel(self, text="You have established the ")
        ofthe = QLabel(self, text="Social Link of the " + self.link.arcana + " arcana!")

        self.grid.addWidget(pseudoL, 2, 0, 1, 12)
        self.grid.addWidget(youhave, 3, 0, 1, 5)
        self.grid.addWidget(ofthe, 3, 7, 1, 6)

        self.grid.addWidget(self.save, 6, 0, 1, 1)
        self.grid.addWidget(self.back, 6, 1, 1, 1)

        self.pseudoname = QLineEdit(self)
        self.pseudoname.setFixedSize(150, 20)
        self.pseudoname.setText(self.link.pseudoname)
        self.grid.addWidget(self.pseudoname, 3, 5, 1, 2)

        self.grid.setAlignment(infoL, Qt.AlignHCenter)
        self.grid.setAlignment(self.aitext, Qt.AlignHCenter)
        self.grid.setAlignment(arcanainfo, Qt.AlignHCenter)
        self.grid.setAlignment(self.save, Qt.AlignRight)
        self.grid.setAlignment(self.back, Qt.AlignLeft)
        self.grid.setAlignment(youhave, Qt.AlignRight)
        self.grid.setAlignment(ofthe, Qt.AlignLeft)
        self.grid.setAlignment(pseudoL, Qt.AlignHCenter)
        self.grid.setAlignment(self.pseudoname, Qt.AlignHCenter)

    def saveinfo(self):
        try:
            for angle, data in self.reqs.textboxes.iteritems():
                (int)(data.text())
                if data.text() != "":
                    if self.level.currentText() not in  self.link.requiredPoints:
                        self.link.requiredPoints[self.level.currentText()] = {}
                    if angle not in self.link.requiredPoints[self.level.currentText()]:
                        self.link.requiredPoints[self.level.currentText()][angle] = {}
                    self.link.requiredPoints[self.level.currentText()][angle]['points'] = (int)(data.text())
            for angle, data in self.reqs.courages.iteritems():
                self.link.requiredPoints[self.level.currentText()][angle]['courage'] = (int)(data.currentText())
            for angle, data in self.reqs.charms.iteritems():
                self.link.requiredPoints[self.level.currentText()][angle]['charm'] = (int)(data.currentText())
            for angle, data in self.reqs.acads.iteritems():
                self.link.requiredPoints[self.level.currentText()][angle]['acad'] = (int)(data.currentText())
            for angle, data in self.reqs.ultis.iteritems():
                self.link.finalpersona[angle] = data.currentText()
            self.link.pseudoname = self.pseudoname.text()
            self.link.info = self.aitext.toPlainText()
            if self.linklevel:
                if str(self.linklevel)+"_"+str(self.linkangle) not in self.link.cutinfo:
                    self.link.cutinfo[str(self.linklevel)+"_"+str(self.linkangle)] = ""
                self.link.cutinfo[str(self.linklevel)+"_"+str(self.linkangle)] = self.titext.toPlainText()
        except:
            popup("Points must be integers.\nNot saved.", "Critical")
            return
        self.link.save()
        popup("Saved", "Information")

    def endedit(self):
        self.mainframe.changeState(self.op)


    def recs(self):
        try:
            self.reqs.close()
        except Exception as e:
            print e
            print "Can't close oudated req widget"
        if self.level.currentText() == "":
            return
        if self.level.itemText(0) == "":
            self.level.removeItem(0)

        self.reqs = Requirements(self)
        self.grid.addWidget(self.reqs, 1, 2, 1, 10)


class Requirements(QWidget):
    def __init__(self, op):
        QWidget.__init__(self)
        self.op = op
        self.textboxes = {}
        self.eangs = []
        self.courages = {}
        self.charms = {}
        self.acads = {}
        self.ultis = {}
        self.plist = json_reader.readPerNames()
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        rowi = 0

        if self.op.level.currentText() == '10':
            for angle in self.op.levang[self.op.level.currentText()]:
                self.grid.addWidget(QLabel(self, text="Finishing at angle " + angle + ":\tWe bestow upon thee the ability to create"), rowi, 0)
                ulti = QComboBox(self)
                ulti.addItems(self.plist)
                if angle in self.op.link.finalpersona:
                    ulti.setCurrentIndex(self.plist.index(self.op.link.finalpersona[angle]))
                self.ultis[angle] = ulti
                self.grid.addWidget(self.ultis[angle], rowi, 1)
                self.grid.addWidget(QLabel(self, text=", the ultimate form of the " + self.op.link.arcana + " arcana."), rowi, 2)
                rowi += 1
            return

        for angle in self.op.levang[self.op.level.currentText()]:
            eang = QLabel(self, text=angle)
            self.eangs.append(eang)
            ptb = QLineEdit(self)
            ptb.setText("0")
            ptb.setFixedSize(20, 20)
            self.textboxes[angle] = ptb
            self.grid.addWidget(QLabel(self, text="Reaching angle"), rowi, 0)
            self.grid.addWidget(self.eangs[-1], rowi, 1)
            self.grid.addWidget(QLabel(self, text="requires"), rowi, 2)
            self.grid.addWidget(self.textboxes[angle], rowi, 3)
            self.grid.addWidget(QLabel(self, text="points and: Courage"), rowi, 4)
            courage = QComboBox(self)
            self.courages[angle] = courage
            self.courages[angle].addItems(["1", "2", "3", "4", "5"])
            self.courages[angle].setCurrentIndex(0)
            self.grid.addWidget(self.courages[angle], rowi, 5)
            self.grid.addWidget(QLabel(self, text="Charm"), rowi, 6)
            charm = QComboBox(self)
            self.charms[angle] = charm
            self.charms[angle].addItems(["1", "2", "3", "4", "5"])
            self.charms[angle].setCurrentIndex(0)
            self.grid.addWidget(self.charms[angle], rowi, 7)
            self.grid.addWidget(QLabel(self, text="Academics"), rowi, 8)
            acad = QComboBox(self)
            self.acads[angle] = acad
            self.acads[angle].addItems(["1", "2", "3", "4", "5"])
            self.acads[angle].setCurrentIndex(0)
            self.grid.addWidget(self.acads[angle], rowi, 9)
            if self.op.level.currentText() in self.op.link.requiredPoints and angle in self.op.link.requiredPoints[self.op.level.currentText()]:
                self.textboxes[angle].setText(str(self.op.link.requiredPoints[self.op.level.currentText()][angle]['points']))
                self.acads[angle].setCurrentIndex(self.op.link.requiredPoints[self.op.level.currentText()][angle]['acad']-1)
                self.charms[angle].setCurrentIndex(self.op.link.requiredPoints[self.op.level.currentText()][angle]['charm']-1)
                self.courages[angle].setCurrentIndex(self.op.link.requiredPoints[self.op.level.currentText()][angle]['courage']-1)
            rowi += 1

"""app = QApplication(sys.argv)
sl = SocialLink("Void")
sl.pseudoname = "Chaos"
sl.finalpersona[5] = "Jack Frost"
sl.finalpersona[15] = "Seraph"
li = LinkInfo(sl, '1', '42')
li.show()
sys.exit(app.exec_())"""