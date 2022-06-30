import pandas as pd
import csv
from OutputService.GerbilFormat import GerbilFormat

class Output():

	def getOutput(self,assertionScores,approaches):
		"""
		To create the output DataFrame that consists of triples and scores from each approach for that particular triple.
        """
		result = dict()
		result['subject'] = []
		result['predicate'] = []
		result['object'] = []

		for assertionScore in assertionScores:
			result['subject'].append(assertionScore.subject)
			result['predicate'].append(assertionScore.predicate)
			result['object'].append(assertionScore.object)

			for approach in approaches.keys():
				try:
					if str(approach) in result:
						result[str(approach)].append(assertionScore.score[str(approach)])
					else:
						result[str(approach)] = [assertionScore.score[str(approach)]]
				except KeyError as ex:
					pass

		df = pd.DataFrame(result)
		
		return(df)

	def writeOutput(self,df):
		"""
		Writes results to file.
        """
		df.to_csv("./OutputService/Outputs/Output.csv",index=False)

	def gerbilFormat(self):
		"""
		To convert datasets used by Favel into GERBIL format.
		Also, converts output from Favel to GERBIL format for Evaluation purposes.
        """
		g = GerbilFormat()
		g.getGerbilFormat()

