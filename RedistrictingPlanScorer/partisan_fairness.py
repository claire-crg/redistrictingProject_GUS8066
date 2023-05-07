# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 10:56:25 2023

@author: joshu
"""
import sys
import os
import pandas as pd
import numpy as np



""" 

"""

def eg(df):
    """
    Calculate the efficiency gap (EG) based on the provided DataFrame.
 
    Efficiency Gap indicates difference between the two parties total votes cast
    for an unsuccessful candidate AND any vote surplus for a successful candidate
    (both considered wasted votes) over all districts for each party divided by
    total votes.
    
    Reference: Stephanopoulos, Nicholas and McGhee, Eric,
    Partisan Gerrymandering and the Efficiency Gap (October 1, 2014).
    82 University of Chicago Law Review, 831 (2015), U of Chicago,
    Public Law Working Paper No. 493,
    Available at SSRN: https://ssrn.com/abstract=2457468
      
    Parameters:
        df (DataFrame): DataFrame containing election data from historic_election_data with
        'dem_wasted', 'gop_wasted', and 'total' columns.

    Returns:
        float: Efficiency gap value.
    """    
    dem_waste_total = df['dem_wasted'].sum()
    gop_waste_total = df['gop_wasted'].sum()
    total = df['total'].sum()
    eg = (dem_waste_total - gop_waste_total)/total
    #print(eg)
    return eg

def mean_median(df):
    """
    Calculate the mean-median difference (MMD) based on the provided DataFrame.
    
    Score indicates difference between a party's  median voteshaer minus its mean
    for all districts. According to planscore.org, "When the mean and the median
    diverge significantly, the district distribution is skewed in favor of one
    party and against its opponent."
    
    Reference: Mcdonald, Michael & Best, Robin. (2015). Unfair Partisan Gerrymanders
    in Politics and Law: A Diagnostic Applied to Six Cases. Election Law Journal:
    Rules, Politics, and Policy. 14. 312-330. 10.1089/elj.2015.0358. 
    
    Parameters:
        df (DataFrame): DataFrame from fairness module containing election data
        with party voteshare.
    Returns:
        float: Mean-median difference value.
    """
    dem_median = df['d_voteshare'].median()
    # gop_median = 1 - df['d_voteshare'].median
    dem_mean = df['d_voteshare'].sum()/len(df['district'])
    mean_median = abs(dem_median-dem_mean)

    return mean_median


def lmt(df):
    """
    Calculate the lopsided margins test (LMT) based on the provided DataFrame.
    
    Metric is a t-test conducted on degree of winning voteshare of district totaled. 
    
    Reference: Sam Wang, “Three Tests for Practical Evaluation of Partisan Gerrymandering,”
    Stanford Law Journal, 16, June 2016. Available at:
    https://www.stanfordlawreview.org/print/article/three-tests-for-practical-evaluation-ofpartisan-gerrymandering/)
    
    Parameters:
        df (DataFrame): DataFrame from fairness module containing election data with party voteshare.
    
    Returns:
        float: Lopsided margins test value.
    """
    d_voteshare = np.array(df.d_voteshare)
    d_lmt = d_voteshare[df.party == 'D'].mean()
    r_voteshare = np.array(df.r_voteshare)
    r_lmt = r_voteshare[df.party == 'R'].mean()
    lmt = d_lmt - r_lmt    
    return lmt

def main():
    # Typical uses for main are to run or call a test or to run a 
    # significant or commonly used function from the command line

    if __name__ == "__main__":
        main()
    else:
        pass