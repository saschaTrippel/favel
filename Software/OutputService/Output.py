import pandas as pd
import csv
from OutputService.GerbilFormat import GerbilFormat

class Output():

	def __init__(self, experimentPath:str):
		self.experimentPath = experimentPath

	def writeOutput(self,df):
		"""
		Writes results to file.
        """
		df.to_csv("{}Output.csv".format(self.experimentPath), index=False)

	def gerbilFormat(self,testingData):
		"""
		To convert testingData into GERBIL format.
		Also, converts output(ensemble_score) from Favel to GERBIL format for Evaluation purposes.
        """
		g = GerbilFormat(testingData, self.experimentPath)
		g.getGerbilFormat()

