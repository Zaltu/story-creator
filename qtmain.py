# --coding:utf-8--
import sys
from PySide.QtGui import QApplication, QIcon
from libs import json_reader
from qtmainframe import MainFrame

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
m = MainFrame(app)
sys.exit(app.exec_())
