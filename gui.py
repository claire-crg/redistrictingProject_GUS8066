"""
"""
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QCheckBox, QComboBox
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import sys
import os
from osgeo import ogr
from final_dict_builder import final_dict_builder
import pandas as pd
from pathlib import Path

user_input=[]
plans_folder=[]
shape=[]
historic =[]
geo_list =['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
user_geo = []
user_pop = []
pop_column_options = []
compactness_tests = ['Polsby-Popper', 'Schwartzberg', 'Convex Hull Ratio', 'Reock'] 
fairness_tests = ['Efficiency Gap', 'Mean-Median Difference', 'Lopsided-Margins Test']
population_tests = ['Equal Population']
final_dictionary = {}

    
class UI(QWidget):
    """
    A PyQt5 GUI for redistricting plan loading and launching tests.

    Attributes:
        plan_button (QPushButton): Button for browsing and selecting a redistricting plan path.
        shape_button (QPushButton): Button for browsing and selecting a shapefile.
        historic_button (QPushButton): Button for browsing and selecting a path to historical election data.
        geo_combo (QComboBox): Combo box for selecting census geography level.
        pop_combo (QComboBox): Combo box for selecting population field.
        checkBoxes (list): List of QCheckBox objects for selecting compactness,
            partisan fairness, and equal population tests.
        compare_button (QPushButton): Button for launching tests.
    """
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.setWindowTitle('Redistricting Plan Loader')
        self.setWindowIcon(QIcon('templeicon.ico'))
        self.show()
        self.plan_button.clicked.connect(self.browse_plan_box)
        self.shape_button.clicked.connect(self.browse_shape_box)

        self.historic_button.clicked.connect(self.browse_historic_box)
        self.geo_combo.addItems(geo_list)
        self.geo_combo.activated.connect(self.choose_geo)
        self.pop_combo.addItems(pop_column_options)
        self.pop_combo.activated.connect(self.choose_pop)
    
        
        #find children

        self.checkBoxes = [self.pp_box, self.schwartzberg_box, self.c_hull_box,
                           self.reock_box, self.eg_box, self.mmd_box, self.lmt_box, self.population_box]
        

        self.compare_button.clicked.connect(self.launch_tests)        
        
    def on_state_changed(self):
        """
        Updates the user_input list based on the state of the checkboxes when
        launch button is pushed.
        """
        for self.checkBox in self.checkBoxes:
            if self.checkBox.isChecked() == True:
                user_input.append(self.checkBox.text())


    def choose_geo(self):
        """
        Stores the selected census geography in user_geo list.
        Choices should be ['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
        but only 'Voting District' is functioning
        """
        self.geo_choice = self.geo_combo.currentText()
        user_geo.append(self.geo_choice)        

    def choose_pop(self):
        """
        Store the selected population field in user_pop list.
        """
        self.pop_choice = self.pop_combo.currentText()
        user_pop.append(self.pop_choice)

    def browse_plan_box(self):
        """
        Open a file dialog to browse and select a redistricting plan path.
        """
        self.plan_path = QFileDialog.getExistingDirectory(self)
        self.plan_text.setText(self.plan_path)
        plans_folder.append(self.plan_path)

    def browse_shape_box(self):
        """
        Open a file dialog to browse and select a shapefile.
        """
        self.shape_file = QFileDialog.getOpenFileName(self)
        self.shape_text.setText(self.shape_file[0])
        shape.append(self.shape_file[0])
        self.get_pop_column()

        
    def get_pop_column(self):
        """
        Get the population column options from the selected shapefile
        and send to update the choose_pop combo box with them.
        Default value = 'tot_pop'
        """
        file = shape[0]
        if len(file) > 0:
            source = ogr.Open(file)
            layer = source.GetLayer()
            ldefn = layer.GetLayerDefn()
            for n in range(ldefn.GetFieldCount()):
                fdefn = ldefn.GetFieldDefn(n)
                pop_column_options.append(fdefn.name)
            self.update_pop_combo()
        else:
            cen_pop = 'tot_pop'
            pop_column_options.append(cen_pop)
            self.update_pop_combo()
    def update_pop_combo(self):
        """
        Update the population combo box with the available options.
        """
        self.pop_combo.addItems(pop_column_options)
    def browse_historic_box(self):
        """
        Open a file dialog to browse and select a path to historical election data.
        """
        self.historic_file = QFileDialog.getOpenFileName(self)
        self.historic_text.setText(self.historic_file[0])
        historic.append(self.historic_file[0])

            
    def launch_tests(self):
        """
        Call on_state_changed to append the user_options, close the window, and pass the lists
        Loop completes when dictionary of plans returns
        """             
        self.on_state_changed()   
        window.close()
        final = final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic)
        final_dictionary.update(final)
        output = pd.DataFrame(final_dictionary)
        here = Path.cwd()
        pwp = here.parents[2]
        if Path('output').exists == True:
            output.to_csv("output/score.csv")
        else: 
            Path.mkdir('output')
            output.to_csv("output/score.csv")
            
            
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('templeicon.ico'))
    window = UI()
    window.show()
    sys.exit(app.exec_())
