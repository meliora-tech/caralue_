# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 08:08:57 2021

@author: 27608
"""

import pandas as pd

   
def summary_statistics(list_ans):

     df         = pd.DataFrame(list_ans)
     df["year"] = df["year"].astype(int)
     avg        = df.groupby('year').mean().reset_index().to_dict('records')
     median     = df.groupby('year').median().reset_index().to_dict('records')
     
     
     
     all_dict = {}
     years =  list(df["year"].unique())
     years.sort()
     for year in years:
         temp_df = df[df["year"]== year]
         temp_df["bins"] = pd.cut(temp_df['mileage'],5)
         temp_df =   temp_df.groupby("bins").mean().dropna().reset_index()
         temp_df['bins'] = temp_df['bins'].astype(str)
         
         all_dict[year] = temp_df.to_dict('records')
         
         
     return avg, median, all_dict