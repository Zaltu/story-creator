# --coding:utf-8--
import sys
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
from libs import json_reader
from qtmainframe import MainFrame

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
m = MainFrame(app)
sys.exit(app.exec_())
