import pandas as pd
import csv
from os import path
from pathlib import Path
from sklearn import metrics
from OutputService.GerbilFormat import GerbilFormat

class Output():

    def __init__(self, experimentPath:str):
        self.experimentPath = experimentPath

    def writeOutput(self, df):
        """
		Writes results to file.
		"""
        df.to_csv(path.join(self.experimentPath, "Output.csv"), index=False)
        
    def writeTestOverview(self, df, experimentPath:str, datasetPath:str, approaches):
        
        ### Calculate metrics ###
        # Ensemble score
        y = df.truth
        ensembleScore = df.ensemble_score
        auc_roc = metrics.roc_auc_score(y, ensembleScore)
        
        # Individual scores
        bestApproach = None
        bestScore = 0
        for approach in approaches:
            approachScore = df[approach]
            auc_roc_single = metrics.roc_auc_score(y, approachScore)
            if auc_roc_single > bestScore:
                bestScore = auc_roc_single
                bestApproach = approach

        ### Write file ###
        # Read existing file, or create new data frame
        try:
            overviewFrame = pd.read_excel(path.join(self._getEvaluation(experimentPath), "Overview.xlsx"))
        except Exception as ex:
            overviewFrame = pd.DataFrame(columns=["Experiment", "Dataset", "Best Single Approach", "Best Single Score", "AUC-ROC Score"])
            
        # Create a new row for current experiment
        row = pd.Series([self._getExperiment(experimentPath), self._getDataset(datasetPath), bestApproach, bestScore, auc_roc], index=overviewFrame.columns)
        
        # See if there already is a row for the current experiment and dataset
        exSet = set(overviewFrame.index[overviewFrame.Experiment == row.Experiment].tolist())
        dataSet = set(overviewFrame.index[overviewFrame.Dataset == row.Dataset].tolist())
        inter = exSet & dataSet
        if len(inter) > 0:
            # Update existing row
            for index in inter:
                overviewFrame.loc[index, ['AUC-ROC Score']] = auc_roc
        else:
            # Add new row
            overviewFrame = overviewFrame.append(row, ignore_index=True)

            
        overviewFrame.to_excel(path.join(self._getEvaluation(experimentPath), "Overview.xlsx"), index=False)
    
    def _getExperiment(self, experimentPath:str):
        pathLst = experimentPath.split('/')
        return pathLst[-1]
    
    def _getEvaluation(self, experimentPath:str):
        pathLst = experimentPath.split('/')
        pathStr = "/".join(pathLst[:-1])
        return pathStr
    
    def _getDataset(self, datasetPath:str):
        pathLst = datasetPath.split('/')
        return pathLst[-1]

    def gerbilFormat(self,testingData):
        """
        To convert testingData into GERBIL format.
        Also, converts output(ensemble_score) from Favel to GERBIL format for Evaluation purposes.
        """
        g = GerbilFormat(testingData, self.experimentPath)
        g.getGerbilFormat()

