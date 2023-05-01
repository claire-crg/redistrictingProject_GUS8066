# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 15:07:28 2023

@author: joshu
"""
import pandas as pd
import numpy as np
import geopandas as gpd
from election_2020 import election_2020
from historic_election_data import historic_df_builder
import partisan_fairness as pf
import os
import glob
import warnings
warnings.filterwarnings("ignore")
wd = os.getcwd()

path = wd
plans = glob.glob(os.path.join(path + "/data/plans/*.csv"))
# plan = pd.read_csv("./data/pa_no_splits.csv")

def build_geoid(plan):
    plan_df = pd.read_csv(plan)
    plan = plan_df.rename(columns={'id': 'GEOID20'})
    df = historic_df_builder()
    df = df.merge(plan, on='GEOID20')
    
    return df

def group_by_party_outcome(df):
    
    df_grouped = df.groupby(by='District')['dem_votes', 'gop_votes'].sum()
    df_grouped['d_voteshare'] = df_grouped['dem_votes']/(df_grouped['dem_votes'] + df_grouped['gop_votes'])
    df_grouped.insert(1, 'State', 'PA')
    # df_grouped.insert(1, 'Year', '2018')
    # df_grouped.insert(1, 'Incumbent', 'R')
    # df_grouped.insert(1, 'Party', 'R')
    df_grouped = df_grouped.reset_index().rename(columns = {'index':'District'})
    
    return df_grouped
    
def calc_measures(df_calc):
        
    d={}       
    
    #df_calc = df_grouped[['State', 'District' , 'dem_votes', 'gop_votes', 'd_voteshare']]
    # df_calc = df_calc.rename(columns={'dem_votes': 'Dem Votes', 'gop_votes': 'GOP Votes', 'd_voteshare' : 'D Voteshare'})
    df_calc['Party'] = np.where(df_calc['dem_votes'] > df_calc['gop_votes'], 'D', 'R')
    df_calc['total'] = df_calc.dem_votes + df_calc.gop_votes
    df_calc['dem_wasted'] = np.where(df_calc['Party'] == 'R', df_calc.dem_votes, df_calc.dem_votes - (df_calc.total/2) - .5)
    df_calc['gop_wasted'] = np.where(df_calc['Party'] == 'D', df_calc.gop_votes, df_calc.gop_votes - (df_calc.total/2) - .5)
    df_calc['r_voteshare'] = 1 - df_calc['d_voteshare']
    #df = df_calc.copy()
    d['eg'] = pf.eg(df_calc)
    d['mmd'] = pf.mean_median(df_calc)
    d['lmt'] = pf.lmt(df_calc)
    
    return d

def fairness(plan):
    a= build_geoid(plan)
    b= group_by_party_outcome(a)
    c= calc_measures(b)
    
    return c

    

##original code for joiner.py
    # plan_df = pd.read_csv(plan)
    # plan = plan_df.rename(columns={'id': 'GEOID20'})
    # df = historic_df_builder()
    # df = df.merge(plan, on='GEOID20')
    # df_grouped = df.groupby(by='District')['dem_votes', 'gop_votes'].sum()
    # df_grouped['d_voteshare'] = df_grouped['dem_votes']/(df_grouped['dem_votes'] + df_grouped['gop_votes'])
    # df_grouped.insert(1, 'State', 'PA')
    # # df_grouped.insert(1, 'Year', '2018')
    # # df_grouped.insert(1, 'Incumbent', 'R')
    # # df_grouped.insert(1, 'Party', 'R')
    # df_grouped = df_grouped.reset_index().rename(columns = {'index':'District'})
    # df_calc = df_grouped[['State', 'District' , 'dem_votes', 'gop_votes', 'd_voteshare']]
    # # df_calc = df_calc.rename(columns={'dem_votes': 'Dem Votes', 'gop_votes': 'GOP Votes', 'd_voteshare' : 'D Voteshare'})
    # df_calc['Party'] = np.where(df_calc['dem_votes'] > df_calc['gop_votes'], 'D', 'R')
    # df_calc['total'] = df_calc.dem_votes + df_calc.gop_votes
    # df_calc['dem_wasted'] = np.where(df_calc['Party'] == 'R', df_calc.dem_votes, df_calc.dem_votes - (df_calc.total/2) - .5)
    # df_calc['gop_wasted'] = np.where(df_calc['Party'] == 'D', df_calc.gop_votes, df_calc.gop_votes - (df_calc.total/2) - .5)
    # df_calc['r_voteshare'] = 1 - df_calc['d_voteshare']
    # df = df_calc.copy()
    # eg = pf.eg(df)
    # mmd = pf.mean_median(df)
    # lmt = pf.lmt(df)
    # print(eg)
    # print(mmd)
    # print(lmt)
# result = eg(df_calc)

#df_calc.to_csv("./data/2020_pa.csv")





