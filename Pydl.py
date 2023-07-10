# TODO = Add path  download and multy processing

#Link = https://dl.subtitlestar.com/dlsub/friends-All-S09.zip

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QTimer, QDateTime, QThread
import sys, time
import urllib.request
from PyQt5.QtWidgets import *

status = {
    "compelete": "Compelete",
    "failed": "Failed",
    "downloading": "Downloading",
    "wait": "Waiting For Download"
}

tableColumn = {
    "Link": 0,
    "Start Time": 1,
    "Finish Time": 2,
    "Status": 3
}
statusDownload = False

class DownloadWindow(QWidget):
    url = ""
    def __init__(self):
        super().__init__()
        self.init_UI()
 
    def init_UI(self):
        
        self.progressBar = QProgressBar(self)
        self.progressBar.setGeometry(25, 25, 210, 30)
 
        self.setGeometry(300, 300, 250, 100)
        self.setWindowTitle("PyDl")
        self.show()

    def getUrl(self, url):
        self.url = url
        
    def Handle_Progress(self, blocknum, blocksize, totalsize):
        readed_data = blocknum * blocksize
        
        if totalsize > 0:
            download_percentage = int(readed_data * 100 / totalsize)
            self.progressBar.setValue(download_percentage)
            QtWidgets.QApplication.processEvents()

        if download_percentage == 100:
            self.messageDownload()

    def messageDownload(self):
        self.messageDownlaod = Ui_MainWindow()
        self.messageDownlaod.showMsgDownload("File: " + self.url + " Downloaded.")
        statusDownload = True


class Ui_MainWindow(object):

    counterRow = 0
    downloadComplete = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 750)

        icon = QtGui.QIcon('Pydl.png')
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Logo = QtWidgets.QLabel(self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(80, 350, 500, 500))
        self.Logo.setPixmap(QtGui.QPixmap("Pydl.png"))

        self.textEditForLable = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditForLable.setGeometry(QtCore.QRect(160, 10, 451, 30))
        self.textEditForLable.setObjectName("textEditForLable")

        self.LinkLabel = QtWidgets.QLabel(self.centralwidget)
        self.LinkLabel.setGeometry(QtCore.QRect(20, 10, 141, 30))
        self.LinkLabel.setObjectName("LinkLabel")

        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(500, 440, 110, 30))
        self.StartButton.setObjectName("StartButton")
        self.StartButton.clicked.connect(self.startDownload)

        self.CancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.CancelButton.setGeometry(QtCore.QRect(382, 440, 110, 30))
        self.CancelButton.setObjectName("CancelButton")
        self.CancelButton.clicked.connect(self.cancelDownload)

        self.AddButton = QtWidgets.QPushButton(self.centralwidget)
        self.AddButton.setGeometry(QtCore.QRect(140, 440, 110, 30))
        self.AddButton.setObjectName("AddButton")
        self.AddButton.clicked.connect(self.addLink)

        self.ExitButton = QtWidgets.QPushButton(MainWindow)
        self.ExitButton.setGeometry(QtCore.QRect(20, 440, 110, 30))
        self.ExitButton.setObjectName("ExitButton")
        self.ExitButton.clicked.connect(self.exitProgram)

        self.DeleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteButton.setGeometry(QtCore.QRect(260, 440, 110, 30))
        self.DeleteButton.setObjectName("DeleteButton")
        self.DeleteButton.clicked.connect(self.deleteLink)

        self.DateAndTime = QtWidgets.QLabel(self.centralwidget)
        self.DateAndTime.setGeometry(QtCore.QRect(240, 470, 200, 30))
        self.DateAndTime.setText("")
        self.DateAndTime.setObjectName("DateAndTime")

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 50, 590, 380))
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pydl"))
        self.LinkLabel.setText(_translate("MainWindow", "Copy Link Into The Box:"))
        self.StartButton.setText(_translate("MainWindow", "StartDownload"))
        self.CancelButton.setText(_translate("MainWindow", "CancelDownload"))
        self.AddButton.setText(_translate("MainWindow", "Add Link"))
        self.ExitButton.setText(_translate("MainWindow", "Exit"))
        self.DeleteButton.setText(_translate("MainWindow", "Delete Link"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Link"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Start Time"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Finish Time"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))

    def addRow(self):
        self.tableWidget.insertRow(self.counterRow)
        self.rowValue()
        self.counterRow += 1

    def delRow(self):
        if self.counterRow > 0:
            self.tableWidget.removeRow(self.counterRow - 1)
            self.counterRow -= 1

    def rowValue(self):
        link = self.textEditForLable.toPlainText()
        self.tableWidget.setItem(self.counterRow, tableColumn["Link"], QtWidgets.QTableWidgetItem(link))
        if self.downloadComplete:
            timeFinish = self.timeTable()
            self.tableWidget.setItem(self.counterRow, tableColumn["Finish Time"],
                                     QtWidgets.QTableWidgetItem(timeFinish))
            self.tableWidget.setItem(self.counterRow, tableColumn["Status"],
                                     QtWidgets.QTableWidgetItem(status["compelete"]))
            self.downloadComplete = False
        else:
            timeStart = self.timeTable()
            self.tableWidget.setItem(self.counterRow, tableColumn["Start Time"], QtWidgets.QTableWidgetItem(timeStart))
            self.tableWidget.setItem(self.counterRow, tableColumn["Status"], QtWidgets.QTableWidgetItem(status["wait"]))

    def showTime(self):
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.DateAndTime.setText(timeDisplay)

    def timeTable(self):
        time = QDateTime.currentDateTime()
        timeStart = time.toString('hh:mm:ss')
        return timeStart

    def addLink(self):
        self.addRow()


    def deleteLink(self):
        self.delRow()

    def startDownload(self):
        try:
            url = self.tableWidget.item(self.counterRow - 1, tableColumn["Link"]).text()
            if url == "":
                self.showMsgDownload("Url is Empty !!!")
                self.tableWidget.setItem(self.counterRow - 1, tableColumn["Status"],
                                         QtWidgets.QTableWidgetItem(status["failed"]))
            else:
                try:
                    self.worker = WorkerThread()
                    self.worker.getItem(url)
                    self.worker.start()
                    while not statusDownload:
                        self.counterRow -= 1
                        self.downloadComplete = True
                        self.rowValue()
                        self.counterRow += 1

                except:
                    self.showMsgDownload("Link " + url + " Does Not Exist Or Your Net is Problem.")
                    self.tableWidget.setItem(self.counterRow - 1, tableColumn["Status"],
                                             QtWidgets.QTableWidgetItem(status["failed"]))
        except:
            self.showMsgDownload("Please Enter Link Into The Box.")

    def showMsgDownload(self, message):
        icon = QtGui.QIcon('Pydl.png')
        msg = QMessageBox()
        msg.setWindowIcon(icon)
        msg.setWindowTitle("Pydl")
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.Ok)
        e = msg.exec_()

    def cancelDownload(self):
        pass

    def exitProgram(self):
        exit(0)

class WorkerThread(QThread):
    url = ""
    
    def getItem(self, url):
        self.url = url

    def run(self):
        self.anotherWindow = DownloadWindow()
        save_loc = "/home/amir/Programming/Python/PyDl-main/friends-All-S09.zip"
        self.anotherWindow.getUrl(self.url)
        urllib.request.urlretrieve(self.url,save_loc, self.anotherWindow.Handle_Progress)

            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
