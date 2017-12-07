#--coding:utf-8--
import sys
from qtheader import *
from qtmainframe import MainFrame

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(json_reader.buildPath('icon.gif')))
m = MainFrame(app)
sys.exit(app.exec_())
