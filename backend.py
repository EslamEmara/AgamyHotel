import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QSizePolicy,QDialog,QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from os import path
import sys
from datetime import datetime

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "assets/layout.ui")) #used to make any changed in .ui code work on here


class MainApp2(QMainWindow , FORM_CLASS):
    def __init__(self, msg, parent=None):
        super(MainApp2 , self).__init__(parent)
        QMainWindow.__init__(self)

        self.appList = []

        self.setupUi(self)          #sets up the ui
        self.Handel_UI()        #calling function to work when the class is initialized
        self.connectObjects()
        self.ParseDataFile()
        self.DisplayDataList()


    def Handel_UI(self):    #function that handels the ui of the gui
        now = datetime.now()
        self.setWindowTitle('El-Agamy Hotel')    #sets window name
        self.setWindowIcon(QtGui.QIcon(path.join(path.dirname(__file__), 'assets/logo.png')))
        self.dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d"))), QtCore.QTime(0, 0, 0)))
        self.listWidget.itemDoubleClicked.connect(self.click)
        self.tabWidget.setCurrentIndex(0)
        #self.showFullScreen()




    def connectObjects(self):
        self.lineEdit.textChanged.connect(self.searchBarAction)
        self.submitButton.clicked.connect(self.submitClick)


    def ParseDataFile(self):
        f = open((path.join(path.dirname(__file__), "assets/data.txt")), "r")
        self.appList =[]
        for x in f:
            info = x.split("\n")
            if(info[0] == ''):
                continue
            info = info[0].split('-')
            if (info[2] == ''):
                info[2] = 'N/A'
            self.appList.append(info)
        f.close()

    def DisplayDataList(self):
        self.listWidget.clear()
        for app in self.appList:
            if(app[1] == '1'):
                item = QListWidgetItem(app[0] + '\t\t\t\t Not Available \t\t\t\t' + app[2] )
                item.setBackground(Qt.red)
            else:
                item = QListWidgetItem(app[0] + '\t\t\t\t Available \t\t\t\t\t' + app[2] )

            self.listWidget.addItem(item)

    def saveDatatoFile(self):
        f = open((path.join(path.dirname(__file__), "assets/data.txt")), "w")
        for app in self.appList:
            print(app)
            f.write(app[0]+'-'+app[1]+'-'+app[2]+'\n')
        f.close()

    def submitClick(self):
        value = self.dateEdit.date()
        print(value.toPyDate().strftime("%d/%m/%Y"))
        print(self.AppartmentnumberIn.text())
        for app in self.appList:
              if app[0] == self.AppartmentnumberIn.text():
                  if app[1] == '1':
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowTitle("Reservation Error")
                    msg.setText("The Appartment is not available in the selected time");
                    msg.exec();
                  else:
                      app[1] = '1'
                      app[2] = value.toPyDate().strftime("%d/%m/%Y")

                      msg = QMessageBox()
                      msg.setIcon(QMessageBox.Information)
                      msg.setWindowTitle("Reservation Success")
                      msg.setText("The Reservation has been added");
                      msg.exec();


        self.saveDatatoFile()
        self.ParseDataFile()
        self.DisplayDataList()


    def searchBarAction(self):
        items = self.listWidget.findItems(self.lineEdit.text(),Qt.MatchStartsWith)
        for i in range(self.listWidget.count()):
             if (self.listWidget.item(i) not in items):
                 self.listWidget.item(i).setHidden(True)
             else:
                 self.listWidget.item(i).setHidden(False)

    def click(self,item):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Appartment info")

        for app in self.appList:
            if int(app[0]) == int(item.text().split("\t\t\t")[0]):
                if app[1] == '1':
                    dlg.setText("Appartment: " + app[0] + "\nState: " + 'Reserved'+
                    "\nDate of vacancy: " + app[2] + "\n\n\nDo you want to clear the Appartment?")
                    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    dlg.setIcon(QMessageBox.Question)
                    button = dlg.exec()
                    
                    if button == QMessageBox.Yes:
                        app[1] = '0'
                        app[2] = ''
                        self.saveDatatoFile()
                        self.ParseDataFile()
                        self.DisplayDataList()

                    break
                else:
                    dlg.setText("Appartment: " + app[0] + "\nState: " + 'Available'+
                    "\nDate of vacancy: " + app[2] + "\n\n\nDo you want to Reserve the Appartment?")
                    dlg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                    dlg.setIcon(QMessageBox.Question)
                    button = dlg.exec()
                    
                    if button == QMessageBox.Yes:
                        self.tabWidget.setCurrentIndex(1)
                    break


if __name__ == "__main__":          #main loop
    app = QApplication(sys.argv)    #object of class QApplication
    window = MainApp2("")  #object of class MainApp2
    window.show()       #shows the window

    sys.exit(app.exec_())
