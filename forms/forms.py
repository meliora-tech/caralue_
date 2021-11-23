# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:32:26 2021

@author: 27608
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, StringField




class CarSearchForm(FlaskForm):
    
    car = StringField('car')
   # year = IntegerField('year')
   # mileage = IntegerField('mileage')
    submit = SubmitField('Submit')