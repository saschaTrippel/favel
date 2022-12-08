import configparser, logging, argparse

from os import path
from controller.Controller import Controller
from argparse import ArgumentParser

def main():
    args = _parseArguments()
    experimentPath = _loadExperimentPath(args)
    config = _loadConfig(experimentPath)
    _configureLogging(config)

    #gen = powerset(list(dict(config['Approaches']).keys()))

    if not args.experiment is None:
        controller = Controller(approaches=dict(config['Approaches']), mlAlgorithm=config['MLAlgorithm']['method'], mlParameters=config['MLAlgorithm']['parameters'],
                                experimentPath=experimentPath, datasetPath=args.data, useCache=eval(config['General']['useCache']), handleContainers=args.containers)
        controller.input()
        controller.validate()
        controller.train()
        controller.test()
        controller.output()
        
    elif not args.batch is None:
        subsetGen = powerset(list(dict(config['Approaches']).items()))
        i = 0
        for subset in subsetGen:
            if len(subset) >= 2:
                subExperimentPath = path.join(experimentPath, f"sub{str(i).rjust(4, '0')}")
                controller = Controller(approaches=dict(subset), mlAlgorithm=config['MLAlgorithm']['method'], mlParameters=config['MLAlgorithm']['parameters'],
                                        experimentPath=subExperimentPath, datasetPath=args.data, useCache=eval(config['General']['useCache']), handleContainers=args.containers)
                
                controller.createSubExperiment()
                controller.input()
                controller.validate()
                controller.train()
                controller.test()
                controller.output()

                i += 1

def powerset(approaches:list):
    if len(approaches) <= 0:
        yield approaches
    else:
        for item in powerset(approaches[1:]):
            yield [approaches[0]] + item
            yield item
                
    

def _parseArguments(argv=None):
    argumentParser = argparse.ArgumentParser()

    argumentParser.add_argument("-d", "--data", required=True, help="Path to input data")
    argumentParser.add_argument("-c", "--containers", action="store_true", help="To Start/Stop containers, if not already running")

    group = argumentParser.add_mutually_exclusive_group(required=True)
    group.add_argument("-e", "--experiment", help="Name of the experiment to execute. The name must correspond to one directory in the Evaluation directory which contains a configuration file")
    group.add_argument("-b", "--batch", help="Name of the experiment to execute in batch mode. Batch mode executes an experiment for each set in the powerset of the approaches.")
    
    return argumentParser.parse_args(argv)
    
def _loadExperimentPath(args):
    favelPath = path.realpath(__file__)
    pathLst = favelPath.split('/')
    favelPath = "/".join(pathLst[:-2])
    if not args.experiment is None:
        return path.join(favelPath, "Evaluation", args.experiment)
    if not args.batch is None:
        return path.join(favelPath, "Evaluation", args.batch)
        
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
