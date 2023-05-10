# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 17:24:09 2023

@author: tup48123
"""


#get state code
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
    
    st = x[:2]
    return st


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
    
    ##get state from user input
    #find the column with GEOID
    geoid_col = user_txt.applymap(lambda x: len(str(x)) > 4).all()
    
    #get the name of the GEOID column
    geoid = str(geoid_col[geoid_col].index[0])

    #choose the first 2 digits
    stt = user_txt[geoid].apply(split_string)
    state_id = stt[1]
    
    return geoid, state_id

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
    
    #find the column with GEOID
    district_col = user_txt.applymap(lambda x: len(str(x)) < 4).all()
    district_csv = district_col[district_col].index[0]

    return district_csv


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
    
    #find the column with GEOID
    district_col = user_txt.applymap(lambda x: len(str(x)) < 4).all()
    district_csv = district_col[district_col].index[0]
    user_txt = user_txt.rename(columns={str(district_csv):'district_csv'})
    

    return user_txt


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
    
    #get state id
    state_id = get_state_geoid(user_txt)[1]
    #find the column with GEOID
    geoid_col_shp = user_gdf.applymap(lambda x: len(str(x)) > 4 and str(x).startswith(str(state_id))).all()
    geoid_shp = str(geoid_col_shp[geoid_col_shp].index[0])
    
    return geoid_shp




