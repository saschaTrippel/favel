import logging, argparse, configparser

from FactValidationService.Validator import Validator
from InputService.Input import Input
from ContainerService.Containers import Containers
from MLService.ML import ML
# from MLService.ML_train import train as train_model, test as test_model
from OutputService.Output import Output
# from MLService.ML_train import main
import sklearn
import pandas as pd
import ast
import pdb

class Controller:
    """
    Controler that interacts with the different services.
    """
    def __init__(self, argv=None):
        self.args = self._parseArguments(argv)
        self.configParser = self._loadConfig()
        self._configureLogging()
        self.testingData = None
        self.trainingData = None
        self.validateTrainingData = None

        
        self.ml = ML(
            log_file=f"../Evaluation/{self.args.experiment}/ml_logs.log",
        )


    def _parseArguments(self, argv=None):
        argumentParser = argparse.ArgumentParser()
        exclusionGroup = argumentParser.add_mutually_exclusive_group(required=True)
    
        exclusionGroup.add_argument("-d", "--data", help="Path to input data")
        exclusionGroup.add_argument("-c", "--cache", action="store_true", help="Check whether the cache entries are correct")

        argumentParser.add_argument("-e", "--experiment", required=True, help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
        argumentParser.add_argument("-sc", "--containers", action="store_true", help="To Start/Stop containers, if not already running")
    
        return argumentParser.parse_args(argv)
        
    def _loadConfig(self):
        configParser = configparser.ConfigParser()
        configParser.read("../Evaluation/{}/favel.conf".format(self.args.experiment))
        return configParser
    
    def _configureLogging(self):
        loggingOptions = dict()
        loggingOptions['debug'] = logging.DEBUG
        loggingOptions['info'] = logging.INFO
        loggingOptions['warning'] = logging.WARNING
        loggingOptions['error'] = logging.ERROR
        loggingOptions['critical'] = logging.CRITICAL
        
        logging.basicConfig(level=loggingOptions[self.configParser['General']['logging']])
    
    def getMethod(self):
        """
        Return what is supposed to be done.
        - 'cache' validate the cache
        - 'train' train the model
        - 'test' test the model
        """
        # TODO: should return either 'cache', 'train', or 'test'
        if self.args.cache:
            return "cache"
        return "train"
    
    def startContainers(self):
        if self.args.containers:
            logging.info("Starting Containers")
            c = Containers()
            c.startContainers() 
            c.status()
    
    def stopContainers(self):
        if self.args.containers:
            logging.info("Stopping Containers")
            c = Containers()
            c.rmContainers()

    def validateCache(self):
        self.startContainers()

        logging.info("Checking cache for correctness")
        validator = Validator(dict(self.configParser['Approaches']), self.configParser['General']['cachePath'])
        validator.validateCache()
        
        self.stopContainers()
        
    def input(self):
        """
        Read the input dataset that was specified using the '-d' argument.
        The assertions are held in self.assertions.
        """
        input = Input()
        self.trainingData, self.testingData = input.getInput(self.args.data)
    
    def validate(self):
        """
        Validate the assertions that are held in self.assertions.
        """
        self.startContainers()
        
        validator = Validator(dict(self.configParser['Approaches']),
                              self.configParser['General']['cachePath'], self.configParser['General']['useCache'])

        validator.validate(self.trainingData, self.testingData)

        self.stopContainers()
    
    def get_sklearn_model(self, model_name, ml_model_params):
        xdf=pd.DataFrame(sklearn.utils.all_estimators())
        model = xdf[xdf[0]==model_name][1].item()

        model=model()

        model.set_params(**ml_model_params)

        return model


    def train(self):
        """
        Train the ML model
        """

        # TODO: call MLService to train model
        training_df = self.ml.createDataFrame(self.trainingData, dict(self.configParser['Approaches']))
        # if not training_df: logging.info('[controller train] Error in createDataFrame')

        ml_model_name = self.configParser['MLApproches']['method']

        ml_model_params = self.configParser['MLApproches']['parameters']

        ml_model_params=ast.literal_eval(ml_model_params)

        ml_model = self.get_sklearn_model(ml_model_name, ml_model_params)

        train_result = self.ml.train_model(df=training_df, 
                                            ml_model=ml_model, 
                                            output_path=f"../Evaluation/{self.args.experiment}", 
                                            dataset_path=self.args.data)
        # if not train_result: logging.info('[controller train] Error in train_model')


    def test(self):
        """
        Test the ML model
        """
        testing_df = self.ml.createDataFrame(self.testingData, dict(self.configParser['Approaches']))
        # if not testing_df: logging.info('[controller test] Error in createDataFrame')

        testing_result = self.ml.validate_model(df=testing_df, 
                                                output_path=f"../Evaluation/{self.args.experiment}", 
                                                dataset_path=self.args.data)
        # if not testing_result: logging.info('[controller test] Error in validate_model')

        self.ml_test_result = testing_result
    

    def output(self):
        """
        Write the results to disk.
        Also, Conversion to GERBIL format.
        """
        op = Output("../Evaluation/{}/".format(self.args.experiment))
        op.writeOutput(self.ml_test_result)
        op.gerbilFormat(self.testingData)
