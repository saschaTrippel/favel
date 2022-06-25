import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from joblib import dump, load
import pickle



def label_encode(vec):
    le = preprocessing.LabelEncoder()
    le.fit(vec)
    vec_en=le.transform(vec)
    return vec_en, le

# le.inverse_transform([0, 0, 1, 2])



def trn_data_triples(df):
    df.fillna(0, inplace=True)
    
    df.subject,le_subject    =label_encode(df.subject)
    df.predicate,le_predicate=label_encode(df.predicate)
    df.object,le_object      =label_encode(df.object)
    
    X=df.drop(['true_value',
              ], axis=1)
    y=df.true_value

    

    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)
    
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

    trn_data=pd.DataFrame({
        'X_train':[X_train],
        'X_test':[X_test],
        'y_train':[y_train],
        'y_test':[y_test],
        'le_subject':[le_subject], 
        'le_predicate':[le_predicate], 
        'le_object':[le_object], 
    })
    return trn_data




def trn_data_wo_triples(df):
    df.fillna(0, inplace=True)
    
    X=df.drop(['true_value',
               'subject',
               'predicate',
               'object'
              ], axis=1)
    y=df.true_value


    X.fillna(0, inplace=True)
    y.fillna(0, inplace=True)
    
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
                        'triples':[set(['subject','predicate', 'object']).issubset(X_train.columns)], 
                        'accuracy':[model.score(X_test, y_test)], 
                        'auc_roc':[roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])]})
    result_df=pd.concat([result_df, tmpdf])
    return result_df



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
        
    best_method=result_df.iloc[result_df.auc_roc.idxmax()]
    
    
    
    print(f'''
        Best Model: {best_method.method_name}
        Auc_Roc:    {best_method.auc_roc}
        Accuracy:   {best_method.accuracy}
        Includes Triples as input: {best_method.triples}

    '''
    )
    
    Path(output_path).mkdir(parents=True, exist_ok=True)    
    
    with open(f'{output_path}/classifier.pkl','wb') as fp: pickle.dump(best_method.method,fp)
    with open(f'{output_path}/le_subject.pkl','wb') as fp: pickle.dump(trn_data.le_subject.item(),fp)
    with open(f'{output_path}/le_predicate.pkl','wb') as fp: pickle.dump(trn_data.le_predicate.item(),fp)
    with open(f'{output_path}/le_object.pkl','wb') as fp: pickle.dump(trn_data.le_object.item(),fp)

    return result_df.reset_index(drop=True)


if __name__=="__main__":
    ''' 
    get input from command line
    ## df
    ## models_list
    ## output_path
    '''
    main(df, models_list, output_path)




        
        
        