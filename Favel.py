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

def getOutputs(assertionScores,configParser):
    op = Output(assertionScores,dict(configParser['Approaches']))
    op.getOutput()
    #op.gerbilFormat()


if __name__ == '__main__':
    main()