"""
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QCheckBox
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys
import os

cwd = os.getcwd()
user_input=[]
plan=[]
shape=[]
historic =[]

class UI(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle('Redistricting Plan Loader')
        self.setWindowIcon(QIcon('templeicon.png'))
        self.show()
        self.plan_button.clicked.connect(self.browse_plan_box)
        self.shape_button.clicked.connect(self.browse_shape_box)
        self.historic_button.clicked.connect(self.browse_historic_box)
        #find children

        self.checkBoxes = [self.pp_box, self.schwartzberg_box, self.c_hull_box,
                           self.reock_box, self.eg_box, self.mmd_box, self.lmt_box]
        
        button = self.findChild(QPushButton, 'compare_button') 
        button.clicked.connect(self.launch_tests)        
        
    def on_state_changed(self):
        for self.checkBox in self.checkBoxes:
            if self.checkBox.isChecked() == True:
                user_input.append(self.checkBox.text())
            # print(self.checkBox.text() + str(self.checkBox.isChecked()))
              
    def browse_plan_box(self):
        self.plan_path = QFileDialog.getExistingDirectory(self)
        self.plan_text.setText(self.plan_path)
        plan.append(self.plan_path)
    def browse_shape_box(self):
        self.shape_file = QFileDialog.getOpenFileName(self)
        self.shape_text.setText(self.shape_file[0])
        shape.append(self.shape_file[0])
    def browse_historic_box(self):
        self.historic_file = QFileDialog.getOpenFileName(self)
        self.historic_text.setText(self.historic_file[0])
        historic.append(self.historic_file[0])
    
    # def tests(self):
    #     if self.pp_box.isChecked():
    #         pp_test = self.pp_box.text()
    #         print(pp_test)
    #         return pp_test
            
    def launch_tests(self):
        user_input.append(plan)
        user_input.append(shape)
        user_input.append(historic)
        # for box in self.checkBoxes:
        #     if self.checkState() == 2:
        #         on_list.append(self.checkBox.text)                
        self.on_state_changed()
        window.close()
        

        
app = QApplication(sys.argv)
window = UI()
# window.show()
app.exec_()