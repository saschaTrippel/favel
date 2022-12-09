from FactValidationService.AssertionsRunner import AssertionsRunner
from FactValidationService.AssertionsCacheRunner import AssertionsCacheRunner

class Validator:
    
    def __init__(self, approaches, useCache:bool=True):
        self.approaches = approaches
        if type(useCache) == str:
            self.useCache = useCache == 'True'
        else:
            self.useCache = useCache

    def validate(self, trainingAssertions:list, testingAssertions:list):
        """
        Validate the given assertions on every approach.
        Assertions expected as a list of assertions.
        Returns list of assertions with their scores added to the Assertion.score[approach] dictionary.
        """
        jobs = []
        
        # Start a thread for each approach
        for approach in self.approaches.keys():
            if self.useCache:
                jobRunner = AssertionsCacheRunner(approach, int(self.approaches[approach]), trainingAssertions, testingAssertions)
            else:
                jobRunner = AssertionsRunner(approach, int(self.approaches[approach]), trainingAssertions, testingAssertions)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()

        return trainingAssertions, testingAssertions
            
        

