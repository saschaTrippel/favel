import configparser, logging, argparse

from controller.Controller import Controller

def main():
    controller = Controller()

    if controller.getMethod() == "cache":
        controller.validateCache()
    else:
        controller.input()
        controller.validate()
        controller.train()
        controller.test()
        controller.output()

    # Outputs written to a file './OutputService/Outputs/Output.csv'
    #getOutputs(assertionScores,configParser)

def containers(args, configParser):

    # To start and stop containers with Favel if they are not already running on VM 
    logging.info("Starting Containers")
    c = Containers()
    c.startContainers() 
    c.status()

    assertionScores = validateInputData(args, configParser)

    logging.info("Stopping Containers")
    c.rmContainers()

    return(assertionScores)

def getOutputs(assertionScores,configParser):
    op = Output(assertionScores,dict(configParser['Approaches']))
    op.getOutput()
    #op.gerbilFormat()


if __name__ == '__main__':
    main()