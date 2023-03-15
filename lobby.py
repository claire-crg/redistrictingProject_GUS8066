# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 07:41:49 2023

@author: joshu
"""

import  tkinter as tk
from tkinter import filedialog
import pandas as pd
import geopandas as gpd
import glob
import os
import zipfile
import requests
import io


def shp_fp20_check():
    return 'wrong' if len(set(shp_fp20_list)) > 1 else 'correct'

def csv_fp20_check():
    return 'wrong' if len(set(csv_fp20_list)) > 1 else 'correct'


#convert csv_files to pandas dataframes



def csv_check(file):
    name = os.path.splitext(os.path.basename(file))[0]
    input_file = pd.read_csv(file, delimiter=",", dtype={"GEOID20": "string", "District":int}, header=0)
    csv_fp20 = input_file['GEOID20'][1][:2]
    csv_fp20_list.append(csv_fp20)
    return csv_fp20

def shp_check(file):
    shp_df = gpd.read_file(file)
    if "STATEFP20" in shp_df.columns:
        shp_fp20 = shp_df["STATEFP20"][1]
        shp_fp20_list.append(shp_fp20)
        return shp_fp20
    else:
        print("No state/fp20 column identified in shapefile. Check that csv and shp files are the same geography.")

def csv_df_builder(file):   
    name = os.path.splitext(os.path.basename(file))[0]
    input_file = pd.read_csv(file, delimiter=",", dtype={"GEOID20": "string", "District":int}, header=0)
    csv_df = pd.DataFrame(input_file)
    shp_df = gpd.read_file(shp_files[0])
    df = shp_df.merge(csv_df, on='GEOID20')
    gpd.GeoDataFrame.to_file(df, filename= "./data/" + name + "_gdf.shp")

def shp_df_builder(file):
    name = os.path.splitext(os.path.basename(file))[0]
    shp_df = gpd.read_file(file) 
    gpd.GeoDataFrame.to_file(shp_df, filename= "./data/" + name + "_gdf.shp")

    

def vtd_download(csv_fp20):
    # build file path for voting district shapefile download. 
    shp_root = "https://www2.census.gov/geo/tiger/TIGER2020PL/LAYER/VTD/2020/tl_2020_"
    shp_stem = csv_fp20
    shp_leaf = "_vtd20.zip"
    url = shp_root + shp_stem + shp_leaf
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path='./data/')
    shp_files = glob.glob(path + '*/data/*.shp')    
    shp_df = gpd.read_file(shp_files[0])

    
root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()


csv_files = glob.glob(path + '/*.csv')
shp_files = glob.glob(path + '/*.shp')
#create empty list for shp_fp20s
shp_fp20_list = []
#create empty list for fp20s
csv_fp20_list = []

if len(shp_files)==0 and len(csv_files)==0:
    print('No valid shapefiles or assignment files detected.')
    print('Terminating file loader.')
    exit()
elif len(shp_files)==0 and len(csv_files) > 0:    
    print("No shapefile detected.")
    print("Voting District geographies files will be retrieved from Census Department")
    print("if valid csv assignment files are present.")
    print("This should trigger .csv function")
    for file in csv_files:
        csv_fp20 = csv_check(file)
    if csv_fp20_check() == 'correct' and len(shp_files)==0:
        vtd_download(csv_fp20)
        csv_df_builder(file)
    elif csv_fp20_check() == 'correct':
        csv_df_builder(file)
    else:
        print("Included csv files have unmatched state/fp20 codes. Terminating file loader.")
        exit()
elif len(shp_files) > 0 and len(csv_files)==0:
    for file in shp_files:
        shp_check(file)
        if shp_fp20_check() == 'correct':
            shp_df_builder(file)
        else:
            print("1 Shapefile (or files) lack state/fp20 codes or represent different geometries.")
elif len(shp_files) > 0 and len(csv_files) > 0:
    for file in shp_files:
        shp_check(file)
        if shp_fp20_check() == 'correct':
            shp_df_builder(file)
    for file in csv_files:
        csv_check(file)
        if csv_fp20_check() == 'correct':
            csv_df_builder(file)

    
else:
    print('Undesignated problem.')
    



    



