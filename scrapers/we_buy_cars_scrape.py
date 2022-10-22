# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 09:33:01 2021

@author: Car Pricing Team
"""



from selenium import webdriver
import time
import random
import re
import pandas as pd
import datetime 
import os



CHROMEDRIVER_DIR = "C:/Users/27608/Documents/Chrome Drivers/chromedriver"


driver = webdriver.Chrome(executable_path=CHROMEDRIVER_DIR)

#driver.get("https://www.webuycars.co.za/buy-a-car")


all_car_names   = []
all_car_prices  = []
all_car_mileage = []
price_mileage   = []

# This number comes from looking at the https://www.webuycars.co.za/buy-a-car page
pages = 192

for page in range(1,pages+1):
    
    
    if page == 1:
      driver.get("https://www.webuycars.co.za/buy-a-car")
    else:
        link = "https://www.webuycars.co.za/buy-a-car?page="+str(page)
        driver.get(link)
            
    time.sleep(8)
    
    # Get the car names
    car_names = driver.find_elements_by_class_name("result-item-title")
    
    # Get the car prices and mileage
    car_body  = driver.find_elements_by_class_name("result-item-body")
    
    #print("Page "+str(page)+ " got " + str(len(car_body)) + " results")
    
    if len(car_body) == len(car_names):
    
        for car_name, item in zip(car_names,car_body):
            
            result = item.text
            name  = car_name.find_element_by_tag_name('a').text
            try:
             
             price_mileage.append(result)
             all_car_names.append(name)
            except:
                print("There was an error with: " + name)

    time.sleep(random.randint(5,10))
    
    
driver.close()


# Clean the results
#len(all_car_names) == len(price_mileage)

# Get the prices
p = re.compile("R\d+\s\d+")

for x in price_mileage:
    ans = p.findall(x)
    if len(ans) == 0:
        all_car_prices.append("")
    else:
        all_car_prices.append(ans[0])
      
clean_prices = [prices.replace(" ","").replace("R","")  for prices in all_car_prices]

        
# Get the mileage
m = re.compile("\d+\s\d+\skm")
        
for x in price_mileage:
    ans = m.findall(x)
    if len(ans) == 0:
        all_car_mileage.append("")
    else:
        all_car_mileage.append(ans[0])

clean_mileages = [mileage.replace(" ","").replace("km","")  for mileage in all_car_mileage]


# Get the years
years = []
n = re.compile("\d{4}")
n.findall(all_car_names[0])

for x in all_car_names:
    ans = n.findall(x)
    
    if len(ans) == 0:
        years.append("")
    else:
        years.append(ans[0])



# Save the results
dt = {"year":years,"name":all_car_names, "price":clean_prices, "mileage": clean_mileages}
date    = datetime.datetime.now().strftime("%Y%m%d")


df = pd.DataFrame.from_dict(dt)
df["company"] = "webuycars"
df["date"]    = date

# Convert the price and mileage to numbers. Empty values will be NaN
df["price"]   = pd.to_numeric(df["price"], errors='coerce')
df["mileage"] = pd.to_numeric(df["mileage"],errors='coerce')

# Remove the year model in the names
df["name"] = df["name"].str.replace("^\d{4}","").str.strip()

save_dir = "data//"

# Save all data in data/cars-'date'/

new_dir = "cars-"+date 

# Check if the directory already exists 
if  new_dir in os.listdir(save_dir):
    df.to_csv(save_dir+ new_dir +"//webuycars_"+date+".csv")
else:
    os.mkdir(save_dir+new_dir)    
    df.to_csv(save_dir+ new_dir +"//webuycars_"+date+".csv")
    

