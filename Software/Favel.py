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

if __name__ == '__main__':
    main()
