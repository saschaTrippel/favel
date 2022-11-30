import logging, argparse, configparser, ast

from os import path
from FactValidationService.Validator import Validator
from InputService.Input import Input
from ContainerService.Containers import Containers
from MLService.ML import ML
from OutputService.Output import Output

class Controller:
    """
    Controler that interacts with the different services.
    """
    def __init__(self, argv=None):
        self.args = self._parseArguments(argv)
        self.experimentPath = self._loadExperimentPath()
        self.configParser = self._loadConfig()
        self._configureLogging()
        self.testingData = None
        self.trainingData = None
        self.validateTrainingData = None

        self.ml = ML(log_file=path.join(self.experimentPath, "ml_logs.log"))

    def _parseArguments(self, argv=None):
        argumentParser = argparse.ArgumentParser()

        argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
        argumentParser.add_argument("-e", "--experiment", required=True, help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
        argumentParser.add_argument("-c", "--containers", action="store_true", help="To Start/Stop containers, if not already running")
    
        return argumentParser.parse_args(argv)
    
    def _loadExperimentPath(self):
        favelPath = path.realpath(__file__)
        pathLst = favelPath.split('/')
        favelPath = "/".join(pathLst[:-3])
        return path.join(favelPath, "Evaluation", self.args.experiment)
        
    def _loadConfig(self):
        configPath = path.join(self.experimentPath, "favel.conf")
        if not path.exists(configPath):
            raise FileNotFoundError(f"Config file {configPath} does not exist")
        configParser = configparser.ConfigParser()
        configParser.read(configPath)
        return configParser
    
    def _configureLogging(self):
        loggingOptions = dict()
        loggingOptions['debug'] = logging.DEBUG
        loggingOptions['info'] = logging.INFO
        loggingOptions['warning'] = logging.WARNING
        loggingOptions['error'] = logging.ERROR
        loggingOptions['critical'] = logging.CRITICAL
        
        logging.basicConfig(level=loggingOptions[self.configParser['General']['logging']])
    
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
        
        validator = Validator(dict(self.configParser['Approaches']), bool(self.configParser['General']['useCache']))

        validator.validate(self.trainingData, self.testingData)

        self.stopContainers()
    
    def train(self):
        """
        Train the ML model
        """
        training_df = self.ml.createDataFrame(self.trainingData)
        # if not training_df: logging.info('[controller train] Error in createDataFrame')

        ml_model_name = self.configParser['MLApproches']['method']
        ml_model_params = self.configParser['MLApproches']['parameters']
        ml_model_params=ast.literal_eval(ml_model_params)
        ml_model = self.ml.get_sklearn_model(ml_model_name, ml_model_params)

        train_result = self.ml.train_model(df=training_df, 
                                            ml_model=ml_model, 
                                            output_path=self.experimentPath, 
                                            dataset_path=self.args.data)

    def test(self):
        """
        Test the ML model
        """
        testing_df = self.ml.createDataFrame(self.testingData)
        # if not testing_df: logging.info('[controller test] Error in createDataFrame')

        testing_result = self.ml.validate_model(df=testing_df, 
                                                output_path=self.experimentPath, 
                                                dataset_path=self.args.data)
        # if not testing_result: logging.info('[controller test] Error in validate_model')

        self.ml_test_result = testing_result
    

    def output(self):
        """
        Write the results to disk.
        Also, Conversion to GERBIL format.
        """
        op = Output(self.experimentPath)
        op.writeOutput(self.ml_test_result)
        op.writeTestOverview(self.ml_test_result, self.experimentPath, self.args.data)
        op.gerbilFormat(self.testingData)
