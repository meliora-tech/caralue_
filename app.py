# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 10:52:56 2021

@author: Car pricing
"""


from flask import Flask, flash, jsonify ,render_template, redirect, request, url_for
from forms.forms import CarSearchForm
from utils.utils import summary_statistics
import pymongo
from collections import Counter


client            = pymongo.MongoClient("mongodb+srv://meliora1:5XtcvFVXZQc2bUJ@cluster0.2l3yg.mongodb.net/carsdb?retryWrites=true&w=majority")
db                = client.carsdb
car_collection    = db["cars"]


#car_collection.create_index([("name",pymongo.TEXT)])



app = Flask(__name__)


app.config["SECRET_KEY"] = "oasdfn09nísp"

@app.route("/")
def home():
    form = CarSearchForm()
    
    return render_template("home.html",form=form)


@app.route("/search", methods=["GET","POST"])
def search_term():
   form = CarSearchForm()
   
   if request.method == "POST"  :
       if form.validate_on_submit():
           
           
           term = '\"'+ form.car.data +'\"'
           ans = car_collection.find({ '$text': { '$search': term } })
           
           list_ans = list(ans)
           
           avg, median, all_dict = summary_statistics(list_ans)
           
           return render_template("results.html",avg=avg, median=median, all_dict=all_dict, car_name=form.car.data)
       else:
           
           flash("Submission was not valid. Please try again",'danger')
           return redirect(url_for('home'))
   
    
   term = '\"'+request.args.get("query") +'\"'
   ans = car_collection.find({ '$text': { '$search': term } }).limit(20)
   
   all_names = []
   for a in ans:
       all_names.append(a["name"])

   if len(all_names) > 0:
        counter  = Counter(all_names)       
        all_keys = list(counter.keys())
        
        return jsonify({"ans":all_keys})
        
   return jsonify({"ans":all_names})       
   
   
   















if __name__ == "__main__":
    
    app.run(debug=True,use_reloader=True)
    
