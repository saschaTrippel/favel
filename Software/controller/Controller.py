import logging, ast, os

from os import path
from FactValidationService.Validator import Validator
from InputService.Input import Input
from ContainerService.Containers import Containers
from MLService.ML import ML
from OutputService.Output import Output
import pdb 

class Controller:
    """
    Controler that interacts with the different services.
    """
    def __init__(self, approaches:dict, mlAlgorithm:str, mlParameters, experimentPath:str, datasetPath:str, useCache:bool, handleContainers:bool):
        self.approaches = approaches
        self.mlAlgorithm = mlAlgorithm
        self.mlParameters = mlParameters
        self.experimentPath = experimentPath
        self.datasetPath = datasetPath
        self.useCache = useCache
        self.handleContainers = handleContainers
        self.testingData = None
        self.trainingData = None

        self.ml = ML(log_file=path.join(self.experimentPath, "ml_logs.log"))
        
    def createSubExperiment(self):
        try:
            os.mkdir(self.experimentPath)
        except FileExistsError:
            pass

    def startContainers(self):
        if self.handleContainers:
            logging.info("Starting Containers")
            c = Containers()
            c.startContainers() 
            c.status()
    
    def stopContainers(self):
        if self.handleContainers:
            logging.info("Stopping Containers")
            c = Containers()
            c.rmContainers()
        
    def input(self):
        """
        Read the input dataset that was specified using the '-d' argument.
        The assertions are held in self.assertions.
        """
        input = Input()
        self.trainingData, self.testingData = input.getInput(self.datasetPath)

    def validate(self):
        """
        Validate the assertions that are held in self.assertions.
        """
        self.startContainers()
        
        validator = Validator(self.approaches, self.useCache)
        validator.validate(self.trainingData, self.testingData)

        self.stopContainers()
    
    def train(self):
        """
        Train the ML model
        """
        training_df = self.ml.createDataFrame(self.trainingData)
        # if not training_df: logging.info('[controller train] Error in createDataFrame')

        ml_model_name = self.mlAlgorithm
        ml_model = self.ml.get_sklearn_model(ml_model_name, self.mlParameters, training_df)

        self.model, self.lableEncoder, self.trainMetrics = self.ml.train_model(df=training_df, 
                                            ml_model=ml_model, 
                                            output_path=self.experimentPath, 
                                            dataset_path=self.datasetPath)

    def test(self):
        """
        Test the ML model
        """
        testing_df = self.ml.createDataFrame(self.testingData)
        # if not testing_df: logging.info('[controller test] Error in createDataFrame')

        testing_result = self.ml.validate_model(df=testing_df, 
                                                output_path=self.experimentPath, 
                                                dataset_path=self.datasetPath)
        # if not testing_result: logging.info('[controller test] Error in validate_model')

        self.ml_test_result = testing_result
    

    def output(self):
        """
        Write the results to disk.
        Also, Conversion to GERBIL format.
        """
        op = Output(self.experimentPath)
        op.writeOutput(self.ml_test_result)
        op.writeOverview(self.ml_test_result, self.experimentPath, self.datasetPath,
                         self.approaches.keys(), self.mlAlgorithm, self.mlParameters, self.trainMetrics)
        op.gerbilFormat(self.testingData)
