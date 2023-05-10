class gui:

	def on_state_changed(self):
		"""
		Updates the user_input list based on the state of the checkboxes when
		launch button is pushed.
		"""
		return


	def choose_geo(self):
		"""
		Stores the selected census geography in user_geo list.
		Choices should be ['County', 'County Subdivision', 'Place', 'Tract', 'Voting District']
		but only 'Voting District' is functioning
		"""
		return       

	def choose_pop(self):
		"""
		Store the selected population field in user_pop list.
		"""
		return

	def browse_plan_box(self):
		"""
		Open a file dialog to browse and select a redistricting plan path.
		"""
		return

	def browse_shape_box(self):
		"""
		Open a file dialog to browse and select a shapefile.
		"""
		return

		
	def get_pop_column(self):
		"""
		Get the population column options from the selected shapefile
		and send to update the choose_pop combo box with them.
		Default value = 'tot_pop'
		"""
		return
			
	def update_pop_combo(self):
		"""
		Update the population combo box with the available options.
		"""
		return
		
	def browse_historic_box(self):
		"""
		Open a file dialog to browse and select a path to historical election data.
		"""
		return

			
	def launch_tests(self):
		"""
		Call on_state_changed to append the user_options, close the window, and pass the lists
		Loop completes when dictionary of plans returns
		"""             
		return
			
			
	