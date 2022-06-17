import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner

class AssertionsRunner(AbstractJobRunner):

    def __init__(self, approach:str, port:int, assertions:list):
        super().__init__(approach, port)
        self.assertions = assertions
        self.errorCount = 0
    
    def run(self):
        try:
            self._execute()
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
        output = []

        logging.info("Validating assertions using {}".format(self.approach))
        for assertion in self.assertions:
            response = self._validateAssertion(assertion)

            if type(response) == str and "ERROR" in response:
                self.errorCount += 1
                logging.warning("'{}' while validating {} using {}."
                                .format(response, assertion, self.approach))
            else:
                assertion.score[self.approach] = float(response)
                output.append((self.approach, assertion.subject, assertion.predicate, assertion.object, response))

        with open("./OutputService/Outputs/rawOutputs/Output_Raw.csv", 'w+') as fp:
            for item in output:
                fp.write("{}\n".format(item))