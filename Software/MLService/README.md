FAVEL ML Service
=

# Configuration

The machine learning (ML) algorithm has to be specified in the configuration file favel.conf under the MLApproaches tag. The algorithm name must be the sklearn module. The parameters of this algorithm have to be passed in JSON format.

```
[MLApproches]
method = GradientBoostingClassifier
parameters = {'n_estimators': 100, 'learning_rate': 1.0, 'max_depth': 1, 'random_state': 0}
```

# Outputs 

* ``` Classification Report.xlsx ``` shows the performance of the ML model for each class. 
* ``` classifier.pkl ``` trained ml model dump in pickle format.
* ``` predicate_le.pkl ``` label encoding for predicates dump in pickle format.
* ``` ml_result.xlsx``` contains accuracy, roc_auc scores of ml model from each experiment.  