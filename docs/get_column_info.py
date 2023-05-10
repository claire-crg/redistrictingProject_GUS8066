class get_column_info:

	def split_string(x):
		""" Gets the first 2 digits of a string.
		
		Parameters
		--------------------------
		
		x: string
		
		Returns
		--------------------------
		String
		
		Examples
		------------------------------
		
		>>> split_string('421011902')
		'42'
		"""
		
		return


	def get_state_geoid(user_txt):
		""" Gets the GEOID column name and state code.
		
		Parameters
		--------------------------
		
		user_txt: DataFrame
			User inputted district assignment file.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.  
		
		Returns
		--------------------------
		List
			1. GEOID column name
			2. 2 digit state code
		
		Examples
		------------------------------
		
		>>> get_state_geoid(plan10)
		['geoid', '42']
		
		"""
		
		return

	def get_dist_col(user_txt):
		""" Gets the district column name.
		
		Parameters
		--------------------------
		
		user_txt: DataFrame
			User inputted district assignment file.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.  
		
		Returns
		--------------------------
		String
			District column name
		
		Examples
		------------------------------
		
		>>> get_dist_col(plan10)
		'dist'
		
		"""
		
		return


	def chng_dist_col(user_txt):
		""" Change district column name.
		
		Parameters
		--------------------------
		
		user_txt: DataFrame
			User inputted district assignment file.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.  
		
		Returns
		--------------------------
		DataFrame
			Updated DataFrame of user_txt
		
		"""
		
		return


	def get_gdf_geoid(user_gdf, user_txt):
		""" Gets the GEOID column name in user geography file.
		
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
			GEOID column name
		
		Examples
		------------------------------
		
		>>> get_gdf_geoid(gdf_placeds, plan5)
		'GEOid'
		
		"""
		
		return



