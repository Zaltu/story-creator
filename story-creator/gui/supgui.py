"""
This module holds the Help/Support view.
"""
#pylint: disable=no-name-in-module
from shutil import copytree, copy
import os
from email.mime.multipart import MIMEMultipart, MIMEBase
from email.mime.text import MIMEText
import smtplib
from glob import glob

from PySide2.QtWidgets import (QWidget, QPushButton, QLabel, QGridLayout, QTextEdit, QLineEdit, QCheckBox,
                               QFileDialog)
from PySide2.QtCore import Qt
from gui.popup import popup
from libs import json_reader


class SupportUI(QWidget):
    """
    Top-level help/support view.

    :param MainFrame mainframe: the mainframe of the application
    :param QWidget op: the parent widget
    """
    def __init__(self, mainframe, op):
        super().__init__()
        self.mainframe = mainframe
        self.op = op
        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        Does a lot of stuff.
        """
        self.mainframe.setWindowTitle("Contact/Support")

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        importB = QPushButton(self, text="Import")
        importB.clicked.connect(self.importF)
        self.grid.addWidget(importB, 0, 0)

        exportB = QPushButton(self, text="Export")
        exportB.clicked.connect(self.export)
        self.grid.addWidget(exportB, 0, 1)

        self.contact = QPushButton(self, text="Contact")
        self.contact.clicked.connect(self.contactF)
        self.grid.addWidget(self.contact, 0, 2)

        self.text = QLabel(self, text="Hello and thank you for using the Persona X Story Creator.\n\nTo "
                                      "import data from other versions of the Story Creator, click "
                                      "\"Import\".\n\nTo export your data to a seperate directory, (to "
                                      "prepare for a version change), click \"Export\".\n\nTo send your data"
                                      " to the dev team or to report a bug with the program, click "
                                      "\"Contact\"")
        self.text.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(self.text, 1, 0, 1, 3)

        self.back = QPushButton(self, text="Back")
        self.back.clicked.connect(self.backF)
        self.grid.addWidget(self.back, 2, 1)

    def importF(self):
        """
        Import a file or set of files from disk into Story-Creator controlled directories.

        :raises AssertionError: with an object attempting to being loaded if the object cannot be loaded as a
                 Social Link, Character or Persona.
        """
        fileBrowser = QFileDialog()
        fileBrowser.setFileMode(QFileDialog.Directory)
        fileBrowser.setViewMode(QFileDialog.Detail)
        fileBrowser.setOption(QFileDialog.ShowDirsOnly, True)
        if fileBrowser.exec_():
            paths = fileBrowser.selectedFiles()
        else:
            print("Cancelled")
            return
        print("Copying data from "+str(paths[0]))
        files = os.listdir(str(paths[0]))
        print(files)
        for file in files:
            if file.endswith(".json"):
                print("Copying valid file " + file)
                if "_link" in file:
                    if self.checkOverwrite(file):
                        copy(os.path.join(str(paths[0]), file), json_reader.buildPath("data"))
                else:
                    try:  # Ugly AF
                        # TODO omgf this is more than ugly AF
                        characterL = json_reader.readOne(file[:len(file)-5], 'chars')
                        assert "name" in characterL and "important" in characterL
                        if self.checkOverwrite(file, 'chars'):
                            copy(os.path.join(str(paths[0]), file), json_reader.buildPath("data/chars"))
                    except AssertionError:
                        print("Not a Character")
                        try:
                            personaL = json_reader.readOne(file[:len(file)-5], 'pers')
                            assert "name" in personaL and "arcana" in personaL
                            if self.checkOverwrite(file, 'pers'):
                                copy(os.path.join(str(paths[0]), file), json_reader.buildPath("data/pers"))
                        except AssertionError:
                            print("Not a Persona")
                            raise AssertionError(personaL)
        print("Successfully copied files")
        popup("Files imported successfully!", "Information")


    def checkOverwrite(self, filepath, ctype=''):
        """
        Confirm with user if file should be overwritten.

        :param str filepath: path to file that could be overwritten
        :param str ctype: chars or pers if the file represents either type
        """
        if ctype:
            ctype = ctype+"/"
        if os.path.exists(os.path.join(json_reader.buildPath("data"), filepath)):
            if popup("File " + filepath[:len(filepath)-5] + " already exists. Overwrite?", "Warning"):
                os.remove(json_reader.buildPath("data/%s%s"%(ctype, filepath)))


    def export(self):
        """
        Export the story-creator data files to a user-selected locaion.
        """
        fileBrowser = QFileDialog()
        fileBrowser.setFileMode(QFileDialog.Directory)
        fileBrowser.setViewMode(QFileDialog.Detail)
        fileBrowser.setOption(QFileDialog.ShowDirsOnly, True)
        if fileBrowser.exec_():
            paths = fileBrowser.selectedFiles()
        else:
            print("Cancelled")
            return
        print("Copying data to "+str(paths[0])+"/exportdata")
        try:
            copytree(json_reader.buildPath("data"), str(paths[0])+"/exportdata")
        except OSError as e:
            print(e)
            popup("Error in copying files. There is a file in the selected directory that has the same name "
                  "as a Story Creator file.\n\nFiles are copied to "+str(paths[0])+"/exportdata"+". Please "
                  "ensure this directory does not already exist.", "Critical")
            return
        print("Successfully copied files")
        popup("Files exported successfully!", "Information")

    def contactF(self):
        """
        Bring up the email sending frame instead of the fluff text currently being displayed.
        """
        self.contact.clicked.disconnect()
        self.text.close()
        EmailFrame(self)

    def backF(self):
        """
        The user is done here. Return the view back to whatever brought us to the support page (the OP).
        """
        self.mainframe.changeState(self.op)


class EmailFrame(QWidget):
    """
    EmailFrame is the view in which the user can send a message to me via SMTP.
    Builds itself directly into it's parent widget.

    :param QWidget op: parent widget
    """
    def __init__(self, op):
        QWidget.__init__(self)
        self.op = op
        self.initUI()

    def initUI(self):
        """
        Initializes the GUI.
        Does a lot of stuff.
        """
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.op.grid.addWidget(self, 1, 0, 1, 3)

        subL = QLabel(self, text="Subject:")
        subL.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(subL, 0, 0)

        self.subject = QLineEdit(self)
        self.subject.setFixedSize(150, 20)
        self.grid.addWidget(self.subject, 0, 1)

        bodL = QLabel(self, text="")
        bodL.setAlignment(Qt.AlignHCenter)

        self.body = QTextEdit(self)
        self.body.setFixedSize(400, 150)
        self.grid.addWidget(self.body, 1, 1, 1, 3)

        sem = QLabel(self, text="Your email:")
        sem.setAlignment(Qt.AlignHCenter)
        self.grid.addWidget(sem, 2, 0)

        self.semT = QLineEdit(self)
        self.semT.setFixedSize(150, 20)
        self.grid.addWidget(self.semT, 2, 1)

        send = QPushButton(self, text="Send")
        send.clicked.connect(self.send)
        self.grid.addWidget(send, 2, 2)

        self.addFiles = QCheckBox(self, text="Send submission")
        self.addFiles.setToolTip(
            "Check this box to send all Character, Persona and Social Link data along with your message"
        )
        self.grid.addWidget(self.addFiles, 0, 2)

        self.op.back.clicked.disconnect()
        self.op.back.clicked.connect(self.back)

    def send(self):
        """
        Send entered text as email to me via SMTP.
        """
        if str(self.body.toPlainText()) == "" or \
           str(self.body.toPlainText()).isspace() or \
           str(self.subject.text()) == "" or \
           str(self.subject.text()).isspace():
            popup("Please enter a message and subject.", "Critical")
            return
        msg = MIMEMultipart()
        body = MIMEText(str(self.body.toPlainText() + "\n\nSent by " + self.semT.text()))
        msg.attach(body)
        msg['From'] = str(self.semT.text())
        msg['To'] = "swwouf@hotmail.com"
        msg['Subject'] = str(self.subject.text())
        if self.addFiles.isChecked():
            print("Adding files")
            fileNames = glob(json_reader.buildPath("data/*.json")) + \
                        glob(json_reader.buildPath("data/pers/*.json")) + \
                        glob(json_reader.buildPath("data/chars/*.json"))
            print(fileNames)
            for file in fileNames:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(file, "rb").read())
                part.add_header('Content-Disposition', 'attachment; filename="%s"' % file[file.rfind("/"):])
                msg.attach(part)

        serv = smtplib.SMTP("smtp.live.com", 587)
        serv.set_debuglevel(1)
        serv.ehlo()
        serv.starttls()
        serv.ehlo()
        serv.login("personaxdevteam@hotmail.com", 'PersonaX')
        try:
            serv.sendmail(msg['From'], msg['To'], msg.as_string())
            print("Message sent successfully")
            popup("Email was sent! Thank you!", "Information")
            serv.quit()
            return
        except smtplib.SMTPSenderRefused:
            popup("You must provide your email address so that we may contact you if needed.\n\nYour email "
                  "address will not be shared with any third parties.", "Critical")
            serv.quit()
            return
        except Exception as e:  #pylint: disable=broad-except
            print(e)
            popup("Email failed to send, but not sure why...", "Critical")


    def back(self):
        """
        Hide this view and return the parent widget to it's original state.
        """
        self.close()
        self.op.text.show()
        self.op.back.clicked.disconnect()
        self.op.back.clicked.connect(self.op.backF)
        self.op.contact.clicked.connect(self.op.contactF)
