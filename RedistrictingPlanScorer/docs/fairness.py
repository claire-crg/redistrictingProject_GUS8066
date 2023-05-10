class fairness:

	def build_geoid(plan, historic):
		"""
		Build a DataFrame by merging redistricting plan and historic election data on constructed geoid20 column.
		
		Parameters:
			plan (str): string of redistricing plan passed to function.
			historic (list): List passed from interface_handler including historic data file in csv format.
			st_fips (str): State FIPS code.
		
		Returns:
			DataFrame: Merged DataFrame containing plan and historic data.
		"""
		
		return

	def group_by_party_outcome(df):
		"""
		Group the DataFrame by district and calculate party outcomes.
		
		Parameters:
			df (DataFrame): DataFrame containing election data.
		
		Returns:
			DataFrame: Grouped DataFrame with summed dem_votes and gop_votes, and calculated d_voteshare.
		"""
		
		
		return
		
	def calc_measures(df_calc, user_input):
		"""
		Calculate voteshare and wasted vote measures from provided DataFrame.
		
		Parameters:
			df_calc (DataFrame): DataFrame containing election data.
		
		Returns:
			dict: Dictionary of plan scores for Efficiency Gap:'eg', Mean-Median Difference:
			mmd', and Lopsided Margins Test: 'lmt'.
		"""
			
		return

	def fairness(plan, historic, user_input):
		"""
		Main function of script. Calculates fairness measures: Efficiency Gap, Mean-Median Difference, Lopsided-Margins Test
		and returns scores for plan as dictionary. Dictionary keys: eg, mmd, lmt
		
		Parameters:
			plan (str): string of redistricting plan in .csv format passed to function from list data.
			historic (list): List item of file path to historic election data.
			st_fips (str): State FIPS code passed from geodataframe generated in merge_txt_shp.
		
		Returns:
			dict: Dictionary of calculated fairness measures.
		"""
		
		return
