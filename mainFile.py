import sys
from dataclasses import dataclass
import openpyxl
from PyQt5.QtWidgets import *
from gui import mainMenu
from mapData import *
import startvpt
from openpyxl import Workbook
from PyQt5.QtCore import *
@dataclass
class account:
    title: str
    link: str
    group: str

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
        self.accounts = []
        self.groups = []
        self.listWidget.itemClicked.connect(self.listItemClicked)
        self.tableWidget.setSortingEnabled(False)
        self.populateData()

    def populateData(self):
        self.accounts.clear()
        self.groups.clear()
        self.groups=['All']
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.listWidget.clear()
        workbookData = openpyxl.load_workbook(filename='./account/link_account.xlsx')
        sheet = workbookData.active
        for row in sheet.iter_rows(min_row=2,values_only=True):

            if (row[title] != None):
                t = row[title].strip()
            else:
                t=''
            if (row[link] != None):
                l = row[link].strip()
            else:
                l=''
            if (row[group] != None):
                g = row[group].strip()
            else:
                g=''
            acc = account(title=t.strip(),
                              link=l.strip(),
                              group=g.strip())
            self.accounts.append(acc)
        index = 0
        for acc in self.accounts:
            self.groups.append(acc.group)
            self.addAccountToTable(index, acc.title, acc.link, acc.group)
            index = index + 1

        self.groups = list(dict.fromkeys(self.groups))
        for item in self.groups:
            if(item != ''):
                self.listWidget.addItem(item)
        self.listWidget.addItem('No Group')
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row,True)
        self.listWidget.setCurrentRow(0)
        self.showData()

    def listItemClicked(self):
        self.showData()
    def showData(self):
        groupIndex = self.listWidget.selectedItems()
        groupText = groupIndex[0].text()
        for row in range(self.tableWidget.rowCount()):
            hidden = True
            if groupText == 'All' or groupText == self.tableWidget.item(row,2).text():
                hidden = False
            if groupText == 'No Group' and self.tableWidget.item(row,2).text()=='':
                hidden=False
            self.tableWidget.setRowHidden(row,hidden)
        pass


    def resizeTable(self):
        x = self.tableWidget.horizontalHeader()
        x.setSectionResizeMode(1, QHeaderView.Stretch)



    def addAccountToTable(self, rowPos, title, link, group):
        rowCount = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowCount)
        self.tableWidget.setItem(rowPos, 0, QTableWidgetItem(title))
        self.tableWidget.setItem(rowPos, 1, QTableWidgetItem(link))
        self.tableWidget.setItem(rowPos,2,QTableWidgetItem(group))

    def SaveAccount(self):
        self.accounts.clear()
        for row in range(self.tableWidget.rowCount()):

            t = self.tableWidget.item(row,0).text()
            l = self.tableWidget.item(row,1).text()
            g= self.tableWidget.item(row,2).text()
            acc = account(title=t,link=l,group=g)
            self.accounts.append(acc)

        toSave = Workbook()
        sheet = toSave.active
        index = 2
        sheet['A1'] = 'title'
        sheet['B1']= 'link'
        sheet['C1']= 'group'
        sheet.column_dimensions['A'].width = 20
        sheet.column_dimensions['B'].width = 170
        sheet.column_dimensions['C'].width = 20
        for data in self.accounts:
            if(data.title != '' or data.link != '' or data.group != ''):
                sheet.cell(row=index,column=1).value = data.title.strip()
                sheet.cell(row=index,column=2).value = data.link.strip()
                sheet.cell(row=index,column=3).value = data.group.strip()
            index= index+1
        sheet.auto_filter.ref = sheet.dimensions
        toSave.save('./account/link_account.xlsx')
        self.populateData()
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
        self.addAccountToTable(rowCount, '', '','')
        self.tableWidget.selectRow(len(self.accounts))
        pass

    def removeRow(self):

        indexes = [QPersistentModelIndex(index) for index in self.tableWidget.selectionModel().selectedRows()]
        for index in indexes:
            self.tableWidget.removeRow(index.row())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = mainMenuUI()
    mainMenu.show()
    sys.exit(app.exec_())
