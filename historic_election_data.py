# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:43:11 2023

@author: tuq05079
"""
import os
import pandas as pd
from get_column_info import split_string, get_state_geoid


def historic_df_builder(plan, historic, st_fips):
        """
Build a historic election DataFrame to calculate voteshare based on a plan DataFrame and a historic DataFrame.

Parameters:
    plan (DataFrame): DataFrame containing plan information.
    historic (list): List of file paths to historic data files. Ideally from Harvard Dataverse:
        MIT Election Data and Science Lab, 2022, "U.S. House of Representatives Precinct-Level Returns 2018",
        https://doi.org/10.7910/DVN/IVIXLK, Harvard Dataverse, V1, UNF:6:LuDzTUr155JEhY8ckZ+HHg== [fileUNF]
    st_fips (str or None): State FIPS code. If provided, overrides state FIPS code found in the plan DataFrame.
    
Returns:
    DataFrame: Historic election DataFrame with aggregated data.
    """


    plan.columns = [x.lower().strip() for x in plan.columns]

    if 'state_fips' in plan.columns:
        plan['state_fips'] = plan['state_fips'].apply(lambda x: '{0:0>2}'.format(x))
        state_fips =  plan['state_fips'][1]
        print(f"state_fips = {state_fips}")# grabs state fips code if in plan.
    elif "geoid20" in plan.columns:
        state_fips = plan['geoid20'][1][:2]
        print(f"geoid = {state_fips}")# uses geoid to generate state fips code if in plan.
    elif st_fips is not None:
        state_fips = st_fips # uses state fips code from geodataframe if other options not available.
    else:
        print('No state code found')

    house = pd.read_csv(historic[0], engine ='python')
    house.columns = [x.lower().strip() for x in house.columns]  
    house['plan_fips'] = state_fips
    house = house.astype({'plan_fips': 'Int64'})

 
    state_df = house.loc[house['state_fips'] == house['plan_fips']]
    
    party_df = state_df[state_df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])]
    party_df['precinct_suffix'] = party_df['precinct'].str.split('_').str[2]
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
