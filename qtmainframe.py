from PySide2.QtWidgets import QWidget, QGridLayout, QLayout, QDesktopWidget
from gui.qtop import OP


class MainFrame(QWidget):

    def __init__(self, parent):
        self.parent = parent
        QWidget.__init__(self)
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
        self.setPalette(newWidgetState.palette())
        self.currentWidget.hide()
        self.layout.addWidget(newWidgetState, 0, 0)
        self.currentWidget = newWidgetState
        newWidgetState.show()
        self.center()

    def center(self):
        # Center window
        qr = self.frameGeometry()
        qr.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(qr.topLeft())
