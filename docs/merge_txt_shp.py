class merge_txt_shp:

	def merge_user_inputs(user_txt, geo_gdf, user_input_demographics):
		""" Merges district assignment and geography files provided by user,
			and aggregates polygons by district assignment.
		
		Parameters
		--------------------------
		
		user_txt : DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.    
		geo_gdf : GeoDataFrame
			Geography file provided by user, opened outside this function as GDF.
		user_input_demographics: list
			Column names of demographic columns in user inputted GeoDataFrame.
			Names provided by user in GUI interface.

		
		Returns
		--------------------------
		GeoDataFrame
			GeoDataFrame with aggregated polygons and demographic data
			by district assignment. Represents proposed redistricting plan.
			
		
		Examples
		------------------------------
		  
		>>> merge_user_inputs(plan2, PA_places, ["tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"]).columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"
		
		"""
		
		return
