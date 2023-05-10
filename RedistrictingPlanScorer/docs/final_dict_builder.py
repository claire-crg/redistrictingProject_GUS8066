class final_dict_builder:

	def final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic):
		""" Runs redistricting measures based on user inputs for each plan
			and creates a dictionary of dictionary holding the results for each plan.
		
		Parameters
		--------------------------
		
		plans_folder : List
			A list with the path (string) to the folder containing all proposed
			redistricting plans.
		shape: List
			A list with the path (string) for the geography file.
		user_input: List
			A list with the names of measures chosen by the user in the GUI interface.
		user_geo: List
			A list with the name of the geography level they are working with.
		historic: List
			A list containing the path (string) for the historic election data file.
		
		Returns
		--------------------------
		Dictionary of dictionaries
			Each sub-dictionary corresponds to a single plan from the folder of plans
			and contains the results of the user's chosen measures.
			
		Notes
		-----------------------------
		Redistricting measures:
			1. Compactness: how close to a circle is the shape of the proposed district?
			2. Fairness: does a political party have an unfair advantage in a district?
			3. Population: is the equal population requirement met?
		
		Examples
		------------------------------
		
		>>> final_dict_builder(plans_folder, shape, user_input, user_pop, user_geo, historic)
		
		{
		 plan1:{
			 "eg": 0.07,
			 "lmt": 0.08,
			 "mean_pp": 0.2,
			 "min_pp": 0.01,
			 "pop_range_value" : 4048,
			 "pop_mean_deviation" : 4.1,
			 "pop_range_deviation" : 0.005
			 },
		 plan2:{
			 "eg": 0.07,
			 "lmt": 0.09,
			 "mean_pp": 0.5,
			 "min_pp": 0.2,
			 "pop_range_value" : 7671,
			 "pop_mean_deviation" : 4.79e-11,
			 "pop_range_deviation" : 0.01
			 }  
		 }
		
		"""
		
		return


