"""
Utility module to create a popup window asking for confirmation, warning the user of something, etc.
"""
#pylint: disable=no-name-in-module
from PySide2.QtWidgets import QMessageBox

def popup(message, mestype):
    """
    Pops up a popup window with a certain message.
    It forcefully grabs the focus of the QApplication that may be running, forcing the user to acknowledge it
    before continuing.

    Message types are:
    [Information, Warning, Critical, Question, Default]

    :param str message: Message to display
    :param str mestype: Message type

    :returns: Whether the user confirmed the message
    :rtype: bool
    """
    icon = {"Information":QMessageBox.Information, "Warning":QMessageBox.Warning,
            "Critical":QMessageBox.Critical, "Question":QMessageBox.Question,
            "Default":QMessageBox.NoIcon}

    box = QMessageBox(icon[mestype], mestype, message)
    if mestype in ["Warning", "Question"]:
        box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        box.setDefaultButton(QMessageBox.Yes)
        box.setEscapeButton(QMessageBox.Cancel)
    result = box.exec_()
    return result in [QMessageBox.Yes, QMessageBox.Ok]

#TESTS
#print popup("This is a test window", "Warning")
#print popup("This is another test window", "Critical")
