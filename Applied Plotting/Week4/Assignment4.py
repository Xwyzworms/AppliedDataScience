# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 07:47:09 2020

@author: NowYouNotToBlame
"""

# import modules
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib notebook
# Chdir
os.chdir("D:\CourseraCourses\Applied Machine Learning in python\Applied Plotting\Week4")


# Seattle weather

# lINK To Dataset : https://www.kaggle.com/rtatman/did-it-rain-in-seattle-19482017

dfseattle = pd.read_csv("DataSet\seattleWeather_1948-2017.csv") 

# Link To Dataset : On the coursera Applied Plotting course,  data/binnedcsv25/9bc594d0d6bf5fec16beb2afb02a3b859b7d804548c77d614b2a6b9b.csv

dfGlobal = pd.read_csv("DataSet\GlobalOceanWeather.csv")

# Task / Research Question : 

# 1. Compare the average Seattle Weather with global Ocean Weather everyday from 2010 - 2015, what would we get ? 

## Data Manipulation On Seattle

dfseattle.head(n = 10)

dfGlobal.head(n = 10)

#Check DAte type data
print(type(dfseattle["DATE"][0])) # Str 

print(type(dfGlobal["Date"][0])) # str

# Check Date Range

dfseattle["DATE"].tail() # 1948 - 2017

dfGlobal = dfGlobal.sort_values(by= "Date" , ascending = True)
dfGlobal["Date"].tail() # 2005 - 2015

# Manipulate Both dataFrame 

dfseattle.head()
dfseattle["datelogic"] = dfseattle["DATE"].str.contains(pat = "20[1]+[0-9]+" , regex = True)
dfGlobal["datelogic"]  = dfGlobal["Date"].str.contains(pat = "20[1]+[0-9]+" , regex  = True)

dfGlobal = dfGlobal.drop(dfGlobal[dfGlobal["datelogic"] == False ].index)
dfseattle =  dfseattle.drop(dfseattle[dfseattle["datelogic"] == False].index)

dfGlobal["monthday"] = dfGlobal["Date"].str[-5:] # Take only the day 
dfseattle["monthday"] = dfseattle["DATE"].str[-5:]
# Separate The Tmax and tmin values
dfGlobalTmax = dfGlobal[dfGlobal["Element"] == "TMAX"][["Date" , "Data_Value" , "monthday"]]
dfGlobalTmin = dfGlobal[dfGlobal["Element"] == "TMIN"][["Date" , "Data_Value" , "monthday"]]

dfseattleTmax = dfseattle[["DATE" , "TMAX", "monthday"]]
dfseattleTmin = dfseattle[["DATE", "TMIN" , "monthday"]]


dfGlobalMaxi = dfGlobalTmax.groupby(["monthday"])["Data_Value"].aggregate(["max","mean"])
dfGlobalMin  = dfGlobalTmin.groupby(["monthday"])["Data_Value"].aggregate(["min","mean"])

dfseattleMaxi = dfseattleTmax.groupby(["monthday"])["TMAX"].aggregate(["max","mean"]) # Take The Maximize From All over the years
dfseattleMin =  dfseattleTmin.groupby(["monthday"])["TMIN"].aggregate(["min","mean"]) # Same principle Here
dfseattleMin.head()

## Happy Drawing : 
plt.style.use('seaborn-colorblind')
days = range(0,366)
fig,((axes1,axes2,axes3)) = plt.subplots(1,3  ,figsize = (20,8))
# Seattle Plot Max and Min Temp
axes1.plot(days , dfseattleMaxi["mean"] , "-" , c = "black" , label = "SeattleHigh")
axes1.plot(days , dfseattleMin["mean"] , "-" , c = "red" , label = "SeattleLow")
axes1.fill_between(range(len(dfseattleMaxi)),
                        dfseattleMaxi["mean"],dfseattleMin["mean"],
                        alpha = 0.15 , facecolor = "green")

## Global Plot Max and min temp
axes2.plot(days , dfGlobalMaxi["max"] , "-" , c = "blue" , label = "GlobalHigh")
axes2.plot(days , dfGlobalMin["min"] , "-" , c = "green" , label = "GlobalLow")
axes2.fill_between(range(len(dfseattleMaxi)),
                        dfGlobalMaxi["max"] , dfGlobalMin["min"],
                        alpha = 0.15 , facecolor = "red")
## Both Plot
axes3.plot(days , dfseattleMaxi["mean"] , "-" , c = "black" , label = "SeattleHigh")
axes3.plot(days , dfseattleMin["mean"] , "-" , c = "red" , label = "SeattleLow")
## Global Plot Max and min temp
axes3.plot(days , dfGlobalMaxi["max"] , "-" , c = "blue" , label = "GlobalHigh")
axes3.plot(days , dfGlobalMin["min"] , "-" , c = "green" , label = "GlobalLow")



axes3.fill_between(range(len(dfseattleMaxi)),
                        dfseattleMaxi["mean"],dfseattleMin["mean"],
                        alpha = 0.50 , facecolor = "green")
axes3.fill_between(range(len(dfseattleMaxi)),
                        dfGlobalMaxi["max"] , dfGlobalMin["min"],
                        alpha = 0.30 , facecolor = "red")

## LAbelling
axes1.set_title("Average Seattle Temperature ")
axes2.set_title("Global ocean Temperature ")
axes3.set_title("Joined Seattle And Global temperature")

axes1.set_ylabel("Temperature on Farenheit")
axes2.set_ylabel("Temperature on Farenheit")
axes3.set_ylabel("Temperature on Farenheit")

axes1.set_xlabel("Days")
axes2.set_xlabel("Days")
axes3.set_xlabel("Days")

axes1.legend()
axes2.legend()
axes3.legend()
#fig.savefig("Answer.png")
#axes2.set_xticks(months)
#axes3.set_xticks(thirtyday)

# Conclusion : 
print("From These Information we know that Seattle Have Normal Average Temperature for the past 5 years ,\
around roughly 35 farenheit to  < 100 Farenheit compare with global Temperature")

## 

