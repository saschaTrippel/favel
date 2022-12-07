import pandas as pd
from sklearn import preprocessing
from sklearn import metrics
from sklearn.linear_model import *
from sklearn.ensemble import *
from sklearn.tree import *
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
import csv,sys, ast
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
import statistics
from sklearn.metrics import classification_report
from skopt import BayesSearchCV
from skopt.space import Real, Categorical, Integer
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


    def createDataFrame(self, assertions):
        try:
            """
            To create the DataFrame that consists of triples and scores from each approach for that particular triple.
            """
            result = dict()
            result['subject'] = []
            result['predicate'] = []
            result['object'] = []
            result['truth'] = []
            
            approaches = assertions[0].score.keys()

            for assertion in assertions:
                result['subject'].append(assertion.subject)
                result['predicate'].append(assertion.predicate)
                result['object'].append(assertion.object)
                result['truth'].append(assertion.expectedScore)
                
                for approach in approaches:
                    if not approach in result:
                        result[approach] = []
                    result[approach].append(assertion.score[approach])

            df = pd.DataFrame(result)
            
            return(df)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in createDataFrame: ', exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in createDataFrame: ' +' '+ str(e) + ' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            return False


    def get_model_name(self, model):
        mdl_name=model.__class__.__name__ if model.__class__.__name__!='Pipeline' else model[1].__class__.__name__
        return mdl_name


    def search_best_params(self,model, ml_model_params, X, y):
        params_range_dict={}
        for x in ml_model_params:
            if type(x['range'])==tuple:
                if type(x['range'][0]) == int: 
                    params_range_dict[x['name']] = Integer(x['range'][0], x['range'][1])
                elif type(x['range'][0]) == float: 
                    params_range_dict[x['name']] = Real(x['range'][0], x['range'][1])
            elif type(x['range']) == list:
                params_range_dict[x['name']] = Categorical(x['range'])

        opt = BayesSearchCV(
                    model,
                    params_range_dict,
                    n_iter=5,
                    random_state=0
                )
        _ = opt.fit(X, y)
        best_params=dict(opt.best_params_)
        return best_params

    def get_sklearn_model(self, model_name, ml_model_params, train_data):
        X=train_data.drop(['subject', 'predicate', 'object', 'truth'], axis=1)
        y=train_data.truth

        xdf=pd.DataFrame(sklearn.utils.all_estimators())
        model = xdf[xdf[0]==model_name][1].item()

        if ml_model_params == 'default':
            model=model()

        elif type(ast.literal_eval(ml_model_params)) == dict:
            model=model()
            ml_model_params=ast.literal_eval(ml_model_params)
            model.set_params(**ml_model_params)

        elif type(ast.literal_eval(ml_model_params)) == list:
            ml_model_params=ast.literal_eval(ml_model_params)
            model=model()
            best_params=self.search_best_params(model, ml_model_params, X, y) # skopt
            model.set_params(**best_params)

        return model


    def custom_model_train(self,X, y, model):
        try:
            model=model.fit(X, y)
            mdl_name=self.get_model_name(model)
            # y_pred=model.predict_proba(X)[:, 1]
            y_pred=model.predict(X)

            roc_auc = roc_auc_score(y, y_pred)

            report_df = pd.DataFrame(classification_report(np.array(y, dtype=int), np.array(y_pred, dtype=int), output_dict=True)).T.reset_index(drop=False).rename(columns={'index': 'label'})
            # print('>>>>> trn acc: ', sum(np.array(y, dtype=int)==np.array(y_pred, dtype=int))/ len(y), roc_auc)

            return model, mdl_name, roc_auc, report_df
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in custom_model_train: ' +' '+str(e)+' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

            return False, False, False, False


    def custom_model_train_cv(self, X, y, model):
        try:
            skfold=StratifiedKFold(n_splits=5)
            scores=cross_val_score(model, X, y,cv=skfold, scoring="roc_auc")
            # roc_auc_cv = np.mean(scores)

            mdl_name=self.get_model_name(model)

            return scores
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            logging.error('Error in custom_model_train_cv: '+' '+str(e) +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            return False, False, False



    
    # Change model list here to be a single model
    def train_model(self, df, ml_model, output_path, dataset_path):
        """
        Returns:
            - Model
            - Predicate lable encoder
            - Training AUC-ROC score
        """
        try:
            le = preprocessing.LabelEncoder()
            le.fit(df['predicate'])
            df['predicate']=le.transform(np.array(df['predicate'].astype(str), dtype=object))

            X=df.drop(['truth', 'subject', 'object'], axis=1)
            y=df.truth

            print('TRAIN: ', X.shape, y.shape, ml_model, y.dtypes)

            roc_auc_cv_scores = self.custom_model_train_cv(X, y, ml_model)

            trained_model, model_name, roc_auc_overall_score, report_df = self.custom_model_train(X, y, ml_model)
            metrics = {"overall": roc_auc_overall_score, "cv_mean": np.mean(roc_auc_cv_scores), "cv_std": round(statistics.stdev(roc_auc_cv_scores), 2)}

            logging.info('ML model trained')


            if trained_model==False and model_name==False and roc_auc_overall_score==False: 
                return False
            else:
                report_df.to_excel(f'{output_path}/Classifcation Report.xlsx', index=False)

                with open(f'{output_path}/classifier.pkl','wb') as fp:   pickle.dump(trained_model,fp)
                with open(f'{output_path}/predicate_le.pkl','wb') as fp: pickle.dump(le,   fp)

                logging.info('ML model and labelencoder saved in output path')

                return trained_model, le, metrics
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('Error in train_model: ', ex, exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in train_model: ' +' '+str(ex)+' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

            raise ex


    def validate_model(self, df, output_path, dataset_path):
        try:
            
            # read saved model
            with open(f'{output_path}/classifier.pkl','rb') as fp: ml_model = pickle.load(fp)

            # read predicate label encoder
            with open(f'{output_path}/predicate_le.pkl','rb') as fp: le_predicate = pickle.load(fp)


            X=df.drop(['truth','subject', 'object'], axis=1)
            y=df.truth

            # predict on test df
            ensembleScore = []

            X['predicate'] = X['predicate'].map(lambda s: '-1' if s not in le_predicate.classes_ else s)
            le_predicate.classes_ = np.append(le_predicate.classes_, '-1')

            # pdb.set_trace()
            X['predicate'] = le_predicate.transform(np.array(X['predicate'].astype(str), dtype=object))
            # X = df.drop(['subject','object'], axis=1)

            ensembleScore = ml_model.predict(X)
            
            df['ensemble_score'] = ensembleScore

            roc_auc = roc_auc_score(y, ensembleScore)

            print("For test we have the roc:auc score "+str(roc_auc))

            logging.info('Validation completed')

            return df

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            # print('Error in validate_model: ', exc_type, fname, exc_tb.tb_lineno)
            logging.error('Error in validate_model: ' +str(e)+ ' ' +str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))
            
            return False


    def test_model(self, df, output_path):
        try:
            # read saved model
            with open(f'{output_path}/classifier.pkl','rb') as fp: ml_model = pickle.load(fp)

            # read predicate label encoder
            with open(f'{output_path}/predicate_le.pkl','rb') as fp: le_predicate = pickle.load(fp)


            X=df.drop(['truth','subject', 'object'], axis=1)

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
            logging.error('Error in test_model: ' +' '+ str(exc_type) +' '+ str(fname) +' '+ str(exc_tb.tb_lineno))

            return False





