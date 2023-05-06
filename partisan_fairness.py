# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 10:56:25 2023

@author: joshu
"""
import sys
import os
import pandas as pd
import numpy as np



""" The following function takes the electoral outcomes from the 2020 election 
processed and released by the VEST team at Redistricting Data Hub in .shp
format. The function concatenates columns to create a GEOID20. It renames the
vote tallies for the first race as 'Dem Votes' and 'GOP Votes' and configures
the data for partisan fairness analysis by the gerrymetrics package. 
"""

def eg(df):
   dem_waste_total = df['dem_wasted'].sum()
   gop_waste_total = df['gop_wasted'].sum()
   total = df['total'].sum()
   eg = (dem_waste_total - gop_waste_total)/total
   #print(eg)
   return eg

def mean_median(df):
    dem_median = df['d_voteshare'].median()
    # gop_median = 1 - df['d_voteshare'].median
    dem_mean = df['d_voteshare'].sum()/len(df['district'])
    mean_median = abs(dem_median-dem_mean)
    #print(dem_median)
    return mean_median


def lmt(df):
    d_voteshare = np.array(df.d_voteshare)
    d_lmt = d_voteshare[df.party == 'D'].mean()
    r_voteshare = np.array(df.r_voteshare)
    r_lmt = r_voteshare[df.party == 'R'].mean()
    # print(d_lmt)
    # print (r_lmt)
    # print(d_voteshare)
    # print(r_voteshare)
    # r_list = []
    # d_list = []
    # r_win = (df['Party'] == 'R') 
    # d_win = (df['Party'] == 'D') 
    # np.where(r_win, r_list.append(df['r_voteshare']))
    # np.where(d_win, d_list.append(df['d_voteshare']))
    # r_avg = np.average(r_list)
    # d_avg = np.average(d_list)
    # lmt = d_avg - r_avg
    lmt = d_lmt - r_lmt    
    return lmt

def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

    if __name__ == "__main__":
        main()
    else:
        pass