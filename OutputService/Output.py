import pandas as pd
import csv
import logging
from OutputService.GerbilFormat import GerbilFormat
from MLService.ML import ML

class Output(GerbilFormat):

	def __init__(self,assertionScores,approaches):
		self.assertionScores = assertionScores
		self.approaches = approaches

	def getOutput(self):
		# TODO: this should not be in output service,
		# output service should only write stuff to disk, not prepocess stuff for MLService
		"""
		To create the output DataFrame that consists of triples and scores from each approach for that particular triple.
		Returns a DataFrame that would be used by MLService to give the Ensemble score
        """
		result = dict()
		result['subject'] = []
		result['predicate'] = []
		result['object'] = []

		for assertionScore in self.assertionScores:
			result['subject'] += self.parseLine(assertionScore.subject)
			result['predicate'] += self.parseLine(assertionScore.predicate)
			result['object'] += self.parseLine(assertionScore.object)

			for approach in self.approaches.keys():
				try:
					if str(approach) in result:
						result[str(approach)].append(assertionScore.score[str(approach)])
					else:
						result[str(approach)] = [assertionScore.score[str(approach)]]
				except KeyError as ex:
					pass

		df = pd.DataFrame(result)
		dff = self.ensembleScores(df)
		
		dff.to_csv("./OutputService/Outputs/Output.csv",index=False)
		
		return(dff)
		
	def parseLine(self, line):
		line = line.replace('<', '')
		line = line.replace('>', '')

		return(line.split(' '))

	def ensembleScores(self, df):
		# TODO: MLService should be called in Favel.py, not in OutputService
		"""
		To get ensemble score from ML Service.
        """
		ml = ML()
		ensembleScore = []
		ensembleScore = ml.getEnsembleScore(df)
		df['ensemble_score'] = ensembleScore
		return(df)

	def gerbilFormat(self):
		"""
		To convert datasets used by Favel into GERBIL format.
		Also, converts output from Favel to GERBIL format for Evaluation purposes.
        """
		super().__init__()
		self.getGerbilFormat()

