class lobby_new:

	def csv_check(plans):
		""" Check that district assignment files were provided.
		
		Parameters
		--------------------------
		plans: List
			List with the path strings for the plans.
		
		Returns
		--------------------------
		String
			Error message
		
		"""
		
		pass
		

	def check_cols_match(user_gdf, user_txt):
		""" Check if GEOID columns match.
		
		Parameters
		--------------------------
		user_gdf: GeoDataFrame
			Geography file provided by user, opened outside this function as GDF.
		user_txt: DataFrame
			User inputted district assignment file.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.  
		
		Returns
		--------------------------
		String
			Either update or error message.
		
		"""
		pass
