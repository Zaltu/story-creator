"""
Module for the pretty(est) graph view of a social link cutscene and it's interdependencies.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout
from PySide2.QtCore import Qt
from NodeGraphQt import (NodeGraph, setup_context_menu)
from gui.popup import popup
from gui.sl_creator.node_graph.frames import InfoNode, SpeakNode, CameraNode, MoveNode
from libs.action import Info, Speak, Camera, Movement

class PrettySL(QWidget):
    """
    This is the base widget to contain the graph view of the cutscene.

    :param MainFrame mainframe: application mainframe
    :param QWidget op: parent widget
    """
    def __init__(self, mainframe, op):
        QWidget.__init__(self)
        self.mainframe = mainframe
        self.op = op
        self.graph = self.op.link
        self.table = self.op.link.items
        self.lastButtonPressed = None
        self.needsRefresh = False
        self.tree = None
        self.subtree = []
        self.delete = None

        # View initializations...
        self.lab = None
        self.idLabel = None
        self.edit = None
        self.lkst = None
        self.rels = None

        self.initData()
        self.initUI()


    def initData(self):
        """
        Initialize the data to be used.
        """
        self.lab = None
        self.actionIDs = self.graph.getIDs()
        self.actionObjs = []
        for act in self.table:
            self.actionObjs.append(act[0])

    def initUI(self):
        """
        Initializes the GUI.
        Does lots of stuff.
        """
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.tree = TreeWidget(self, self.actionObjs, self.actionIDs, self.table)
        self.grid.addWidget(self.tree.widget, 0, 0, 10, 3)

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def trackIndex(self, index):
        """
        Update the Tree and info views with a new index.

        :param int index: the new index
        """
        self.needsRefresh = True
        self.lastButtonPressed = index
        self.subtree = self.graph.subTree(index)
        print(self.subtree)
        self.initInfoUI(index)

    def deleteSubtree(self):
        """
        Delete the subtree of the current selected index.
        """
        if not popup("Are you certain you want to delete this item and it's subtree?\n(Everything in red and"
                     " yellow will be deleted)", "Warning"):
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

    def enter(self, index):
        """
        Leave the graph view and edit a node.

        :param int index: index of node to edit
        """
        load = self.graph.getItem(index)
        self.close()
        self.op.view.setText("Graphic View")
        self.op.view.clicked.disconnect()
        self.op.view.clicked.connect(lambda: self.op.viewF(True))
        self.op.listview.changeFrame(load, index)


class TreeWidget(NodeGraph):
    """
    The actual graph view of the cutscene.
    Nodes are represented by QPushButtons, and lines are drawn between them to symbolize relationships.

    This is all very dumb.

    :param QWidget op: parent widget
    :param list actions: list of nodes to display
    :param list ids: list of ids of the action in the actions list, in the same order
    :param list table: table of both the actions and the ids
    """
    def __init__(self, op, actions, ids, table):
        super().__init__()
        self.actions = actions
        self.ids = ids
        self.table = table
        self.op = op
        self.currentDepth = 0

        self.node_type_names = {
            Info: "personax.InfoNode",
            Speak: "personax.SpeakNode",
            Camera: "personax.CameraNode",
            Movement: "personax.MoveNode"
        }
        try:
            setup_context_menu(self)
            # registered nodes.
            reg_nodes = [
                InfoNode,
                SpeakNode,
                CameraNode,
                MoveNode
            ]
            for node in reg_nodes:
                self.register_node(node)
        except:  #pylint: disable=bare-except
            # Despite the function being tied explicitely to this object instance, the IDs in NodeGraphQt of
            # each registered node are not actually related to the object at all but act similar to class
            # objects due to a poorly implemented factory model.
            pass

        self.initUI()


    def initUI(self):
        """
        Initializes the GUI.
        Does lots of stuff.
        """
        self.processed = [0]
        self.map = [(0, 0)]
        self.depthTracker = {}
        self.heightTracker = {}

        self.nextRow(self.table[0], 1)

        self.nodes = {}


        for element in self.map:
            elementsPerDepth = self.depthTracker.get(element[1], 1)
            hpos = 200 * self.heightTracker.get(element[1], 1)
            hpos -= (200 * elementsPerDepth)/2
            if elementsPerDepth != 1:
                self.heightTracker[element[1]] += 1

            self.nodes[element[0]] = self.create_node(
                self.node_type_names[type(self.actions[element[0]])],
                self.actions[element[0]],
                name=str(element[0]),
                pos=[400*element[1], hpos]  # TODO
            )
        for node in self.nodes:
            for connection in self.table[node][1:len(self.table[node])]:
                self.nodes[node].set_output(0, self.nodes[connection].input(0))


    def nextRow(self, currentAction, currentDepth):
        """
        Parse the next row's worth of buttons recursively.
        Basically assumes that all rows should be sequential relative to the first caller's row.
        OK in most situations, but can cause problems.

        :param list currentAction: current entry in self.tables
        :param int currentDepth: the current row number
        """
        for relation in currentAction[1:len(currentAction)]:
            if relation not in self.processed:
                self.processed.append(relation)
                self.map.append((relation, currentDepth))
                try:
                    self.depthTracker[currentDepth] += 1
                except KeyError:
                    self.depthTracker[currentDepth] = 1
                self.heightTracker[currentDepth] = 1
                self.nextRow(self.table[relation], currentDepth + 1)
