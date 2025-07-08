import pandas as pd
import numpy as np
import io
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from supabase import create_client, Client
from dotenv import load_dotenv
featurenames = ['Price','Numofreviews','sellerRating','Platform','Proof','Justification']




#print (response.data)
def replicamodel(data,userinput):
    thedata = pd.read_csv(io.StringIO(data))
    thedata['Proof'] = thedata['Proof'].map(lambda x: 1 if x == 'Yes' else 0)
    thedata['Justification'] = thedata['Justification'].map(lambda x: 1 if x == 'Yes' else 0)
    thedata['LikelyToBeAuthentic'] = thedata['LikelyToBeAuthentic'].map(lambda x: 1 if x == 'Yes' else 0)
    #The columns are categorical, so we binary encode them to 1s and 0s for the model to understand
    platformsencode ={
    'Vinted': 0,
    'Depop': 1,
    'Ebay': 2
    }
    #These platforms are categorical. The model will not understood the categorical data, so we convert it into numerical form so it's easier to understand.
    thedata['Platform'] = thedata['Platform'].map(platformsencode)


#pd.set_option('display.max_rows',None)
#print(thedata)

    thedata = thedata.drop(columns = ['ListingID','ItemID'], axis =1)

    #These columns are not useful for the model, so we drop them 

    x = thedata.drop("LikelyToBeAuthentic", axis = 1)
    y = thedata['LikelyToBeAuthentic']

    #Here we are splitting the data into features and label.
    #Features are the columns use to predict the label
    #The label is the column we are looking to predict

    x_train, x_test, y_train, y_test = train_test_split(x,y,random_state = 42,test_size = 0.2)
    #We split the data into training and test sets. This will allow us to train the model.
   

    rf = RandomForestClassifier(n_estimators=100, random_state = 42, class_weight='balanced_subsample')
    rf.fit(x_train, y_train)
    #Random forest classifier is fit into the training set

    result = rf.predict(userinput)


    resultvalue = result[0]

    if resultvalue == 1:
        authentic = "Good news! <br> <br> This item is likely to be authentic"
    else:
        authentic = "Sorry To Break It To You! <br> <br> This item is not likely to be authentic"




    return authentic

   #This is a machine learning model that predicts whether an item in an online marketplace is likely to be authentic or not

