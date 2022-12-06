import csv
from os import path
from OutputService.GerbilFormat import GerbilFormat
from OutputService.Overview import Overview

class Output():

    def __init__(self, experimentPath:str):
        self.experimentPath = experimentPath

    def writeOutput(self, df):
        """
		Writes results to file.
		"""
        df.to_csv(path.join(self.experimentPath, "Output.csv"), index=False)
        
    def writeOverview(self, df, experimentPath:str, datasetPath:str, approaches:list, mlAlgorithm:str, mlParameters:str, trainingMetrics):
        """
        Write Overview.xlsx
        """
        overview = Overview(df, experimentPath, datasetPath, approaches, mlAlgorithm, mlParameters, trainingMetrics)
        overview.write()
    
    def gerbilFormat(self,testingData):
        """
        To convert testingData into GERBIL format.
        Also, converts output(ensemble_score) from Favel to GERBIL format for Evaluation purposes.
        """
        g = GerbilFormat(testingData, self.experimentPath)
        g.getGerbilFormat()

