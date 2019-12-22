"""
Mainframe of the application, responsible for maintaining the visibility of the application as well switching
between GUIs based on the user's input in the app.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QWidget, QGridLayout, QLayout, QDesktopWidget
from gui.qtop import OP


class MainFrame(QWidget):
    """
    Omnipresent background widget that fills itself with whatever GUI is requested.

    :param QObject parent: the QApplication used to launch the program.
    """
    def __init__(self, parent):
        self.parent = parent
        super().__init__()
        self.state = "Opening Screen"
        self.setAutoFillBackground(True)
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)
        self.currentWidget = OP(self)
        self.setPalette(self.currentWidget.palette())
        self.layout.addWidget(self.currentWidget, 0, 0, 2, 2)
        self.layout.setSizeConstraint(QLayout.SetFixedSize)
        self.currentWidget.show()
        self.show()
        self.raise_()

    def changeState(self, newWidgetState):
        """
        Change the displayed widget that the MainFrame container is showing to a new view.

        :param QWidget newWidgetState: new QWidget view to switch to
        """
        self.setPalette(newWidgetState.palette())
        self.currentWidget.hide()
        self.currentWidget.destroy()
        self.layout.addWidget(newWidgetState, 0, 0)
        self.currentWidget = newWidgetState
        newWidgetState.show()
        self.center()

    def center(self):
        """
        Force the window to center itself.
        (Does cause stupid things on multi-screen setups sometimes though.)
        """
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
