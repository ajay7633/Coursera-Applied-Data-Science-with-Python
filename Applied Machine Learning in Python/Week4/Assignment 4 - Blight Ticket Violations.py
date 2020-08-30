
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-machine-learning/resources/bANLa) course resource._
# 
# ---

# ## Assignment 4 - Understanding and Predicting Property Maintenance Fines
# 
# This assignment is based on a data challenge from the Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)). 
# 
# The Michigan Data Science Team ([MDST](http://midas.umich.edu/mdst/)) and the Michigan Student Symposium for Interdisciplinary Statistical Sciences ([MSSISS](https://sites.lsa.umich.edu/mssiss/)) have partnered with the City of Detroit to help solve one of the most pressing problems facing Detroit - blight. [Blight violations](http://www.detroitmi.gov/How-Do-I/Report/Blight-Complaint-FAQs) are issued by the city to individuals who allow their properties to remain in a deteriorated condition. Every year, the city of Detroit issues millions of dollars in fines to residents and every year, many of these fines remain unpaid. Enforcing unpaid blight fines is a costly and tedious process, so the city wants to know: how can we increase blight ticket compliance?
# 
# The first step in answering this question is understanding when and why a resident might fail to comply with a blight ticket. This is where predictive modeling comes in. For this assignment, your task is to predict whether a given blight ticket will be paid on time.
# 
# All data for this assignment has been provided to us through the [Detroit Open Data Portal](https://data.detroitmi.gov/). **Only the data already included in your Coursera directory can be used for training the model for this assignment.** Nonetheless, we encourage you to look into data from other Detroit datasets to help inform feature creation and model selection. We recommend taking a look at the following related datasets:
# 
# * [Building Permits](https://data.detroitmi.gov/Property-Parcels/Building-Permits/xw2a-a7tf)
# * [Trades Permits](https://data.detroitmi.gov/Property-Parcels/Trades-Permits/635b-dsgv)
# * [Improve Detroit: Submitted Issues](https://data.detroitmi.gov/Government/Improve-Detroit-Submitted-Issues/fwz3-w3yn)
# * [DPD: Citizen Complaints](https://data.detroitmi.gov/Public-Safety/DPD-Citizen-Complaints-2016/kahe-efs3)
# * [Parcel Map](https://data.detroitmi.gov/Property-Parcels/Parcel-Map/fxkw-udwf)
# 
# ___
# 
# We provide you with two data files for use in training and validating your models: train.csv and test.csv. Each row in these two files corresponds to a single blight ticket, and includes information about when, why, and to whom each ticket was issued. The target variable is compliance, which is True if the ticket was paid early, on time, or within one month of the hearing data, False if the ticket was paid after the hearing date or not at all, and Null if the violator was found not responsible. Compliance, as well as a handful of other variables that will not be available at test-time, are only included in train.csv.
# 
# Note: All tickets where the violators were found not responsible are not considered during evaluation. They are included in the training set as an additional source of data for visualization, and to enable unsupervised and semi-supervised approaches. However, they are not included in the test set.
# 
# <br>
# 
# **File descriptions** (Use only this data for training your model!)
# 
#     readonly/train.csv - the training set (all tickets issued 2004-2011)
#     readonly/test.csv - the test set (all tickets issued 2012-2016)
#     readonly/addresses.csv & readonly/latlons.csv - mapping from ticket id to addresses, and from addresses to lat/lon coordinates. 
#      Note: misspelled addresses may be incorrectly geolocated.
# 
# <br>
# 
# **Data fields**
# 
# train.csv & test.csv
# 
#     ticket_id - unique identifier for tickets
#     agency_name - Agency that issued the ticket
#     inspector_name - Name of inspector that issued the ticket
#     violator_name - Name of the person/organization that the ticket was issued to
#     violation_street_number, violation_street_name, violation_zip_code - Address where the violation occurred
#     mailing_address_str_number, mailing_address_str_name, city, state, zip_code, non_us_str_code, country - Mailing address of the violator
#     ticket_issued_date - Date and time the ticket was issued
#     hearing_date - Date and time the violator's hearing was scheduled
#     violation_code, violation_description - Type of violation
#     disposition - Judgment and judgement type
#     fine_amount - Violation fine amount, excluding fees
#     admin_fee - $20 fee assigned to responsible judgments
# state_fee - $10 fee assigned to responsible judgments
#     late_fee - 10% fee assigned to responsible judgments
#     discount_amount - discount applied, if any
#     clean_up_cost - DPW clean-up or graffiti removal cost
#     judgment_amount - Sum of all fines and fees
#     grafitti_status - Flag for graffiti violations
#     
# train.csv only
# 
#     payment_amount - Amount paid, if any
#     payment_date - Date payment was made, if it was received
#     payment_status - Current payment status as of Feb 1 2017
#     balance_due - Fines and fees still owed
#     collection_status - Flag for payments in collections
#     compliance [target variable for prediction] 
#      Null = Not responsible
#      0 = Responsible, non-compliant
#      1 = Responsible, compliant
#     compliance_detail - More information on why each ticket was marked compliant or non-compliant
# 
# 
# ___
# 
# ## Evaluation
# 
# Your predictions will be given as the probability that the corresponding blight ticket will be paid on time.
# 
# The evaluation metric for this assignment is the Area Under the ROC Curve (AUC). 
# 
# Your grade will be based on the AUC score computed for your classifier. A model which with an AUROC of 0.7 passes this assignment, over 0.75 will recieve full points.
# ___
# 
# For this assignment, create a function that trains a model to predict blight ticket compliance in Detroit using `readonly/train.csv`. Using this model, return a series of length 61001 with the data being the probability that each corresponding ticket from `readonly/test.csv` will be paid, and the index being the ticket_id.
# 
# Example:
# 
#     ticket_id
#        284932    0.531842
#        285362    0.401958
#        285361    0.105928
#        285338    0.018572
#                  ...
#        376499    0.208567
#        376500    0.818759
#        369851    0.018528
#        Name: compliance, dtype: float32
#        
# ### Hints
# 
# * Make sure your code is working before submitting it to the autograder.
# 
# * Print out your result to see whether there is anything weird (e.g., all probabilities are the same).
# 
# * Generally the total runtime should be less than 10 mins. You should NOT use Neural Network related classifiers (e.g., MLPClassifier) in this question. 
# 
# * Try to avoid global variables. If you have other functions besides blight_model, you should move those functions inside the scope of blight_model.
# 
# * Refer to the pinned threads in Week 4's discussion forum when there is something you could not figure it out.

# ### Required Libraries

# In[1]:

import pandas as pd
import numpy as np

# Logistic Regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Hyper Parameter Tuning
from sklearn.grid_search import GridSearchCV

# Precision and auc - Imbalanced class
from sklearn.metrics import roc_auc_score


# 1. We only take consider features in the test data columns so all common features are cosidered and rest are dropped & not considered 
# 2. From the Test Data : Some of features from initial consideration are as follows:
#     
#     Numerical Data:
#         1. Judgement amount ( Total Net Amount owed by person)
#         3. Late fee         (If any late fee incurred by the poi - person of interest)
#         4. Fine amount      (Original Amount)
#         P.S: All the fees like(state fees,admin fee etc are dropped cause its standard fee and does not help with prediction)
#     
#     Categorical Data:
#         This can have an impact on the prediction, as the person from a 'certain place' might not consider paying
#         and can have better understanding on prediction , atleast provide understanding if people are paying in certain   locations than others
#         
#         1. City
#         2. State
#         3. Pincode (Yet to decide)
#         4. Disposition
#         
# 3.We try to choose features that dont blow up in to 100s and 1000s of features after creating dummy variables.

# #### PART 1: Loading the data

# In[2]:

def load_data():
    
    train = pd.read_csv('train.csv', encoding="latin1")
    test = pd.read_csv("test.csv")

    print('Length of Training Data ={}'.format(len(train)))
    print('Length of Test Data ={}'.format(len(test)))
    
    return train,test


# #### PART 2: Cleaning up the data
#         1. Removing unwanted rows (NA values) - Training Data ,  Test Data should not have any rows dropped.
#         2. Dropping unnecessary columns that doesnt help with predictions - For Both Test and Training Data.

# In[3]:

def cleaning_data(train,test):
    
    df = train.copy()
    df_test = test.copy()
    df = df[['ticket_id','state','zip_code','disposition','judgment_amount','late_fee','compliance']]
    
    # Among the features we intend to use only disposition ,judgement amout ,late fee(need to be converted to 0 and 1),compliance
    
    # Dropping NA values
    df.dropna(axis = 0,inplace = True)
    
    # Converting compliance to int (0 and 1)
    df['compliance'] = df['compliance'].astype(int)
    
    # Converting late fee in to binary (0 and 1)
    df['late_fee']= df['late_fee'].apply(lambda x : 1 if x > 0 else 0 )
    df_test['late_fee']= df_test['late_fee'].apply(lambda x : 1 if x > 0 else 0 )
    
    
    # Keeping ticket id for final series result
    df_test = df_test[['ticket_id','disposition','judgment_amount','late_fee']]
    
    return df,df_test


# #### PART 3: Creating Dummy variables (if required) and hot encoding categorical data
#         1. We need to hot encode the disposition (it becomes numbered )
#         2. Dont forget to do the same transformation in Test data
#             - We are replacing disposition in to reflect both the Training and Test data
#         3. Ziping up can make it easier to lookup that information (if you want)
#         
#   We are going to consider the following columns for our classifier
#      
#      
#      FOR X:
#      
#      1.(Disposition columns) - after hot encoding -4 columns
#      2. Judgement Amount
#      3. Late fee
#      
#      FOR Y:
#      1. Compliance

# In[4]:

def dummies(df,df_test):
    import pandas as pd
    the_replacement = {'Responsible (Fine Waived) by Deter':'Fine Waived','Responsible (Fine Waived) by Admis':'Fine Waived',
                   'Responsible - Compl/Adj by Default':'Responsible by Default','Responsible - Compl/Adj by Determi':'Responsible by Determination',
                  'Responsible by Dismissal':'Fine Waived'}
    
    # Training data
    df.replace(the_replacement,inplace =True)
    
    # Test Data
    df_test.replace(the_replacement,inplace =True)
    
    
    # Creating Dummies for Training and Test Data
    # Training
    dummies = pd.get_dummies(df['disposition'])
    df2 = pd.concat([df, dummies],axis =1)
    #Test
    dummies = pd.get_dummies(df_test['disposition'])
    df2_test = pd.concat([df_test, dummies],axis =1)
    df2_test.drop(['disposition'],axis =1,inplace =True)
    
    # We get X and y (target) from training dataframe
    # We get the X and y from the cleaned dataframe
    X = df2.drop(['ticket_id','state','zip_code','disposition','compliance'],axis =1)
    y = df2['compliance']
    
    
    
    return X,y,df2_test


# #### PART 4 : Choosing a Classifier and testing the performace of data (HyperParameter Tuning)
#     1. Logistic Regression
#     2. LinearSVM
#     3. Decision Tree
#     4. Random Forest
#     5. Naive Bayes
#     
#     Finding out the best model with the best parameter to give best performace
#     
#     I chose Logistic Regression and calculate auc score, best parameter and score

# In[5]:

def blight_model():
    
    train,test = load_data()
    df,df_test = cleaning_data(train,test)
    X,y,df2_test = dummies(df,df_test)
    
    
    # Logistic Regression
    X_train,X_test,y_train,y_test = train_test_split(X,y,random_state =0)
    LogR = LogisticRegression()
    parameters = {'C':[0.1,1,100]}

    # Create a classifier object with the classifier and parameter candidates
    clf = GridSearchCV(LogR,param_grid = parameters,scoring ='roc_auc')
    clf.fit(X_train,y_train)

    predicted_log = clf.decision_function(X_test)


    print('Test set AUC:',roc_auc_score(y_test,predicted_log))
    print('Best_parameter:',clf.best_params_)
    print('Best score:',clf.best_score_)
    
    ticket_id = df2_test['ticket_id'].tolist()
    df2_test.drop(['ticket_id'],axis =1,inplace =True)
    
    prob_ticket = clf.predict_proba(df2_test)
    data = pd.Series(prob_ticket[:,1])
    result = pd.DataFrame(data)
    result['ticket_id'] =ticket_id
    result = result.set_index('ticket_id')
    
    
    
    return result

blight_model()

