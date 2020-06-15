
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[1]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[2]:

## PART 1
def get_Dataframe():
    df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
    #Converting the date column to date time column
    df['Date'] = pd.to_datetime(df['Date'])
    #Sorting the Dates
    df.sort_values('Date',inplace =True)
    # reset and getting rid of column index -unnecessary
    df = df.reset_index()
    df =df.drop(['index'],axis =1)
    return df


# In[3]:

## PART 2 -Seperating in to Tmin and Tmax 2005 -2014
def get_maxmin():
    df =get_Dataframe()
    tmin = (df[df['Element'] =='TMIN']).reset_index().drop(['index'],axis=1)
    tmax =df[df['Element'] =='TMAX'].reset_index().drop(['index'],axis =1)
    
    # Taking MIN AND MAX OF 2015 values
    tmin_15 = tmin[(tmin['Date'] >= '2015')].reset_index().drop(['index'],axis=1)
    tmax_15 = tmax[(tmax['Date'] >= '2015')].reset_index().drop(['index'],axis=1)
    # *Need to find better way to remove leap years*
    # MAX AND MIN EACH DAY FROM 2005 -2014
    tmin = tmin[(tmin['Date'] < '2015') & (tmin['Date'] != '2008-02-29') &(tmin['Date'] != '2012-02-29')].reset_index().drop(['index'],axis=1)
    tmax = tmax[(tmax['Date'] < '2015') & (tmax['Date'] != '2008-02-29') &(tmax['Date'] != '2012-02-29')].reset_index().drop(['index'],axis=1)
    tmin.Data_Value = tmin.Data_Value /10
    tmax.Data_Value = tmax.Data_Value /10
    tmin_15.Data_Value = tmin_15.Data_Value /10
    tmax_15.Data_Value = tmax_15.Data_Value /10
    return tmin,tmax,tmin_15,tmax_15
tmin,tmax,tmin_15,tmax_15 =get_maxmin()


# In[4]:

# Replacing all the year values in (2005 -2014) as 2015
# andthengrouping data together by days to calculate minimum and maximum temperatures for next 10 years
year_min =[]
year_max=[]
for i in range(len(tmin)):
    year_min.append(tmin.Date[i].replace(year=2015))
for i in range(len(tmax)):
    year_max.append(tmax.Date[i].replace(year=2015))
tmin['Date'] =year_min
tmax['Date'] =year_max
## PART 3 - grouping data together each day for next 10 years
dict_min ={}
dict_max ={}
dict_15min ={}
dict_15max ={}
p = tmin.groupby(['Date'])
q = tmax.groupby(['Date'])
r = tmin_15.groupby(['Date'])
s = tmax_15.groupby(['Date'])
# Creating dictionaries (key,value pairs) from data frame
# Do we need this step?
for i,frame in p:
    dict_min.update([(i,frame['Data_Value'].min())])
for i,frame in q:
    dict_max.update([(i,frame['Data_Value'].max())])  
    
for i,frame in r:
    dict_15min.update([(i,frame['Data_Value'].max())])  
for i,frame in s:
    dict_15max.update([(i,frame['Data_Value'].max())])  
    
list1 =[]
list2 =[]
for key,value in dict_min.items():
    list1.append(value)
for key,value in dict_max.items():
    list2.append(value)   
    

    
    
#    
# Plotting After getting all the required data
#    
    
get_ipython().magic('matplotlib notebook')
import numpy as np
import matplotlib.pyplot as plt
B = np.array(list1)
A = np.array(list2)
plt.figure()
plt.plot(A,'-r',linewidth=0.2,label ='record highs for 2005-2014')
plt.plot(B,'-b',linewidth=0.2,label ='record lows for 2005-2014')
plt.gca().fill_between(range(len(list1)), A, B, facecolor='blue', alpha=0.25)
plt.title('Record highs and lows (2005 -2014) vs 2015')

A = pd.DataFrame.from_dict(dict_min, orient='index').rename(columns={0:'data_min'})
B = pd.DataFrame.from_dict(dict_15min, orient='index').rename(columns={0:'min_15'})
C = pd.DataFrame.from_dict(dict_max, orient='index').rename(columns={0:'data_max'})
D = pd.DataFrame.from_dict(dict_15max, orient='index').rename(columns={0:'max_15'})
merge1 = pd.merge(A,B,how = 'inner',left_index =True,right_index =True)
merge2 = pd.merge(C,D,how = 'inner',left_index =True,right_index =True)

merge1['Truth'] = merge1['data_min'] > merge1['min_15']
merge2['Truth'] = merge2['data_max'] < merge2['max_15']
merge1.reset_index(inplace =True)
merge2.reset_index(inplace =True)
P =merge1[merge1.Truth == True]
Q =merge2[merge2.Truth == True]

x1 = np.array(P.index)
y1 =np.array(P['min_15'])
plt.scatter(x1,y1,c='b',s=10,label= 'min temp 2015 < (2005 - 2014)')

x2 = np.array(Q.index)
y2 =np.array(Q['max_15'])
plt.scatter(x2,y2,c='r',s=10,label='max temp 2015 > (2005 - 2014)')
plt.xlabel('Number of days (0-365)')
plt.ylabel('Temperature in Celsius($^0$c)')
#Changing the y axis from -45 to 45
plt.axis([0, 365, -45, 45])
plt.legend()
image ='Assignment2.png'
plt.savefig(image)
from IPython.display import HTML
HTML('<a href ="{0}" download>Click here to download {0}</a>'.format(image))

