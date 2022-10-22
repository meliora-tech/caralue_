# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 13:15:36 2021

@author: Car pricing
"""



from selenium import webdriver
import time
import random
import re
import pandas as pd
import datetime
import os

url = "https://www.autotrader.co.za/cars-for-sale?isused=True"




CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"


driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)


all_car_names   = []
all_car_prices  = []
all_car_mileage = []
all_year_mileage   = []



pages = 2931

for page in range(1,pages+1):
    
    
    if page == 1:
      driver.get(url)
    else:
        link = "https://www.autotrader.co.za/cars-for-sale?pagenumber="+ str(page) +"&isused=True"
        driver.get(link)
            
    time.sleep(random.randint(5,10))
    
    all_cars = driver.find_elements_by_class_name("b-result-tile")
    
    for car_element in all_cars: 
        price        = car_element.find_elements_by_class_name("e-price-container")[0].text
        name         = car_element.find_elements_by_class_name("e-title")[0].text
        year_mileage = car_element.find_elements_by_class_name("e-icons")[0].text   
        
        
        all_car_prices.append(price)
        all_car_names.append(name)
        all_year_mileage.append(year_mileage)
        

driver.close()


#== Clean ==#

# Get the prices
prices = [ p.replace("R","").replace(" ","").strip() for p in all_car_prices]


# Get the year
years = [ y[:4] for y in all_year_mileage]

# Get the mileage
mileage_only = [ y[4:] for y in all_year_mileage]

m = re.compile("\d+\s\d+")

mileage = ["".join(m.findall(mil)).replace(" ","") for mil in mileage_only]

# Get the names
names = all_car_names


# Dataframe and save
dt = {"year":years,"name":names, "price":prices, "mileage": mileage}
date    = datetime.datetime.now().strftime("%Y%m%d")

df = pd.DataFrame.from_dict(dt)
df["company"] = "autotrader"
df["date"]    = date

# Convert the price and mileage to numbers. Empty values will be NaN
df["price"]   = pd.to_numeric(df["price"], errors='coerce')
df["mileage"] = pd.to_numeric(df["mileage"],errors='coerce')


save_dir = "C://Users//27608//Documents//Meliora Technologies//MVP//Car pricing//data//"

# Save all data in data/cars-'date'/
new_dir = "cars-"+date 

# Check if the directory already exists 
if  new_dir in os.listdir(save_dir):
    df.to_csv(save_dir+ new_dir +"//autotrader_"+date+".csv")
else:
    os.mkdir(save_dir+new_dir)    
    df.to_csv(save_dir+ new_dir +"//autotrader_"+date+".csv")



#df.to_csv(save_dir+"autotrader_"+date+".csv")
