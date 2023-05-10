class compactness:
	def compact(measures, geo_df):
		
		"""Calculates compactness measures based on which measures the user chooses.

		Minimum and mean values are returned for each chosen measure. This gives a
		user an idea of how well a model performs without providing a score for
		each polygon. Some users might pass a thousand plans.

		Parameters
		--------------------------

		measures : list
			Compactness measures chosen by user in the GUI interface.
		geo_df : GeoDataFrame
			Either the geometry file provided by user or the one pulled from the Census API.
			gdf gets passed after polygons have been aggregated by district assignment.

		Returns
		--------------------------
		dictionary
			Dictionary containing names and values of calculated compactness measures.

		Examples
		------------------------------
	   
		>>> compact(['Polsby Popper', 'Convex Hull Ratio'], gdf_vtds)
		{
		 "min_pp": 0.03,
		 "mean_pp": 0.3,
		 "min_hull": 0.2,
		 "mean_hull": 0.4
		 }

		Example of dictionary returned for one plan passed through compactness()""" 
		
		return

