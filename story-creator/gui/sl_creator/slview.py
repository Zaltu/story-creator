#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PySide2.QtGui import QPalette, QPen, QPainter
from PySide2.QtCore import Qt, QPoint
from gui.popup import popup
from libs.action import Speak

class PrettySL(QWidget):

    def __init__(self, mainframe, op):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.graph = self.op.link
        self.table = self.op.link.items
        self.lastButtonPressed = None
        self.needsRefresh = False
        self.subtree = []
        self.delete = None
        self.initData()
        self.initUI()


    def initData(self):
        self.lab = None
        self.actionIDs = self.graph.getIDs()
        self.actionObjs = []
        for act in self.table:
            self.actionObjs.append(act[0])

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.tree = TreeWidget(self, self.actionObjs, self.actionIDs, self.table)


        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.tree)
        if self.tree.rect().width() < 600:
            self.scrollArea.setFixedWidth(self.tree.rect().width()+25)
        else:
            self.scrollArea.setFixedWidth(600)
        if self.tree.rect().height() < 600:
            self.scrollArea.setFixedHeight(self.tree.rect().height())
        else:
            self.scrollArea.setFixedHeight(600)
        self.scrollArea.ensureWidgetVisible(self.tree, 500, 500)

        self.grid.addWidget(self.scrollArea, 0, 0, 10, 3)

        self.legend = Legend(self)
        self.grid.addWidget(self.legend, 0, 3, 1, 2)

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def trackIndex(self, index):
        self.needsRefresh = True
        self.lastButtonPressed = index
        self.subtree = self.graph.subTree(index)
        print(self.subtree)
        self.initInfoUI(index)

    def deleteSubtree(self):
        if not popup("Are you certain you want to delete this item and it's subtree?\n(Everything in red and yellow will be deleted)", "Warning"):
            return
        self.graph.delItem(self.lastButtonPressed)
        self.lab.close()
        self.initData()
        self.lastButtonPressed = None
        self.delete.close()
        self.delete = None
        self.subtree = []
        self.needsRefresh = True
        self.idLabel.close()
        self.edit.clicked.disconnect()
        self.edit.close()
        self.op.linkstored.save()
        self.tree.close()
        self.tree = TreeWidget(self, self.actionObjs, self.actionIDs, self.table)
        self.grid.addWidget(self.tree, 0, 0, 10, 3)

    def initInfoUI(self, index):
        if not self.lab:
            self.lab = QLabel(self, text="Selected element summary:")
            self.grid.addWidget(self.lab, 2, 3, 1, 2)
            idt = ""
            if isinstance(self.table[index][0], Speak):
                idt += self.table[index][0].speaker + " says:\n\n"
            idt += self.actionIDs[index]
            self.idLabel = QLabel(self, text=idt)
            self.idLabel.setFixedSize(300, 40)
            self.idLabel.setWordWrap(True)
            self.grid.addWidget(self.idLabel, 3, 3, 1, 2)
            self.edit = QPushButton(self, text="Edit")
            self.edit.clicked.connect(lambda: self.enter(index))
            self.grid.addWidget(self.edit, 4, 3, 1, 2)
            self.lkst = QLabel(self, text="Selected element links to:")
            self.grid.addWidget(self.lkst, 5, 3, 1, 2)
            self.rels = QLabel(self)
            self.rels.setMaximumWidth(300)
            text = ""
            for relation in self.table[index][1:len(self.table[index])]:
                text += "(" + str(relation) + ") " + self.graph.getOneID(self.table[relation][0]) + "\n\n"
            self.rels.setText(text)
            self.grid.addWidget(self.rels, 6, 3, 1, 2)
        else:
            text = ""
            idt = ""
            if isinstance(self.table[index][0], Speak):
                idt += self.table[index][0].speaker + " says:\n\n"
            idt += self.actionIDs[index]
            self.idLabel.setText(idt)
            for relation in self.table[index][1:len(self.table[index])]:
                text += "(" + str(relation) + ") " + self.graph.getOneID(self.table[relation][0]) + "\n\n"
            self.rels.setText(text)
            self.edit.clicked.disconnect()
            self.edit.clicked.connect(lambda: self.enter(index))
        if not self.delete:
            self.delete = QPushButton(self, text="Delete element and subtree")
            self.delete.clicked.connect(self.deleteSubtree)
            self.grid.addWidget(self.delete, 1, 3, 1, 2)

    def enter(self, index):
        load = self.graph.getItem(index)
        self.close()
        self.op.view.setText("Graphic View")
        self.op.view.clicked.disconnect()
        self.op.view.clicked.connect(lambda: self.op.viewF(True))
        self.op.listview.changeFrame(load, index)



class Legend(QWidget):

    def __init__(self, op):
        QWidget.__init__(self)
        self.op = op
        self.fixed = False
        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.lab = QLabel(self, text="Legend")
        self.grid.addWidget(self.lab, 0, 0, 1, 2)

        self.dd = QLabel(self, text="Downstream dependancy:")
        self.grid.addWidget(self.dd, 1, 0)

        self.ud = QLabel(self, text="Upstream dependancy:")
        self.grid.addWidget(self.ud, 2, 0)

        self.unid = QLabel(self, text="Unique dependancy:")
        self.grid.addWidget(self.unid, 3, 0)

        self.sel = QLabel(self, text="Selected element:")
        self.grid.addWidget(self.sel, 4, 0)

        self.leaf = QLabel(self, text="End(s) of cutscene:")
        self.grid.addWidget(self.leaf, 5, 0)

        empty = QLabel(self)
        empty.setFixedSize(150, 20)
        self.grid.addWidget(empty, 1, 1)
        self.grid.addWidget(empty, 2, 1)
        self.grid.addWidget(empty, 3, 1)
        self.grid.addWidget(empty, 4, 1)
        self.grid.addWidget(empty, 5, 1)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)

        qp.drawRect(self.rect().left(), self.rect().top(), self.rect().width(), self.rect().height())

        qp.drawLine(self.dd.x()+155, self.dd.y()+5, self.dd.x()+250, self.dd.y()+5)
        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(self.ud.x()+155, self.ud.y()+5, self.ud.x()+250, self.ud.y()+5)
        pen.setStyle(Qt.SolidLine)
        pen.setColor(Qt.red)
        qp.setPen(pen)
        qp.drawLine(self.unid.x()+155, self.unid.y()+5, self.unid.x()+250, self.unid.y()+5)
        pen.setColor(Qt.yellow)
        qp.setPen(pen)
        qp.drawRect(self.sel.x()+155, self.sel.y(), 95, 20)
        pen.setColor(Qt.green)
        qp.setPen(pen)
        qp.drawRect(self.leaf.x()+155, self.leaf.y(), 95, 20)

class TreeWidget(QWidget):

    def __init__(self, op, actions, ids, table):
        QWidget.__init__(self)
        self.actions = actions
        self.ids = ids
        self.table = table
        self.op = op
        self.currentDepth = 0
        self.initUI()


    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.processed = [0]
        self.map = [(0, 0)]
        self.needsLine = []
        self.depthTracker = {}
        self.buttons = []

        self.nextRow(self.table[0], 1)

        self.mapped = {}
        for element in self.map:
            self.mapped[element[0]] = element[1]

        self.placedInLine = {}
        self.lineWidgets = {}
        self.buttons = {}

        for element in self.map:
            if element[1] not in self.lineWidgets:
                self.lineWidgets[element[1]] = (QWidget(), QHBoxLayout())
                self.lineWidgets[element[1]][0].setLayout(self.lineWidgets[element[1]][1])
            tempB = QPushButton(self.lineWidgets[element[1]][0], text=self.ids[element[0]])
            tempB.setFixedSize(150, 20)
            # Causes memory leak because lambda prevents button from being cleaned up.
            # _=False because PySide2 sends a state object to the connecting function as well.
            tempB.clicked.connect(lambda _=False, ind=element[0]: self.op.trackIndex(ind))
            self.lineWidgets[element[1]][1].addWidget(tempB)
            self.buttons[element[0]] = tempB
        for lineNumber, widget in self.lineWidgets.items():
            self.grid.addWidget(widget[0], lineNumber, 0)


    def nextRow(self, currentAction, currentDepth):
        for relation in currentAction[1:len(currentAction)]:
            if relation not in self.processed:
                self.processed.append(relation)
                self.map.append((relation, currentDepth))
                try:
                    self.depthTracker[currentDepth] += 1
                except KeyError:
                    self.depthTracker[currentDepth] = 1
                self.nextRow(self.table[relation], currentDepth + 1)
            self.needsLine.append((self.actions.index(currentAction[0]), relation))

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        # Can be used to test drawing lines between specific actions. Keep for now.
        #ifrom = self.mapToTree(self.needsLine[0][0])
        #ito = self.mapToTree(self.needsLine[0][1])
        #qp.drawLine(ifrom.x(), ifrom.y(), ito.x(), ito.y())
        #alternate = True
        if self.op.lastButtonPressed is not None:
            pen.setColor(Qt.yellow)
            qp.setPen(pen)
            qp.drawRect(self.mapToTree(self.op.lastButtonPressed).x(), self.mapToTree(self.op.lastButtonPressed).y(), self.buttons[self.op.lastButtonPressed].rect().width(), self.buttons[self.op.lastButtonPressed].rect().height())
            pen.setColor(Qt.black)
            qp.setPen(pen)
        for line in self.needsLine:
            width0 = self.buttons[line[0]].rect().width()
            height0 = self.buttons[line[0]].rect().height()
            width1 = self.buttons[line[1]].rect().width()
            height1 = self.buttons[line[1]].rect().height()
            ifrom = self.mapToTree(line[0])
            ito = self.mapToTree(line[1])
            if len(self.table[line[0]]) == 1 or len(self.table[line[1]]) == 1:
                pen.setColor(Qt.green)
                qp.setPen(pen)
                if len(self.table[line[0]]) == 1:
                    if line[0] in self.op.subtree or line[0] == self.op.lastButtonPressed:
                        qp.drawRect(ifrom.x() - 2, ifrom.y() - 2, width0 + 4, height0 + 4)
                    else:
                        qp.drawRect(ifrom.x(), ifrom.y(), width0, height0)
                if len(self.table[line[1]]) == 1:
                    if line[1] in self.op.subtree:
                        qp.drawRect(ito.x()-2, ito.y()-2, width1+4, height1+4)
                    else:
                        qp.drawRect(ito.x(), ito.y(), width1, height1)
                pen.setColor(Qt.black)
                qp.setPen(pen)
            if line[0] in self.op.subtree or line[1] in self.op.subtree:
                pen.setColor(Qt.red)
                qp.setPen(pen)
                if line[0] in self.op.subtree and line[0] != self.op.lastButtonPressed:# and len(self.table[line[0]])>1:
                    qp.drawRect(ifrom.x(), ifrom.y(), width0, height0)
                if line[1] in self.op.subtree and line[1] != self.op.lastButtonPressed:# and len(self.table[line[1]])>1:
                    qp.drawRect(ito.x(), ito.y(), width1, height1)
            if self.op.needsRefresh:
                self.update()
                self.op.needsRefresh = False
            if self.mapped[line[0]] <= self.mapped[line[1]]:
                qp.drawLine(ifrom.x()+(width0/2), ifrom.y()+(height0/2), ito.x()+(width1/2), ito.y()+(height1/2))
            else:
                pen.setStyle(Qt.DashLine)
                qp.setPen(pen)
                qp.drawLine(ifrom.x()+(width0/2), ifrom.y()+(height0/2), ito.x()+(width1/2), ito.y()+(height1/2))
                #if alternate:
                #   qp.drawArc(QRectF(ito.x(), ito.y()+1, width0, ifrom.y()-ito.y()), 90*16, 180*16)
                #   alternate=False
                #else:
                #   qp.drawArc(QRectF(ito.x(), ito.y()+1, width0, ifrom.y()-ito.y()), 270*16, 180*16)
                #   alternate=True
                pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.black)
            qp.setPen(pen)



    def mapToTree(self, index):
        p = QPoint(self.buttons[index].rect().left(), self.buttons[index].rect().top())
        return self.buttons[index].mapTo(self, p)

"""TESTS
app = QApplication(sys.argv)
psl = PrettySL(None, None, SocialLink("Void").startLink(1, 0))
psl.show()
sys.exit(app.exec_())
"""