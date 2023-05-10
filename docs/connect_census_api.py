class connect_census_api:

	def get_geo(user_geo_type, user_txt):
		""" Gets GeoDataFrame from Census API based on user's choice of geography level.
		Uses pygris module.
		
		Parameters
		--------------------------
		
		user_geo_type : list
			Geography level used as building blocks to create voting districts,
			chosen by user in GUI interface- passed as a list.
		user_txt : DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.
		
		Returns
		--------------------------
		list
			The list contains 4 elements:
				a. GeoDataFrame of geography level from Census API,
				b. user_geo_type,
				c. GEOID column name in user_txt,
				d. GEOID column name in GeoDataFrame from the Census API.
		
		Notes
		-----------------------------
		Steps:
			1. Gets the state code based on the first 2 digits of value in user_txt GEOID.
			2. Pulls GeoDataFrame from Census API using geography type from user_geo_type
				and state code.
			3. Gets GEOID column name in the GeoDataFrame.
		
		Examples
		------------------------------
		  
		>>> get_geo('Voting District', plan1)
		
		[{GeoDataFrame},
		 'Voting District',
		 'id',
		 'GEOID20']

		"""
		
		return
		



	def get_data(user_geo_type, user_txt):
		""" Gets demographic data from Census API based on user's choice of geography level.
		
		Parameters
		--------------------------
		
		user_geo_type : list
			Geography level used as building blocks to create voting districts,
			chosen by user in GUI interface- passed as a list.
		user_txt : DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.
		
		Returns
		--------------------------
		DataFrame
			Total population and racial data by user's chosen geography level
			from the Decennial Census.
		
		Notes
		-----------------------------
		Steps:
			1. Gets GEOID column name in the GeoDataFrame.
			2. Gets the state code based on the first 2 digits of value in user_txt GEOID.
			2. Pulls data from Census API using geography type from user_geo_type
				and state code.
			
		
		Examples
		------------------------------
		  
		>>> get_data('County Subdivision', plan1).columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop"

		"""
		
		return
		

	#merge census data to district assignment file
	def join_cen_assgn(user_txt, geo_data, user_geo_type):
		""" Join demographic data from Census API and district assignment file.
		
		Parameters
		--------------------------
		
		user_txt : DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.
		geo_data : list
			Output from get_geo():
				[GeoDataFrame, user_geo_type,
				 GEOID column name in user_txt, GEOID column name in GeoDataFrame]
		user_geo_type : list
			Geography level used as building blocks to create voting districts,
			chosen by user in GUI interface- passed as a list.
		
		Returns
		--------------------------
		DataFrame
			DataFrame with district assignment column added to demographic data
			by geography level.
		
		Notes
		-----------------------------
		Steps:
			1. Gets demographic data from Census API using get_data() 
			2. Gets GEOID column name in the user_txt and geography level from user input.
			3. Builds GEOID in Census DataFrame using state code, county code, and
				chosen geography code.
			4. Merges Census data and district assignment file.
			
		
		Examples
		------------------------------
		  
		>>> join_cen_assgn(plan1, geo_data, 'County Subdivision').columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district"

		"""
		
		return
		

	def merge_cendata_geo(data_merged, geo_data):
		""" Join merged demographic and district assignment data to GeoDataFrame.
		
		Parameters
		--------------------------
		
		data_merged : DataFrame
			Output from join_cen_assgn():
				District Assignment file merged with demographic Census data.
		geo_data : list
			Output from get_geo():
				[GeoDataFrame, user_geo_type,
				 GEOID column name in user_txt, GEOID column name in GeoDataFrame]
		
		Returns
		--------------------------
		GeoDataFrame
			GeoDataFrame with district assignment column and demographic data
			by geography level.
		
		Notes
		-----------------------------
		Steps:
			1. Gets GeoDataFrame from geo_data[0], GEOID column name from district
				assignment file, and GEOID column name from Census GeoDataFrame.
			2. Merges Census data and GeoDataFrame.
			
		
		Examples
		------------------------------
		  
		>>> merge_cendata_geo(data_merged, geo_data).columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"

		"""
		
		return
		

	def agg_geo(data_merged, geo_data, user_txt):
		""" Aggregates polygons in GeoDataFrame by district assignment.
		
		Parameters
		--------------------------
		
		data_merged : DataFrame
			Output from join_cen_assgn():
				District Assignment file merged with demographic Census data.
		geo_data : list
			Output from get_geo():
				[GeoDataFrame, user_geo_type,
				 GEOID column name in user_txt, GEOID column name in GeoDataFrame]
		user_txt: DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.
		
		Returns
		--------------------------
		GeoDataFrame
			GeoDataFrame with aggregated polygons by district assignment. Represents
			proposed redistricting plan.
		
		Notes
		-----------------------------
		Steps:
			1. Merges Census data and GeoDataFrame.
			2. Aggregates polygons by district assignment.
			3. Aggregates demographic data by district assignment.
			4. Merges aggregated data to aggregated polygons
			
		
		Examples
		------------------------------
		  
		>>> agg_geo(data_merged, geo_data, user_txt).columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"

		"""
		
		return



	def census_gdf_data(user_txt, user_geo_type):
		""" Produces GeoDataFrame with aggregated polygons by district assignment.
			Calls functions in this module based on workflow order.
		
		Parameters
		--------------------------
		
		user_txt : DataFrame
			District Assignment file provided by user.
			Contains two columns: geography level, district assignment.
			Geography level in user_txt must match user_geo_type.    
		user_geo_type : list
			Geography level used as building blocks to create voting districts,
			chosen by user in GUI interface- passed as a list.

		
		Returns
		--------------------------
		GeoDataFrame
			GeoDataFrame with aggregated polygons and demographic data
			by district assignment. Represents proposed redistricting plan.
			
		
		Examples
		------------------------------
		  
		>>> census_gdf_data(plan2, 'Places').columns
		
		"GEOID", "tot_pop", "hispLat_pop", "white_pop", "black_pop", "asian_pop", "district", "geometry"
		
		"""

		return

