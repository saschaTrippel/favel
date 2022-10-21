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
import logging, argparse, configparser

if not sys.warnoptions: warnings.simplefilter("ignore")

import time
time.ctime() # 'Mon Oct 18 13:35:29 2010'


def loadConfig(experiment):
    configParser = configparser.ConfigParser()
    print('logging path: ', f"./PG/Evaluation/{experiment}/favel.conf", os.getcwd())
    configParser.read(f"./PG/Evaluation/{experiment}/favel.conf")
    return configParser
    
def configureLogging(configParser):
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['warning'] = logging.WARNING
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL

    logging.basicConfig(
        filename='ml_logs.log',
        level=   loggingOptions[configParser['General']['logging']]
    )



def custom_model_train(X, y, model):
    try:
        model=model.fit(X, y)
        mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
        roc_auc = roc_auc_score(y, model.predict_proba(X)[:, 1])

        return model, mdl_name, roc_auc
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print('Error in custom_model_train: ', exc_type, fname, exc_tb.tb_lineno)
        logging.info('Error in custom_model_train: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
        return False, False, False


# Change model list here to be a single model
def train_model(df, ml_model, output_path):
    try:
        le = preprocessing.LabelEncoder()
        le.fit(df['predicate'])
        df['predicate']=le.transform(df['predicate'])

        X=df.drop(['true_value', 'subject', 'object'], axis=1)
        y=df.true_value

        print('TRAIN: ', X.shape, y.shape)

        model, model_name, roc_auc = custom_model_train(X, y, ml_model)

        logging.info('ML model trained')

        if not model and not model_name and not roc_auc: 
            return False
        else:
            with open(f'{output_path}/results.txt', 'w') as f:
                f.write(f'''
                    {time.strftime('%l:%M%p %Z on %b %d, %Y')}
                    TRAIN RESULT:
                    model name: {model_name}
                    roc auc score: {roc_auc}
                ''')

            with open(f'{output_path}/classifier.pkl','wb') as fp:   pickle.dump(model,fp)
            with open(f'{output_path}/predicate_le.pkl','wb') as fp: pickle.dump(le,   fp)

            logging.info('ML model and labelencoder saved in output path')

            return True
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print('Error in train_model: ', exc_type, fname, exc_tb.tb_lineno)
        logging.info('Error in train_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

        return False


def validate_model(df, output_path):
    try:
        # read saved model
        with open(f'{output_path}/classifier.pkl','rb') as fp: ml_model = pickle.load(fp)

        # read predicate label encoder
        with open(f'{output_path}/predicate_le.pkl','rb') as fp: le_predicate = pickle.load(fp)


        X=df.drop(['true_value','subject', 'object'], axis=1)
        y=df.true_value

        # predict on test df
        ensembleScore = []
        X['predicate'] = X['predicate'].map(lambda s: '<unknown>' if s not in le_predicate.classes_ else s)
        le_predicate.classes_ = np.append(le_predicate.classes_, '<unknown>')
        X.predicate = le_predicate.transform(X.predicate)
        # X = df.drop(['subject','object'], axis=1)
        ensembleScore = ml_model.predict(X)
        
        df['ensemble_score'] = ensembleScore

        roc_auc = roc_auc_score(y, ensembleScore)

        logging.info('validation completed')

        with open(f'{output_path}/results.txt', 'a') as f:
            f.write(f'''
                {time.strftime('%l:%M%p %Z on %b %d, %Y')}
                VALIDATION RESULT:
                roc auc score: {roc_auc}
            ''')

        logging.info('validation results written in results file')

        return df

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print('Error in validate_model: ', exc_type, fname, exc_tb.tb_lineno)
        logging.info('Error in validate_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
        
        return False


def test_model(df, output_path):
    try:
        # read saved model
        with open(f'{output_path}/classifier.pkl','rb') as fp: ml_model = pickle.load(fp)

        # read predicate label encoder
        with open(f'{output_path}/predicate_le.pkl','rb') as fp: le_predicate = pickle.load(fp)


        X=df.drop(['true_value','subject', 'object'], axis=1)

        # predict on test df
        ensembleScore = []
        X['predicate'] = X['predicate'].map(lambda s: -1 if s not in le_predicate.classes_ else s)
        le_predicate.classes_ = np.append(le_predicate.classes_, -1)
        X.predicate = le_predicate.transform(X.predicate)
        # X = df.drop(['subject','object'], axis=1)
        ensembleScore = ml_model.predict(X)
        
        df['ensemble_score'] = ensembleScore

        logging.info('predictions done')

        return df

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        # print('Error in test_model: ', exc_type, fname, exc_tb.tb_lineno)
        logging.info('Error in test_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

        return False




