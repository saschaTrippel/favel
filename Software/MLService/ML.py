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
from pathlib import Path
if not sys.warnoptions: warnings.simplefilter("ignore")

import time
time.ctime() # 'Mon Oct 18 13:35:29 2010'

class ML:

    def __init__(self, log_file):
        logging.basicConfig(
            filename=log_file,
            filemode='a',
            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
            datefmt='%H:%M:%S',
            level=logging.INFO
        )


    def createDataFrame(self,assertionScores,approaches):
        try:
            """
            To create the DataFrame that consists of triples and scores from each approach for that particular triple.
            """
            result = dict()
            result['subject'] = []
            result['predicate'] = []
            result['object'] = []

            for assertionScore in assertionScores:
                result['subject'].append(assertionScore.subject)
                result['predicate'].append(assertionScore.predicate)
                result['object'].append(assertionScore.object)

                for approach in approaches.keys():
                    try:
                        if str(approach) in result:
                            result[str(approach)].append(assertionScore.score[str(approach)])
                        else:
                            result[str(approach)] = [assertionScore.score[str(approach)]]
                    except KeyError as ex:
                        pass

            df = pd.DataFrame(result)
            
            return(df)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in createDataFrame: ', exc_type, fname, exc_tb.tb_lineno)
            logging.info('Error in createDataFrame: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            return False


    def get_model_name(self, model):
        mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
        return mdl_name

    def custom_model_train(self,X, y, model):
        try:
            model=model.fit(X, y)
            mdl_name=get_model_name(model)
            roc_auc = roc_auc_score(y, model.predict_proba(X)[:, 1])

            return model, mdl_name, roc_auc
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in custom_model_train: ', exc_type, fname, exc_tb.tb_lineno)
            logging.info('Error in custom_model_train: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            return False, False, False


    # Change model list here to be a single model
    def train_model(self, df, ml_model, output_path):
        try:
            le = preprocessing.LabelEncoder()
            le.fit(df['predicate'])
            df['predicate']=le.transform(df['predicate'])

            X=df.drop(['true_value', 'subject', 'object'], axis=1)
            y=df.true_value

            print('TRAIN: ', X.shape, y.shape, ml_model)

            trained_model, model_name, roc_auc = self.custom_model_train(X, y, ml_model)

            logging.info('ML model trained')

            if not trained_model and not model_name and not roc_auc: 
                return False
            else:
                with open(f'{output_path}/results.txt', 'w') as f:
                    f.write(
                        f'''
                        {time.strftime('%l:%M%p %Z on %b %d, %Y')}
                        TRAIN RESULT:
                        model name: {model_name}
                        roc auc score: {roc_auc}
                        ''')

                with open(f'{output_path}/classifier.pkl','wb') as fp:   pickle.dump(trained_model,fp)
                with open(f'{output_path}/predicate_le.pkl','wb') as fp: pickle.dump(le,   fp)

                logging.info('ML model and labelencoder saved in output path')

                return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in train_model: ', exc_type, fname, exc_tb.tb_lineno)
            logging.info('Error in train_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

            return False


    def validate_model(self, df, output_path, dataset_path):
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
                f.write(
                    f'''
                    {time.strftime('%l:%M%p %Z on %b %d, %Y')}
                    VALIDATION RESULT:
                    roc auc score: {roc_auc}
                    ''')

            # Dataset Folder Name | ML Model Name | Accuracy | Eval Folder | Model Path 

            evaluation_path = Path(output_path).parent
            print('>>>> ', evaluation_path)

            Path(f'{evaluation_path}/ML_Results').mkdir(parents=True, exist_ok=True)
            new_result = pd.DataFrame({
                    'dataset_path': [dataset_path],
                    'ml_model_name': [self.get_model_name(ml_model)],
                    'roc_auc': [roc_auc],
                    'experiment_folder': [output_path]
            })
            try:
                ml_result = pd.read_excel(f"{evaluation_path}/ml_results.xlsx")
                ml_result=pd.concat([ml_result, new_result])
            except:
                ml_result=new_result.copy()
            ml_result.to_excel(f'{evaluation_path}/ML_Results/ml_results.xlsx')

            logging.info('validation results written in results file')

            return df

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in validate_model: ', exc_type, fname, exc_tb.tb_lineno)
            logging.info('Error in validate_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            
            return False


    def test_model(self, df, output_path):
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





