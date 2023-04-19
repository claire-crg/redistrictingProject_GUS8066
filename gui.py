import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt

import sys
import os

user_input = []
test_list = []

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pathChooser = QPushButton(text='Choose path', parent=self)
        self.selectionLabel = QLabel(text="No selection yet", parent=self)
        self.checkBoxPolsbyPopper = QCheckBox(text="Polsby-Popper", parent=self)
        self.checkBoxSchwartzberg = QCheckBox(text="Schwartzberg", parent=self)
        self.checkBoxConvexHullRatio = QCheckBox(text="Convex Hull Ratio", parent=self)
        self.checkBoxReock = QCheckBox(text="Reock", parent=self)        
        self.checkBoxEfficiencyGap = QCheckBox(text="Efficiency Gap", parent=self)
        self.checkBoxMeanMedianDifference = QCheckBox(text="Mean-Median Difference", parent=self)
        self.checkBoxLopsidedMarginsTest = QCheckBox(text="Lopsided Margins Test", parent=self)
        self.launchButton = QPushButton(text='Launch', parent=self)
 
             
        layout = QVBoxLayout()
        layout.addWidget(self.pathChooser)
        layout.addWidget(self.checkBoxPolsbyPopper)
        layout.addWidget(self.checkBoxSchwartzberg)
        layout.addWidget(self.checkBoxConvexHullRatio)
        layout.addWidget(self.checkBoxReock)
        layout.addWidget(self.checkBoxEfficiencyGap)
        layout.addWidget(self.checkBoxMeanMedianDifference)
        layout.addWidget(self.checkBoxLopsidedMarginsTest)
        layout.addWidget(self.selectionLabel)
        layout.addWidget(self.launchButton)        
        
        self.setLayout(layout)
        self.pathChooser.clicked.connect(self.choose_path)
        self.checkBoxPolsbyPopper.stateChanged.connect(self.onStateChanged)
        self.checkBoxSchwartzberg.stateChanged.connect(self.onStateChanged)
        self.checkBoxConvexHullRatio.stateChanged.connect(self.onStateChanged)
        self.checkBoxReock.stateChanged.connect(self.onStateChanged)
        self.checkBoxEfficiencyGap.stateChanged.connect(self.onStateChanged)
        self.checkBoxMeanMedianDifference.stateChanged.connect(self.onStateChanged)
        self.checkBoxLopsidedMarginsTest.stateChanged.connect(self.onStateChanged)
        self.launchButton.clicked.connect(self.launchDialog)

    def onStateChanged(self):
        # test_list=[]
        if self.checkBoxPolsbyPopper.isChecked():
            test_list.append("Polsby-Popper")
        if self.checkBoxSchwartzberg.isChecked():
            test_list.append("Schwartzberg")
        if self.checkBoxConvexHullRatio.isChecked():
            test_list.append("Convex Hull Ratio")
        if self.checkBoxReock.isChecked():
            test_list.append("Reock")
        if self.checkBoxEfficiencyGap.isChecked():
            test_list.append("Efficiency Gap")
        if self.checkBoxMeanMedianDifference.isChecked():
            test_list.append("Mean-Median Difference")
        if self.checkBoxLopsidedMarginsTest.isChecked():
            test_list.append("Lopsided Margins Test")
        # user_input.append(test_list)
        t= [set(test_list)]
        return t




    def choose_path(self):
        dialog = QFileDialog()
        folder_path = dialog.getExistingDirectory(
            parent=self
        )
        user_input.append(folder_path)
        # print(folder_path)
        return user_input
    

    def launchDialog(self):
        # path = Window.choose_path(self)
        tests = Window.onStateChanged(self)
        # user_input = [path, tests]
        # print(user_input)
        
        return tests


    
# here = user_input
    
    # def getFileNameDialog(self):
    #     response = QFileDialog.getOpenFileName(
    #         parent=self,
    #         caption='Select a single plan',
    #         directory=os.getcwd()
    #     )
    #     print(response)
    #     return response[0]
    


# def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.choose_path()
    window.onStateChanged()
    window.launchDialog()

    sys.exit(app.exec())