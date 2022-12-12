from os import path
from sklearn import metrics
import logging
import pandas as pd
import statistics

class Overview:

    def __init__(self, testingResults:list, paths:dict, approaches:list, mlAlgorithm:str, mlParameters:str, trainingMetrics, normaliser_name):
        self.evaluation = paths['EvaluationPath']
        self.experiment = paths['SubExperimentName']
        self.dataset = paths['DatasetName']
        self.mlAlgorithm = mlAlgorithm
        self.normaliser_name = normaliser_name
        
        self.approaches = list(approaches)
        self.approaches.sort()
        self.mlParameters = mlParameters
        self.scoresApproaches, self.bestApproach, self.bestApproachScore = self._getBestApproach(testingResults[0][0], approaches)
        self.testingResults = testingResults # [(df, ensemble auc_roc_score)]
        
        self.trainingMean, self.trainingStDev = self._trainingStatistics(trainingMetrics)
        self.testingMean, self.testingStDev = self._testingStatistics(testingResults)
        
    def write(self):
        # Read existing file, or create new data frame
        try:
            overviewFrame = pd.read_excel(path.join(self.evaluation, "Overview.xlsx"))
        except Exception as ex:
            overviewFrame = pd.DataFrame(columns=["Experiment", "Dataset", "Fact Validation Approaches", "#Approaches", "Approaches Scores", "Best Single Approach", "Best Single Score", "ML Algorithm", "ML Parameters", "Normaliser", "Iterations", "Training AUC-ROC Score Mean", "Training AUC-ROC STD. DEV.", "Testing AUC-ROC Score Mean", "Testing AUC-ROC STD. DEV.", "Improvement"])
            
        # Create a new row for current experiment
        row = pd.Series([self.experiment, self.dataset, ", ".join(self.approaches), len(self.approaches), str(self.scoresApproaches), self.bestApproach, self.bestApproachScore, self.mlAlgorithm, self.mlParameters, self.normaliser_name, len(self.testingResults), self.trainingMean, self.trainingStDev, self.testingMean, self.testingStDev, self.testingMean - self.bestApproachScore], index=overviewFrame.columns)
        
        # See if there already is a row for the current experiment and dataset
        dataSet = set(overviewFrame.index[overviewFrame.Dataset == row.Dataset].tolist())
        apSet = set(overviewFrame.index[overviewFrame["Fact Validation Approaches"] == row["Fact Validation Approaches"]].tolist())
        mlSet = set(overviewFrame.index[overviewFrame["ML Algorithm"] == row["ML Algorithm"]].tolist())
        mlParamSet = set(overviewFrame.index[overviewFrame["ML Parameters"] == row["ML Parameters"]].tolist())
        inter = dataSet & apSet & mlSet & mlParamSet
        if len(inter) > 0:
            # Update existing row
            for index in inter:
                logging.debug(f"Updated row in evaluation overvew \n{row}")
                overviewFrame.loc[index, ['Testing AUC-ROC Score']] = self.testingAucRoc
                overviewFrame.loc[index, ['Training AUC-ROC Score']] = self.trainingMetrics['overall']
                overviewFrame.loc[index, ['Improvement']] = self.testingAucRoc - self.bestApproachScore
                overviewFrame.loc[index, ['Approaches Scores']] = str(self.scoresApproaches)
                overviewFrame.loc[index, ['Best Single Approach']] = self.bestApproach
                overviewFrame.loc[index, ['Best Single Score']] = self.bestApproachScore
                overviewFrame.loc[index, ['Experiment']] = self.experiment

        else:
            # Add new row
            overviewFrame = overviewFrame.append(row, ignore_index=True)
            logging.debug(f"Added row to evaluation overview \n{row}")

            
        overviewFrame.to_excel(path.join(self.evaluation, "Overview.xlsx"), index=False)
        
    def _trainingStatistics(self, trainingMetrics):
        tmp = []
        for result in trainingMetrics:
            tmp.append(result['overall'])
        return statistics.mean(tmp), statistics.stdev(tmp)
    
    def _testingStatistics(self, testingResults):
        tmp = []
        for df, auc_roc in testingResults:
            tmp.append(auc_roc)
        return statistics.mean(tmp), statistics.stdev(tmp)
        
    def _getBestApproach(self, df, approaches):
        y = df.truth
        results = dict()
        bestApproach = None
        bestScore = 0
        for approach in approaches:
            approachScore = df[approach]
            auc_roc_single = metrics.roc_auc_score(y, approachScore)
            results[approach] = auc_roc_single
            if auc_roc_single > bestScore:
                bestScore = auc_roc_single
                bestApproach = approach
        return results, bestApproach, bestScore