import pandas as pd
import os
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
import sys
import csv,sys
from functools import reduce
import operator
import sys
from sklearn.model_selection import *
from sklearn.svm import *
from sklearn import *
import warnings
import pdb
if not sys.warnoptions:
    warnings.simplefilter("ignore")

def trn_data_triples(df):
    X=df.drop(['true_value',], axis=1)
    y=df.true_value
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

    trn_data=pd.DataFrame({
        'X_train':[X_train],
        'X_test':[X_test],
        'y_train':[y_train],
        'y_test':[y_test],
    })
    return trn_data

def train_model(X_train, X_test, y_train, y_test, model, result_df):
    model=model.fit(X_train, y_train)
    mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
    tmpdf=pd.DataFrame({'method_name': [mdl_name], 
                        'method': [model], 
                        'accuracy':[model.score(X_test, y_test)], 
                        'auc_roc':[roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])]})
    result_df=pd.concat([result_df, tmpdf])
    return result_df


def train_on_all_data(df, model):    
    X=df.drop(['true_value',], axis=1)
    y=df.true_value

    model=model.fit(X, y)
    print(f'All data train roc_auc_score of {model.__class__.__name__}: ', roc_auc_score(y, model.predict_proba(X)[:, 1]),)
    return model



def main(df, models_list, output_path):
    result_df=pd.DataFrame()    
    
    for model in models_list:
        trn_data = trn_data_triples(df)
        result_df=train_model(trn_data.X_train.item(), 
                              trn_data.X_test.item(), 
                              trn_data.y_train.item(), 
                              trn_data.y_test.item(), 
                              model, 
                              result_df)
    result_df=result_df.reset_index(drop=True) 

    print(result_df)   
    print(result_df.auc_roc.idxmax())
    
    best_method=result_df.loc[result_df.auc_roc.idxmax()]
    
    print(f'''
        Best Model: {best_method.method_name}
        Auc_Roc:    {best_method.auc_roc}
        Accuracy:   {best_method.accuracy}

    '''
    )

    final_model = train_on_all_data(df, best_method.method)

    Path(output_path).mkdir(parents=True, exist_ok=True)    
    
    with open(f'{output_path}/classifier.pkl','wb') as fp: pickle.dump(final_model,fp)
    return result_df


def train_global_model(df):
    models_list=[
        AdaBoostClassifier(),
        LogisticRegression(random_state=0),
        GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),
        RandomForestClassifier(n_estimators=50,oob_score = True),
        StackingClassifier(estimators=[('dt',DecisionTreeClassifier()), ('rf',RandomForestClassifier(random_state=0))], final_estimator=GradientBoostingClassifier(random_state=0)),
        DecisionTreeClassifier(), BaggingClassifier(DecisionTreeClassifier(), max_samples=0.5, max_features = 1.0, n_estimators =50), 
        make_pipeline(StandardScaler(), SVC(gamma='auto', probability=True))
    ]
    
    
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


if __name__=="__main__":
    
    output_path = "models/"
    
    # model_df = pd.read_csv(sys.argv[2])
    # models_list=model_df['model_lists'].to_list()
    print('path: ', sys.argv[1])

    df = pd.read_csv(sys.argv[1])
    
    train_global_model(df) 