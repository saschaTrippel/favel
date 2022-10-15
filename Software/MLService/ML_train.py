import pandas as pd
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import *
from sklearn.ensemble import *
from sklearn.tree import *
import pandas as pd
import numpy as np
from sklearn.naive_bayes import *
from sklearn.neighbors import *
import pickle, sklearn
from sklearn.neural_network import *
from pathlib import Path
from sklearn.metrics import *
from sklearn.pipeline import *
from sklearn.preprocessing import *
from joblib import dump, load
import pickle
import csv,sys
from functools import reduce
import operator
import sys
from sklearn.model_selection import *
from sklearn.svm import *
from sklearn import *
import pdb
import os, sys, warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")




# def trn_data_triples(df):
#     X=df.drop(['true_value',], axis=1)
#     y=df.true_value
#     # X_train, X_test, y_train, y_test = train_test_split(
#     # X, y, test_size=0.33, random_state=42)

#     trn_data=pd.DataFrame({
#         'X_train':[X_train],
#         # 'X_test':[X_test],
#         'y_train':[y_train],
#         # 'y_test':[y_test],
#     })
#     return trn_data

# def train_model(X_train, X_test, y_train, y_test, model, result_df):
# def train_model(X_train, y_train, model, result_df):

#     model=model.fit(X_train, y_train)
#     mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__

#     tmpdf=pd.DataFrame({'method_name': [mdl_name], 
#                         'method': [model], 
#                         'accuracy':[model.score(X_train, y_train)], 
#                         'auc_roc':[roc_auc_score(y_train, model.predict_proba(X_train)[:, 1])]})
#     result_df=pd.concat([result_df, tmpdf])
#     return result_df




# def train_on_all_data(df, model):    
#     X=df.drop(['true_value',], axis=1)
#     y=df.true_value

#     model=model.fit(X, y)
#     print(f'All data train roc_auc_score of {model.__class__.__name__}: ', roc_auc_score(y, model.predict_proba(X)[:, 1]),)
#     return model

def train_model(X, y, model):
    model=model.fit(X, y)
    mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
    roc_auc = roc_auc_score(y, model.predict_proba(X)[:, 1])

    return mdl_name, roc_auc

# Change model list here to be a single model
def train(df, ml_model, output_path):
    le = preprocessing.LabelEncoder()
    le.fit(df['predicate'])
    df['predicate']=le.transform(df['predicate'])

    X=df.drop(['true_value', 'subject', 'object'], axis=1)
    y=df.true_value

    model_name, roc_auc = train_model(X, y, ml_model)
    with open(f'{output_path}/results.txt', 'w') as f:
        f.write(f'''
            TRAIN RESULT:
            model name: {model_name}
            roc auc score: {roc_auc}
        ''')

    with open(f'{output_path}/classifier.pkl','wb') as fp: pickle.dump(model,fp)
    with open(f'{output_path}/predicate_le.pkl','wb') as fp: pickle.dump(le,fp)

    return True


def test(df, output_path):
    # read saved model
    with open(f'{output_path}/classifier.pkl','wb') as fp: ml_model = pickle.load(fp)

    # read predicate label encoder
    with open(f'{output_path}/predicate_le.pkl','wb') as fp: le_predicate = pickle.load(fp)


    X=df.drop(['true_value','subject', 'object'], axis=1)
    y=df.true_value

    # predict on test df
    ensembleScore = []
    X['predicate'] = X['predicate'].map(lambda s: '<unknown>' if s not in le_predicate.classes_ else s)
    le_predicate.classes_ = np.append(le_predicate.classes_, '<unknown>')
    X.predicate = le_predicate.transform(X.predicate)
    X = df.drop(['subject','object'], axis=1)
    ensembleScore = ml_model.predict(X)
    
    df['ensemble_score'] = ensembleScore

    roc_auc = roc_auc_score(y, ensembleScore)

    with open(f'{output_path}/results.txt', 'a') as f:
        f.write(f'''
            TEST RESULT:
            roc auc score: {roc_auc}
        ''')

    return df



'''
def train(df):

    output_path = "models/"

    # The chosen model
    models_list=[
        LogisticRegression(random_state=0),
    ]
    
    
    # print('path: ', sys.argv[1])

    # df = pd.read_csv(sys.argv[1])
    
    df.fillna(0, inplace=True)

    # remove triples here
    if sum(df.columns.str.contains('subject', case=False)): df=df.drop(['subject',], axis=1)
    #if sum(df.columns.str.contains('predicate', case=False)): df=df.drop(['predicate',], axis=1)
    if sum(df.columns.str.contains('object', case=False)): df=df.drop(['object',], axis=1)
    print(df.shape)
    print(df.head())

    le = preprocessing.LabelEncoder()
    le.fit(df['predicate'])
    df['predicate']=le.transform(df['predicate'])
    filehandler = open("models/le_predicate.obj","wb")
    pickle.dump(le,filehandler)
    filehandler.close()
    #print(df)
    
    main(df, models_list, output_path)     
'''

# if __name__=="__main__":
    
#     output_path = "models/"
    
    # model_df = pd.read_csv(sys.argv[2])
    # models_list=model_df['model_lists'].to_list()
    
    # train_global_model(df) 


# 1. dont split in main function
# 2. in train_model() calculate acc on train data
# 3. write function for test data
# 4. export model and label_encoding of predicates to output_path folder
