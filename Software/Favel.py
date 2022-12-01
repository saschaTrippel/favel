import configparser, logging, argparse

from os import path
from controller.Controller import Controller

def main():
    args = _parseArguments()
    experimentPath = _loadExperimentPath(args)
    config = _loadConfig(experimentPath)
    _configureLogging(config)

    controller = Controller(approaches=dict(config['Approaches']), mlAlgorithm=config['MLAlgorithm']['method'], mlParameters=config['MLAlgorithm']['parameters'],
                            experimentPath=experimentPath, datasetPath=args.data, useCache=bool(config['General']['useCache']), handleContainers=args.containers)

    try:
        controller.input()
        controller.validate()
        controller.train()
        controller.test()
        controller.output()
    except Exception as ex:
        raise ex
        


def _parseArguments(argv=None):
    argumentParser = argparse.ArgumentParser()

    argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
    argumentParser.add_argument("-e", "--experiment", required=True, help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
    argumentParser.add_argument("-c", "--containers", action="store_true", help="To Start/Stop containers, if not already running")
    
    return argumentParser.parse_args(argv)
    
def _loadExperimentPath(args):
    favelPath = path.realpath(__file__)
    pathLst = favelPath.split('/')
    favelPath = "/".join(pathLst[:-2])
    return path.join(favelPath, "Evaluation", args.experiment)

def _loadConfig(experimentPath:str):
    configPath = path.join(experimentPath, "favel.conf")
    if not path.exists(configPath):
        raise FileNotFoundError(f"Config file {configPath} does not exist")
    configParser = configparser.ConfigParser()
    configParser.read(configPath)
    return configParser

def _configureLogging(configParser):
    loggingOptions = dict()
    loggingOptions['debug'] = logging.DEBUG
    loggingOptions['info'] = logging.INFO
    loggingOptions['warning'] = logging.WARNING
    loggingOptions['error'] = logging.ERROR
    loggingOptions['critical'] = logging.CRITICAL
    
    logging.basicConfig(level=loggingOptions[configParser['General']['logging']])

if __name__ == '__main__':
    main()
