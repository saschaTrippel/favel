import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner

class AssertionsRunner(AbstractJobRunner):
    """
    Subclass of AbstractJobRunner.
    Uses the functionality of AbstracJobRunner to validate a list of assertions.
    """

    def __init__(self, approach:str, port:int, trainingAssertions:list, testingAssertions:list):
        super().__init__(approach, port)
        self.trainingAssertions = trainingAssertions
        self.testingAssertions = testingAssertions
        self.errorCount = 0
    
    def run(self):
        try:
            # Train supervised approach
            typeMessage = self._type()
            if typeMessage.type == "type_response" and typeMessage.content == "supervised":
                self._train()

            # Validate train and test data
            self._test()
            
            # Close connection
            if self.server != None:
                self.server.close()
        except ConnectionRefusedError:
            return

        if self.errorCount < len(self.assertions):
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(len(self.assertions) - self.errorCount, len(self.assertions), self.approach))

    def _train(self):
        self._trainingStart()
        logging.info("Start training {}".format(self.approach))
        
        for assertion in self.trainingAssertions:
            response = self._trainAssertion(assertion)
            if response.type != 'ack':
                logging.warning("Something went wrong while training {}".format(self.approach))

        self._trainingComplete()
        logging.info("Training of {} completed".format(self.approach))

    
    def _test(self):
        """
        Validate the assertions using self.approach.
        """
        logging.info("Validating assertions using {}".format(self.approach))

        assertions = []
        assertions.extend(self.trainingAssertions)
        assertions.extend(self.testingAssertions)

        for assertion in self.assertions:
            response = self._validateAssertion(assertion)

            if response.type == "error":
                self.errorCount += 1
                logging.warning("'{}' while validating {} using {}."
                                .format(response.content, assertion, self.approach))
            else:
                assertion.score[self.approach] = float(response.score)