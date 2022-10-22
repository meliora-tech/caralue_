# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 12:10:43 2021

@author: Car pricing
"""

from selenium import webdriver
import time
import random
import re
import pandas as pd
import datetime
import os

url = "https://motus.cars/shop-cars-for-sale/used-demo"




CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"


driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)

all_car_names   = []
all_car_prices  = []
all_car_mileage = []
all_year_mileage   = []



pages = 479

for page in range(1,pages+1):
    
    
    if page == 1:
      driver.get(url)
    else:
        link = "https://motus.cars/shop-cars-for-sale/used-demo?sort=price&sortdirection=asc&page="+ str(page) +"&pagesize=18&layout=grid"
        driver.get(link)
            
    time.sleep(8)
    
    
    
    
    # Get the car names
    
    all_info = driver.find_elements_by_tag_name("app-vehicle-card") 
    #car_names = driver.find_elements_by_tag_name("app-vehicle-card")[0].find_elements_by_css_selector("div.card > div.card-block > div > div")[3].text
    try:
        for vehicle in all_info:
            name = vehicle.find_elements_by_css_selector("div.card > div.card-block > div > div")[0].text
            price = vehicle.find_elements_by_css_selector("div.card > div.card-block > div > div")[1].text
            year_mileage = vehicle.find_elements_by_css_selector("div.card > div.card-block > div > div")[2].text
        
        
            all_car_names.append(name)
            all_car_prices.append(price)
            all_year_mileage.append(year_mileage)
    except:
        
        print("There was an error scraping " + str(page))

    time.sleep(random.randint(5,10))
    
    
    
driver.close()


#===  Clean the results ===#

# Car prices
prices =  [ line.split("\n")[0].replace("R","").replace(" ","") for line in all_car_prices]

# Car name
names = [ line.replace("\n","") for line in all_car_names]

# Car year
y = re.compile("\d{4}")
years = [ y.findall(line)[0] for line in all_year_mileage]


# Car mileage
m = re.compile("\d+\skm")
mileage = [ m.findall(line)[0].replace(" ","").replace("km","") for line in all_year_mileage]


# Dataframe and save
dt = {"year":years,"name":names, "price":prices, "mileage": mileage}
date    = datetime.datetime.now().strftime("%Y%m%d")

df = pd.DataFrame.from_dict(dt)
df["company"] = "motus"
df["date"]    = date


# Convert the price and mileage to numbers. Empty values will be NaN
df["price"]   = pd.to_numeric(df["price"], errors='coerce')
df["mileage"] = pd.to_numeric(df["mileage"],errors='coerce')

save_dir = "data//"

# Save all data in data/cars-'date'/

new_dir = "cars-"+date 

# Check if the directory already exists 
if  new_dir in os.listdir(save_dir):
    df.to_csv(save_dir+ new_dir +"//motus_"+date+".csv")
else:
    os.mkdir(save_dir+new_dir)    
    df.to_csv(save_dir+ new_dir +"//motus_"+date+".csv")

#df.to_csv(save_dir+"motus_"+date+".csv")