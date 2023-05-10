# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:43:11 2023

@author: tuq05079
"""
# import os
import pandas as pd
# from get_column_info import split_string, get_state_geoid


def historic_df_builder(plan_df, historic, st_fips):
    """
    Build a historic election DataFrame to calculate voteshare based on a plan DataFrame and a historic DataFrame.
    Parameters:
        plan (DataFrame): DataFrame containing plan information.
        historic (list): List of file paths to historic data files. Ideally from Harvard Dataverse:
            MIT Election Data and Science Lab, 2022, "U.S. House of Representatives Precinct-Level Returns 2018",
            https://doi.org/10.7910/DVN/IVIXLK, Harvard Dataverse, V1, UNF:6:LuDzTUr155JEhY8ckZ+HHg== [fileUNF]. Should
            include a column named 'state_fips' with state fips code and 'party simplified' with party names 'DEMOCRAT' or
            'REPUBLICAN'. Should also include 'county_fips' for building geoid20.
        st_fips (str or None): State FIPS code. If provided, overrides state FIPS code found in the plan DataFrame.
    
    Returns:
        DataFrame: Historic election DataFrame with aggregated data.
    """


    plan_df.columns = [x.lower().strip() for x in plan_df.columns]
    # set some state fips code for subsetting the national election returns dataset.
    if 'state_fips' in plan_df.columns:
        plan_df['state_fips'] = plan_df['state_fips'].apply(lambda x: '{0:0>2}'.format(x))
        state_fips =  plan_df['state_fips'][1]
    # if not in the plan column names, look for geoid and grab first two digits
    elif "geoid20" in plan_df.columns:
        state_fips = plan_df['geoid20'][1][:2]
    #else use passed st_fips 
    elif st_fips is not None:
        state_fips = st_fips
    else:
        print('No state code found')

    #read in user passed historic path .csv
    house = pd.read_csv(historic[0], engine='python')
    house.columns = [x.lower().strip() for x in house.columns]  
    # assign fips to subset plan
    house['plan_fips'] = state_fips
    house = house.astype({'plan_fips': 'Int64'}) 
    state_df = house.loc[house['state_fips'] == house['plan_fips']]
    # select only gop and dem votes for consideration    
    party_df = state_df[state_df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])]
    # build geoid20 for merging
    party_df['precinct_suffix'] = party_df['precinct'].str.split('_').str[2]
    party_df[['county_fips', 'precinct_suffix']] = party_df[['county_fips', 'precinct_suffix']].astype(str)
    party_df['geoid20'] = party_df['county_fips']+"00"+party_df['precinct_suffix']
    
    historic_election_df = party_df.groupby(['geoid20'], as_index=True).agg({'dem_votes':'max', 'gop_votes':'max', 'jurisdiction_fips':'first', 'year':'first'})

    return historic_election_df


def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

    if __name__ == "__main__":
        main()
    else:
        pass