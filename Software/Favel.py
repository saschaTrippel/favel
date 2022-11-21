import configparser, logging, argparse

from controller.Controller import Controller

def main():
    controller = Controller()

    try:
        controller.input()
        controller.validate()
        controller.train()
        controller.test()
        controller.output()
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    main()
