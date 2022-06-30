import logging, argparse, configparser

from FactValidationService.Validator import Validator
from InputService.Input import Input
from ContainerService.Containers import Containers
from OutputService.Output import Output

class Controller:
    """
    Controler that interacts with the different services.
    """
    def __init__(self):
        self.args = self._parseArguments()
        self.configParser = self._loadConfig()
        self._configureLogging()

    def _parseArguments(self):
        argumentParser = argparse.ArgumentParser()
        exclusionGroup = argumentParser.add_mutually_exclusive_group(required=True)
    
        exclusionGroup.add_argument("-d", "--data", help="Path to input data")
        exclusionGroup.add_argument("-c", "--cache", action="store_true", help="Check whether the cache entries are correct")
        argumentParser.add_argument("-sc", "--containers", action="store_true", help="To Start/Stop containers, if not already running")
    
        return argumentParser.parse_args()
        
    def _loadConfig(self):
        configParser = configparser.ConfigParser()
        configParser.read("favel.conf")
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
        # TODO: should return either 'cache', 'train', or 'test'
        if self.args.cache:
            return "cache"
        return "train"

    def validateCache():
        logging.info("Checking cache for correctness")
        validator = Validator(dict(self.configParser['Approaches']), self.configParser['General']['cachePath'])
        validator.validateCache()
        
    def input(self):
        """
        Read the input dataset that was specified using the '-d' argument.
        The assertions are held in self.assertions.
        """
        input = Input()
        self.assertions = input.getInput(self.args.data)
    
    def validate(self):
        """
        Validate the assertions that are held in self.assertions.
        """
        validator = Validator(dict(self.configParser['Approaches']),
                              self.configParser['General']['cachePath'], self.configParser['General']['useCache'])

        validator.validate(self.assertions)
    
    def train(self):
        """
        Train the ML model
        """
        pass
    
    def test(self):
        """
        Test the ML model
        """
        pass
    
    def output(self):
        """
        Write the results to disk.
        """
        pass