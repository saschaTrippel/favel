import logging

from FactValidationService.AssertionsRunner import AssertionsRunner
from FactValidationService.AssertionsCacheRunner import AssertionsCacheRunner
from FactValidationService.CacheRunner import CacheRunner

class Validator:
    def __init__(self, approaches, cachePath:str=None, useCache:bool=True):
        self.approaches = approaches
        self.cachePath = cachePath
        if type(useCache) == str:
            self.useCache = useCache == 'True'
        else:
            self.useCache = useCache

    def validate(self, assertions:list):
        """
        Validate the given assertions on every approach.
        Assertions expected as a list of assertions.
        Returns list of assertions with their scores added to the Assertion.score[approach] dictionary.
        """
        jobs = []
        
        # Start a thread for each approach
        for approach in self.approaches.keys():
            if self.useCache:
                jobRunner = AssertionsCacheRunner(approach, int(self.approaches[approach]), assertions, self.cachePath)
            else:
                jobRunner = AssertionsRunner(approach, int(self.approaches[approach]), assertions)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()

        return assertions
        
    def validateCache(self):
        jobs = []
        for approach in self.approaches.keys():
            jobRunner = CacheRunner(approach, int(self.approaches[approach]), self.cachePath)
            jobs.append(jobRunner)
            jobRunner.start()
            
        # Wait for all threads to finish
        for job in jobs:
            job.join()
            
        

