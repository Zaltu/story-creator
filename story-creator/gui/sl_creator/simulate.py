"""
Helper module to simulate running a social link.
"""
#pylint: disable=no-name-in-module,cell-var-from-loop
from PySide2.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PySide2.QtCore import Qt
from libs.action import Info, Speak, Camera, Movement


class Simulation(QWidget):
    """
    Social Link simulation view.

    :param SocialLink link: The social link object
    :param str arcana: the link's arcana
    :param int level: the level of link to simulate
    :param int angle: the andle of link to simulate
    """
    def __init__(self, link, arcana, level, angle):
        QWidget.__init__(self)
        self.fullLink = link
        self.link = self.fullLink.items
        self.arcana = arcana
        self.level = level
        self.angle = angle

        # View initializers
        self.responses = None
        self.next = None
        self.label = None
        self.currentIndex = None

        self.start()

    def start(self):
        """
        Being the simulation. Automatically connects itself to the next element sequencially.
        """
        self.setWindowTitle(
            self.arcana + " Social Link Level: " + str(self.level) + " Angle: " + str(self.angle)
        )

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        #Causes UI to constantly resize...
        #grid.setSizeConstraint(QLayout.SetFixedSize)
        self.label = None
        self.next = None
        self.responses = []
        self.currentIndex = 0

        self.action()

        quitbutt = QPushButton(self, text="Quit")
        quitbutt.clicked.connect(self.shutdown)
        self.grid.addWidget(quitbutt, 1000, 0)

        self.setWindowModality(Qt.ApplicationModal)
        self.show()

    def shutdown(self):
        """
        Quit the simulation.
        Since it's modal, no need to revert to parent widget.
        """
        self.close()

    def action(self):
        """
        Handle the prep and display of a single node in the social link graph.
        Handles connecting the progression buttons to the correct signal.
        """
        print(
            "Dipslaying Action at index " +
            str(self.currentIndex) +
            " " +
            self.fullLink.getOneID(self.fullLink.getItem(self.currentIndex))[:20]
        )
        for response in self.responses:
            response.close()
            response.clicked.disconnect()
        self.responses = []
        if self.next:
            self.next.close()
            self.next.clicked.disconnect()
        self.next = None
        if not self.label:
            self.label = QLabel(self)

        if isinstance(self.link[self.currentIndex][0], Info):
            actionText = self.link[self.currentIndex][0].text
        elif isinstance(self.link[self.currentIndex][0], Speak):
            actionText = self.link[self.currentIndex][0].speaker+":\n\n"+self.link[self.currentIndex][0].text
        elif isinstance(self.link[self.currentIndex][0], Camera):
            actionText = "Camera is being changed in/to " + self.link[self.currentIndex][0].place
        elif isinstance(self.link[self.currentIndex][0], Movement):
            actionText = self.link[self.currentIndex][0].subject + \
                         " is performing a " + \
                         self.link[self.currentIndex][0].animation + \
                         " action"
        else:
            actionText = "ERROR READING SOCIAL LINK\nACTION INDEX: " + self.currentIndex

        self.label.setText(actionText)
        self.grid.addWidget(self.label, 0, 0)

        print("Currently reading: " + str(self.link[self.currentIndex]))
        if len(self.link[self.currentIndex]) == 2:
            self.next = QPushButton(self, text="Next")
            self.grid.addWidget(self.next, 1, 0)
            self.next.clicked.connect(self.action)
            self.currentIndex = self.link[self.currentIndex][1]
        elif len(self.link[self.currentIndex]) > 2:
            for relation in self.link[self.currentIndex][1:len(self.link[self.currentIndex])]:
                print("Linked to multiple relations: " + str(relation))
                self.responses.append(QPushButton(
                    self,
                    text=self.fullLink.getOneID(self.fullLink.getItem(relation))
                ))
                self.grid.addWidget(self.responses[-1], len(self.responses), 0)
                if len(self.link[relation]) == 2:
                    self.responses[-1].clicked.connect(
                        lambda _=False, nextIndex=self.link[relation][1]: self.chosenOne(nextIndex)
                    )
                else:
                    self.responses[-1].clicked.connect(
                        lambda _=False, nextIndex=relation: self.chosenOne(nextIndex)
                    )
        elif len(self.link[self.currentIndex]) == 1:
            print("End of link, user forced to quit")
        else:
            print("ERROR READING SOCIAL LINK\nACTION INDEX: " + str(self.currentIndex))

    def chosenOne(self, index):
        """
        Continue the action with the selected index during a choice.

        :param int index: selected index
        """
        print(index)
        self.currentIndex = index
        self.action()

#TESTS
#app = QApplication(sys.argv)
#fullLink = SocialLink('Void')
#link = fullLink.startLink(1, 0)
#sim = Simulation(link, 'Void', 1, 0)
#sys.exit(app.exec_())
