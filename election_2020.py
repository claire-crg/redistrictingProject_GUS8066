# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 10:56:25 2023

@author: joshu
"""
import sys
import os
import pandas as pd
import geopandas as gpd


""" The following function takes the electoral outcomes from the 2020 election 
processed and released by the VEST team at Redistricting Data Hub in .shp
format. The function concatenates columns to create a GEOID20. It renames the
vote tallies for the first race as 'Dem Votes' and 'GOP Votes' and configures
the data for partisan fairness analysis by the gerrymetrics package. 
"""

def election_2020():
    # wd = os.getcwd()
    path = "./data/pa_vest_20.shp"
    df = gpd.read_file(path)
    df['GEOID20'] = df['STATEFP']+df['COUNTYFP'] + df['VTDST']
    df = df.rename(columns={'G20PREDBID':'dem_votes', 'G20PRERTRU':'gop_votes'})
    df['total'] = df['dem_votes'] + df['gop_votes']
    df['d_voteshare'] = df['dem_votes']/df['total']
    df.insert(1, 'state', 'PA')
    df.insert(1, 'year', '2020')
    # state = "PA"
    # df['state'] = state
    # year = '2020'
    # df['year'] = year    
    df_2020 = df[['state', 'year', 'GEOID20', 'dem_votes', 'gop_votes', 'd_voteshare', 'total', 'geometry']]
    return df_2020

def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

    if __name__ == "__main__":
        main()
    else:
        pass