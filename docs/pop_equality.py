class pop_equality:

	def get_pop_col(user_input_pop_col, gdf):
		""" Gets column name for population data from GeoDataFrame.
		
		Parameters
		--------------------------
		
		user_input_pop_col: list
			Column names of population data inputted by user in GUI interface.
		gdf : GeoDataFrame
			Geography file after polygons are aggregated.
			Either provided by user or pulled from Census API.
		
		Returns
		--------------------------
		String
			String of population column name.
			
		
		Examples
		------------------------------
		  
		Using GDF provided by user and user specified column in GUI interface:
		>>> get_pop_col(["population"], gdf_aggregated)
		
		"population"
		
		Using GDF from Census API. No column name provided by user in GUI interface:
		>>> get_pop_col([], gdf_aggregated)
		
		"tot_pop"
		
		"""
		
		return

	def equal_population(gdf, pop_column):
		""" Calculates if there is equal number of population in each polygon.
		
		Parameters
		--------------------------
		
		gdf : GeoDataFrame
			Geography file after polygons are aggregated.
			Either provided by user or pulled from Census API.
		pop_column: String
			Column name of population column in GeoDataFrame
		
		Returns
		--------------------------
		Dictionary
			Says whether there is equal population or not.
			
		
		Examples
		------------------------------
		  
		Using GDF provided by user and user specified column in GUI interface:
		>>> equal_population(gdf_aggregated, ["pop_column"])
		
		{
		 "equal_pop" : 'No'
		 }
		
		Using GDF from Census API. No column name provided by user in GUI interface:
		>>> equal_population(gdf_aggregated, [])
		
		{
		 "equal_pop" : 'No'
		 }
		
		"""
		
		return

	def pop_difference(gdf, pop_column):
		""" Calculates by how much population quantity varies between polygons.
		
		Parameters
		--------------------------
		
		gdf : GeoDataFrame
			Geography file after polygons are aggregated.
			Either provided by user or pulled from Census API.
		pop_column: String
			Column name of population column in GeoDataFrame
		
		Returns
		--------------------------
		Dictionary
			Measures indicating how much population count differs.
			
		Notes
		-----------------------------
		Measures of population equality:
			1. Range = highest population count - lowest population count
			2. mean_deviation = sum(actual - ideal)/number of polygons
			3. range_deviation = abs(max((actual - ideal)/actual))+abs(min(actual - ideal)/actual))
		
		Examples
		------------------------------
		  
		Using GDF provided by user and user specified column in GUI interface:
		>>> pop_difference(gdf_aggregated, ["pop_column"])
		
		{
		 "pop_range_value" : 4048,
		 "pop_mean_deviation" : 4.1,
		 "pop_range_deviation" : 0.005
		 
		 }
		
		Using GDF from Census API. No column name provided by user in GUI interface:
		>>> pop_difference(gdf_aggregated, [])
		
		{
		 "pop_range_value" : 4048,
		 "pop_mean_deviation" : 4.1,
		 "pop_range_deviation" : 0.005
		 }
		
		"""
		
		return


