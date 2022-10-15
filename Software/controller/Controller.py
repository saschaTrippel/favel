import logging, argparse, configparser

from FactValidationService.Validator import Validator
from InputService.Input import Input
from ContainerService.Containers import Containers
from MLService.ML import ML
from MLService.ML_train import train, test
from OutputService.Output import Output
# from MLService.ML_train import main

class Controller:
    """
    Controler that interacts with the different services.
    """
    def __init__(self):
        self.args = self._parseArguments()
        self.configParser = self._loadConfig()
        self._configureLogging()
        self.testingData = None
        self.trainingData = None
        self.validateTrainingData = None
        self.ml = ML()

    def _parseArguments(self):
        argumentParser = argparse.ArgumentParser()
        exclusionGroup = argumentParser.add_mutually_exclusive_group(required=True)
    
        exclusionGroup.add_argument("-d", "--data", help="Path to input data")
        exclusionGroup.add_argument("-c", "--cache", action="store_true", help="Check whether the cache entries are correct")

        argumentParser.add_argument("-e", "--experiment", required=True, help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
        argumentParser.add_argument("-sc", "--containers", action="store_true", help="To Start/Stop containers, if not already running")
    
        return argumentParser.parse_args()
        
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

        self.validateTrainingData = validator.validate(self.trainingData)
        self.scores               = validator.validate(self.testingData)

        self.stopContainers()
    
    def train(self):
        """
        Train the ML model
        """
        # TODO: call MLService to train model
        training_df = self.ml.createDataFrame(self.validateTrainingData,dict(self.configParser['Approaches']))
        train_result = train(training_df, ml_model=self.configParser['MLApproches']['method'], output_path=self.args.experiment)

    def test(self):
        """
        Test the ML model
        """
        testing_df = self.ml.createDataFrame(self.scores,dict(self.configParser['Approaches']))
        testing_result = test(testing_df, output_path=self.args.experiment)
        self.ml_test_result = testing_result
    

    def output(self):
        """
        Write the results to disk.
        Also, Conversion to GERBIL format.
        """
        op = Output("../Evaluation/{}/".format(self.args.experiment))
        op.writeOutput(self.ml_test_result)
        op.gerbilFormat(self.testingData)
