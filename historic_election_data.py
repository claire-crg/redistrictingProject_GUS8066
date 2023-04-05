# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 12:43:11 2023

@author: tuq05079
"""
import os
import pandas as pd
wd = os.getcwd()

def historic_df_builder():
    path_house_2018 = './data/elections/HOUSE_precinct_general.csv'
    path_senate_2018 = './data/elections/SENATE_precinct_general.csv'
    
    house = pd.read_csv(path_house_2018)
    state = 'PENNSYLVANIA'
    
    #state_df = house.loc[(house['state'] == state)] #& (house['party_simplified'] == 'REPUBLICAN'), ['party_simplified', 'votes', 'state_fips', 'county_fips']] 
    state_df = house[house['state'].isin([state])]
    party_df = state_df[state_df['party_simplified'].isin(['DEMOCRAT', 'REPUBLICAN'])]
    party_df['precinct_suffix'] = party_df['precinct'].str.split('_').str[2]
    party_df['GEOID20'] = party_df['county_fips']+"00"+party_df['precinct_suffix']
    
    historic_election_df = party_df.groupby(['GEOID20'], as_index=True).agg({'dem_votes':'max', 'gop_votes':'max', 'jurisdiction_fips':'first', 'year':'first'})
    return historic_election_df


def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

    if __name__ == "__main__":
        main()
    else:
        pass