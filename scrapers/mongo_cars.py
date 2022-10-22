# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 08:30:29 2021

@author: Car pricing

Take all the scraped car data and place them
into the mongo collection
"""

import pymongo 
import pandas as pd
import datetime
import glob



client = pymongo.MongoClient("mongodb+srv://")

db      = client["cars_db"]

car_collection    = db["cars"]


# Get the data
car_dir = "cars-20211112"
saved_dir = "data//"+car_dir

# Get the files
csv_files = glob.glob1(saved_dir, "*.csv")


# Insert the data into the mongodb database->collection
for file in csv_files:
    df = pd.read_csv(saved_dir+"//"+file)
    
    
    df_dict = df.to_dict('records')

        
    try:
        car_collection.insert_many(df_dict)
    
        print("Successful at inserting "+ file)
    except Exception as e:
       print(e)
       print("Unsuccessful in inserting "+ file)
        