import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner
from datastructures.Assertion import Assertion

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
        self.trainingComplete = False
    
    def run(self):
        try:
            # Validate train and test data
            self._test()
            
            # Close connection
            if self.server != None:
                self.server.close()
        except ConnectionRefusedError:
            return

        size = len(self.trainingAssertions) + len(self.testingAssertions)
        if self.errorCount < size:
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(size - self.errorCount, size, self.approach))
            
    def _validateAssertion(self, assertion:Assertion):
        # Train supervised approach
        if not self.trainingComplete and self.type == "supervised":
            self._train()
            self.trainingComplete = True
        
        return super()._validateAssertion(assertion)
    
    def _train(self):
        # TODO: check if acks are returned
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

        for assertion in assertions:
            response = self._validateAssertion(assertion)

            if response.type == "error":
                self.errorCount += 1
                logging.warning("'{}' while validating {} using {}."
                                .format(response.content, assertion, self.approach))
            else:
                assertion.score[self.approach] = float(response.score)