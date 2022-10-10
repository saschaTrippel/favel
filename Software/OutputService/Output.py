import pandas as pd
import csv
from OutputService.GerbilFormat import GerbilFormat

class Output():

	def writeOutput(self,df):
		"""
		Writes results to file.
        """
		df.to_csv("./OutputService/Outputs/Output.csv",index=False)

	def gerbilFormat(self,testingData):
		"""
		To convert testingData into GERBIL format.
		Also, converts output(ensemble_score) from Favel to GERBIL format for Evaluation purposes.
        """
		g = GerbilFormat(testingData)
		g.getGerbilFormat()

