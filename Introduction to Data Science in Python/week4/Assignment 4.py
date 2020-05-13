
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


#
#CREATED FUNCTIONS FOR ASSIGNMENT
#
def get_gdp():
    gd= pd.read_excel('gdplev.xls','Sheet1',skiprows =5)
    df =gd[['Unnamed: 4','GDP in billions of chained 2009 dollars.1']]
    df.rename(columns ={'Unnamed: 4':'Quarter','GDP in billions of chained 2009 dollars.1':'Gdp'},inplace =True)
    # Finding the index
    index = df[df['Quarter']=='2000q1'].index.values
    new_df =df[index[0]:]
    new_df =new_df.reset_index()
    new_df = new_df[['Quarter','Gdp']]
    new_df['shift'] =new_df['Gdp'].shift(1)
    new_df['GDP change'] = new_df['Gdp'] - new_df['shift']
    change =[np.NaN]
    length = new_df['Quarter'].size
    for count in range(length-1):
        if new_df.iloc[count]['Gdp'] < new_df.iloc[count + 1]['Gdp'] :
            change.append('increase')
        if new_df.iloc[count]['Gdp'] > new_df.iloc[count + 1]['Gdp'] :
            change.append('decline')
        
    new_df['change'] = change
    return new_df


def housing_data():
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    # Use this dictionary to map state names to two letter acronyms
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    housing['State'] = housing['State'].map(states)
    housing.set_index(['State','RegionName'],inplace =True)
    m =housing.columns.get_loc('2000-01')
    housing = housing[housing.columns[m:]] .rename(columns =pd.to_datetime)
    return housing

    


# In[4]:


import pandas as pd
import numpy as np

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    
    df = pd.read_csv('university_towns.txt',delimiter ='\n',header = None)
    df = df.rename(columns={0:'State'})
    lst =[]
    state=''
    region=''
    for line in df.State:
        if '[ed' in line:
            state = line.split(sep ='[ed')[0]
        else:
            region = line.split(sep =' (')[0].strip()
            lst.append([state,region])
    answer1 = pd.DataFrame(lst,columns=['State','RegionName'])
    
    return answer1

get_list_of_university_towns()


# In[5]:


import pandas as pd
import numpy as np
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    new_df = get_gdp()
    #Recession
    length = np.linspace(1,60,60,dtype =int)
    for i in length:
        if new_df.iloc[i]['GDP change'] > new_df.iloc[i+1]['GDP change'] > new_df.iloc[i+2]['GDP change'] < new_df.iloc[i+3]['GDP change']  < new_df.iloc[i+4]['GDP change']:
            recesion_start = new_df.iloc[i+1]['Quarter']  
    return recesion_start
get_recession_start()


# In[6]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df =get_gdp()
    quarter = get_recession_start()
    Index_label = df[df['Quarter'] == quarter].index.tolist()
    start_index = Index_label[0]
    
    
    recession_end_df = df[start_index:]
    recession_end_df = recession_end_df .reset_index()
    recession_end_df = recession_end_df[['Quarter','change']]
    L = recession_end_df['change'].size
    length = np.linspace(1,L-1,L-1,dtype=int)
    m=[]
    for i in length:
        if recession_end_df.iloc[i]['change'] == 'increase':
            m.append((i))
            
    end = recession_end_df.iloc[m[1]]['Quarter']
              
    return end
get_recession_end()


# In[7]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    df =get_gdp()
    quarter = get_recession_start()
    Index_label = df[df['Quarter'] == quarter].index.tolist()
    start_index = Index_label[0]
    
    
    recession_end_df = df[start_index:]
    recession_end_df = recession_end_df .reset_index()
    recession_end_df = recession_end_df[['Quarter','change']]
    L = recession_end_df['change'].size
    length = np.linspace(1,L-1,L-1,dtype=int)
    m=[]
    for i in length:
        if recession_end_df.iloc[i]['change'] == 'decline':
            m.append((i))
        else:
            break
            
    end_bottom = recession_end_df.iloc[m[-1]]['Quarter']

    return end_bottom
get_recession_bottom()


# In[8]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    
    '''
    data = housing_data()
    data =data.resample('Q',axis =1).mean()
    data = data.rename(columns=lambda x: str(x.to_period('Q')).lower())
    

    
    return data
convert_housing_data_to_quarters()


# In[83]:


from scipy import stats
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    hdf = convert_housing_data_to_quarters()
    rec_start=get_recession_start()
    rec_bottom = get_recession_bottom()
    ul = get_list_of_university_towns()
    
    # Getting the column index for start and bottom
    qbs = (hdf.columns.get_loc(rec_start)) -1
    rb = hdf.columns.get_loc(rec_bottom)

    hdf['PriceRatio']= hdf[hdf.columns[qbs]].div(hdf[hdf.columns[rb]])
    
    df = pd.merge(hdf.reset_index(),ul,how='outer',on= ul.columns.tolist(),indicator ='_flag')
    group1 = df[df['_flag'] == 'both']
    group2 = df[df['_flag'] != 'both']
    
    stats.ttest_ind(group1['PriceRatio'],group2['PriceRatio'])
#     different = pvalue <0.01
#     better = group1['Price ratio'].mean() < group2['Price ratio']
    
    t,p = stats.ttest_ind(group1['PriceRatio'].dropna(), group2['PriceRatio'].dropna())
    
    different = True if p<0.01 else False
    better = "university town" if group1['PriceRatio'].mean() < group2['PriceRatio'].mean() else "non-university town"
    
    
    
    
    return (different,p,better)

run_ttest()

