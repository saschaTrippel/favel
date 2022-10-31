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
        
        # TODO: remove
        self.assertions = []
        self.assertions.extend(trainingAssertions)
        self.assertions.extend(testingAssertions)

        self.errorCount = 0
    
    def run(self):
        try:
            self._execute()
            if self.server != None:
                self.server.close()
        except ConnectionRefusedError:
            return

        if self.errorCount < len(self.assertions):
            logging.info("Validated {} out of {} assertions successfully using {}."
                         .format(len(self.assertions) - self.errorCount, len(self.assertions), self.approach))

    def _execute(self):
        """
        Validate the assertions using self.approach.
        """
        logging.info("Validating assertions using {}".format(self.approach))
        for assertion in self.assertions:
            response = self._validateAssertion(assertion)

            if type(response) == str and "ERROR" in response:
                self.errorCount += 1
                logging.warning("'{}' while validating {} using {}."
                                .format(response, assertion, self.approach))
            else:
                assertion.score[self.approach] = float(response)