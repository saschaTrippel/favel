import logging, argparse, configparser

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
    
    def validateCache(self):
        return args.cache
        