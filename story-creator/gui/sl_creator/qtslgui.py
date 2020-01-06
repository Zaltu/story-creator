"""
Module for all the cutscene editing views.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton

from gui.sl_creator.simulate import Simulation
from gui.sl_creator.node_graph.slnodegraph import NodeSL
from gui.sl_creator.slview import PrettySL
from gui.sl_creator.slinfo import LinkInfo
from gui.popup import popup
from libs.sls import SocialLink

class SLFrame(QWidget):
    """
    The main cutscene editing view. This widget is used to contain all other edit views.

    :param MainFrame mainframe: application mainframe
    :param QWidget op: parent widget
    :param str arcana: cutscene's social link arcana
    :param int level: cutscene's social link level
    :param int angle: cutscene's social link angle
    """
    def __init__(self, mainframe, op, arcana, level, angle):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.arcana = arcana
        self.level = level
        self.angle = angle
        self.linkstored = SocialLink(arcana)
        self.link = self.linkstored.startLink(level, angle)
        self.i = 0

        # View initializers...
        self.graphicview = None
        self.nodeview = None
        self.sim = None
        self.cc = None

        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        """
        self.mainframe.setWindowTitle("Social Link Creator")
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        simulate = QPushButton(self, text="Simulate")
        simulate.clicked.connect(self.simulate)
        self.grid.addWidget(simulate, 2, 0)

        self.view = QPushButton(self, text="Dependency View")
        self.view.clicked.connect(lambda: self.viewF(True))
        self.grid.addWidget(self.view, 2, 1)

        self.info = QPushButton(self, text="Info")
        self.info.clicked.connect(self.infoF)
        self.grid.addWidget(self.info, 2, 2)

        back = QPushButton(self, text="Back to Arcana selection")
        back.clicked.connect(self.back)
        self.grid.addWidget(back, 2, 3)

        self.viewF(False)  # Initialize in NodeSL view

    def back(self):
        """
        Return view to the parent widget.
        """
        self.mainframe.changeState(self.op)

    def simulate(self):
        """
        Simulate this cutscene.
        Pops open the simulation model, which is modal.
        """
        if len(self.link.getIDs()) == 0:
            popup("Nothing to simulate!", "Information")
            return
        self.sim = Simulation(self.link, self.arcana, self.level, self.angle)

    def infoF(self):
        """
        Switch to the social link general information edit view.
        """
        self.mainframe.changeState(LinkInfo(
            self.mainframe,
            self,
            self.linkstored,
            str(self.level),
            str(self.angle)
        ))

    def viewF(self, dep):
        """
        Toggle between the list and graph views of the social link.

        :param bool dep: whether the dependency view should be displayed
        """
        if dep:
            if len(self.link.getIDs()) == 0:
                popup("Nothing to show!", "Information")
                return
            self.graphicview = PrettySL(self.mainframe, self)
            self.nodeview.close()
            if self.cc:
                self.cc.close()
            self.view.setText("Graph View")
            self.grid.addWidget(self.graphicview, 0, 0, 1, 4)
            self.graphicview.show()
            self.view.clicked.disconnect()
            self.view.clicked.connect(lambda: self.viewF(False))
        else:
            if self.cc:
                self.cc.close()
            else:
                self.nodeview = NodeSL(self.mainframe, self)
            if self.graphicview:
                self.graphicview.close()
            self.view.setText("Dependency View")
            self.grid.addWidget(self.nodeview, 0, 0, 1, 4)
            self.nodeview.show()
            self.view.clicked.disconnect()
            self.view.clicked.connect(lambda: self.viewF(True))
        self.mainframe.center()

    def writeSave(self):
        """
        Save the current cutscene.
        """
        self.linkstored.setLink(self.link, self.level, self.angle)
        self.linkstored.save()
