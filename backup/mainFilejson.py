
import json
import sys

from PyQt5.QtWidgets import *

import startvpt
from gui import mainMenu


class mainMenuUI(QMainWindow, mainMenu.Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dailyWin = []
        self.counter = 0
        self.resizeTable()
        self.saveBtn.clicked.connect(self.SaveAccount)
        self.startBtn.clicked.connect(self.startBtnClicked)
        self.addBtn.clicked.connect(self.addRow)
        self.delBtn.clicked.connect(self.removeRow)

    def resizeTable(self):
        x = self.tableWidget.horizontalHeader()
        x.setSectionResizeMode(1, QHeaderView.Stretch)


    def addAccount(self, rowPos, title, link):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(rowPos, 0, QTableWidgetItem(title))
        self.tableWidget.setItem(rowPos, 1, QTableWidgetItem(link))


    def SaveAccount(self):
        data = []
        link = None
        title = None
        rowCount = self.tableWidget.rowCount()
        for row in range(rowCount):
            if(self.tableWidget.item(row,1) == ''):
                link = ''

            else:
                link = self.tableWidget.item(row, 1).text()
            if(self.tableWidget.item(row,0) == ''):
                title = ''
            else:
                title = self.tableWidget.item(row, 0).text()
            data.append(
                {
                    'title': title.strip(),
                    'link': link.strip()
                }
            )
        with open('../account/account.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        self.tableWidget.setRowCount(0)
        self.populateData()
        pass

    def populateData(self):
        parsed_account = json.load(open('../account/account.json', 'r'))
        a = len(parsed_account)

        for row in range(a):
            self.addAccount(row, parsed_account[row]['title'], parsed_account[row]['link'])
            pass
        pass

    def startBtnClicked(self):
        selected = self.tableWidget.selectionModel().selectedRows()
        for row in selected:
            title = self.tableWidget.item(row.row(), 0).text()
            link = self.tableWidget.item(row.row(), 1).text()
            startvpt.startGame(title, link)
        pass

    def addRow(self):
        rowCount = self.tableWidget.rowCount()
        self.addAccount(rowCount,'','')
        pass

    def removeRow(self):
        selected = self.tableWidget.selectionModel().selectedRows()
        for row in selected:
            self.tableWidget.removeRow(row.row())
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = mainMenuUI()
    mainMenu.populateData()
    mainMenu.show()
    sys.exit(app.exec_())
