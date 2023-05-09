# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:07:28 2023

@author: joshu
"""
import pandas as pd
import numpy as np
from historic_election_data import historic_df_builder
import partisan_fairness as pf
from get_column_info import get_state_geoid


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
    
    plan_df = pd.read_csv(plan)
    geo_id, st_fips = get_state_geoid(plan_df)
    plan_df = plan_df.rename(columns={'id': 'geoid20'})
    plan_df.columns = [x.lower().strip() for x in plan_df.columns]
    df = historic_df_builder(plan_df, historic, st_fips)
    df = df.merge(plan_df, on='geoid20')
    
    return df

def group_by_party_outcome(df):
    """
    Group the DataFrame by district and calculate party outcomes.
    
    Parameters:
        df (DataFrame): DataFrame containing election data.
    
    Returns:
        DataFrame: Grouped DataFrame with summed dem_votes and gop_votes, and calculated d_voteshare.
    """
    
    
    df_grouped = df.groupby(by='district')[['dem_votes', 'gop_votes']].sum()
    df_grouped['d_voteshare'] = df_grouped['dem_votes']/(df_grouped['dem_votes'] + df_grouped['gop_votes'])
    df_grouped = df_grouped.reset_index().rename(columns = {'index':'district'})
    
    return df_grouped
    
def calc_measures(df_calc, user_input):
    """
    Calculate voteshare and wasted vote measures from provided DataFrame.
    
    Parameters:
        df_calc (DataFrame): DataFrame containing election data.
    
    Returns:
        dict: Dictionary of plan scores for Efficiency Gap:'eg', Mean-Median Difference:
        mmd', and Lopsided Margins Test: 'lmt'.
    """
        
    d={}       
    

    df_calc['party'] = np.where(df_calc['dem_votes'] > df_calc['gop_votes'], 'D', 'R')
    df_calc['total'] = df_calc.dem_votes + df_calc.gop_votes
    df_calc['dem_wasted'] = np.where(df_calc['party'] == 'R', df_calc.dem_votes, df_calc.dem_votes - (df_calc.total/2) - .5)
    df_calc['gop_wasted'] = np.where(df_calc['party'] == 'D', df_calc.gop_votes, df_calc.gop_votes - (df_calc.total/2) - .5)
    df_calc['r_voteshare'] = 1 - df_calc['d_voteshare']

    #df = df_calc.copy()
    
    
    if "Efficiency Gap" in user_input:
        d['eg'] = pf.eg(df_calc)
    if "Mean-Median Difference" in user_input:
        d['mmd'] = pf.mean_median(df_calc)
    if "Lopsided-Margins Test" in user_input:
        d['lmt'] = pf.lmt(df_calc)
        

    return d

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
    a= build_geoid(plan, historic)
    b= group_by_party_outcome(a)
    c= calc_measures(b, user_input)
    
    return c
