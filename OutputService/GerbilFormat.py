import pandas as pd
import csv

class GerbilFormat:

	def __init__(self,testingData):

		self.title = "<http://favel.dice-research.org/task/dataset/"
		self.subject = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#subject>"
		self.predicate = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate>"
		self.object = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#object>"
		self.truthValue = "<http://swc2017.aksw.org/hasTruthValue>"
		self.doubleText = "<http://www.w3.org/2001/XMLSchema#double>"
		self.tripleType = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
		self.statement = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement>"
		self.testingData = testingData
		self.formatDataset()

	def createTripleSubject(self, datasetName,subjectString):
		string = ""
		string += datasetName + " " + self.subject + " " +  "<" + subjectString + ">" +" ." + "\n"
		return string

	def createTriplePredicate(self, datasetName,predicateString):
		string = ""
		string += datasetName + " " + self.predicate +  " " + "<" + predicateString + ">" +" ." + "\n"
		return string

	def createTripleObject(self, datasetName,objectString):
		string = ""
		string += datasetName + " " + self.object +  " " + "<" + objectString + ">" +" ." + "\n"
		return string   
	
	def createTripleType(self, datasetName):
		string = ""
		string += datasetName + " " + self.tripleType + " " + self.statement + " ." + "\n"
		return string

	def createTruthValueTriple(self, datasetName, truthValueFloat):
		string = ""
		string += datasetName + " " + self.truthValue + ' "%s"^^' %str(truthValueFloat) + self.doubleText + " ." + "\n"
		return string

	def formatDataset(self):
		'''Writing the testingData in specified format'''

		df = dict()
		df['subject'] = []
		df['predicate'] = []
		df['object'] = []
		df['true_value'] = []

		for assertion in self.testingData:
			df['subject'].append(assertion.subject)
			df['predicate'].append(assertion.predicate)
			df['object'].append(assertion.object)
			df['true_value'].append(assertion._expectedScore)
			print(assertion._expectedScore)
		
		data1 = pd.DataFrame(df)	# DataFrame with triples and Truth value

		array = " "
		for index,rows in data1.iterrows():
		#    if(index == 0):
		        # Triple Name
				datasetName = self.title + str(index) + ">"
		        #Type of triple
				array += self.createTripleType(datasetName)
		        # Triple Subject 
				array += self.createTripleSubject(datasetName,rows["subject"])
		        #Triple Predicate
				array += self.createTriplePredicate(datasetName,rows["predicate"])
		        # Triple Object
				array += self.createTripleObject(datasetName,rows["object"])
		        # Truth Value
				array += self.createTruthValueTriple(datasetName,rows["true_value"])
		        
				with open("./OutputService/Outputs/GerbilFormat/favel.nt","w+") as file:
					file.write(array)

	def createOutputFileForEvaluation(self):
		'''Writing the output file (for ensemble scores only) in the specified Format'''

		data = pd.read_csv('./OutputService/Outputs/Output.csv')	# Read the Output from our software containing ensemble_score

		array = " "
		for outputFileIndex,rows in data.iterrows():
	        # Triple Name
			datasetName = self.title + str(outputFileIndex) + ">"
			array += self.createTruthValueTriple(datasetName , str(rows['ensemble_score']))

			with open("./OutputService/Outputs/GerbilFormat/favel_ensemble.nt","w+") as file:
				file.write(array)

	def getGerbilFormat(self):
		
		# Create output file in GERBIL format for ensemble scores given by FaVEL
	
		self.createOutputFileForEvaluation()

		


