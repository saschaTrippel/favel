import pandas as pd
import csv

from OutputService.GerbilFormat import GerbilFormat

class Output(GerbilFormat):

	def __init__(self,assertionScores,approaches):
		self.assertionScores = assertionScores
		self.approaches = approaches

	def getOutput(self):

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
				if str(approach) in result:
					result[str(approach)].append(assertionScore.score[str(approach)])
				else:
					result[str(approach)] = [assertionScore.score[str(approach)]]

		df = pd.DataFrame(result)
		df.to_csv("./OutputService/Outputs/Output.csv",index=False)

		return(df)

	def parseLine(self, line):
		line = line.replace('<', '')
		line = line.replace('>', '')

		return(line.split(' '))

	def gerbilFormat(self):
		"""
		To convert datasets used by Favel into GERBIL format.
		Also, converts output from Favel to GERBIL format for Evaluation purposes.
        """
		super().__init__()
		self.getGerbilFormat()