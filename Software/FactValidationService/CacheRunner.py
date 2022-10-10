import threading
import socket
import logging
from FactValidationService.AbstractJobRunner import AbstractJobRunner
from FactValidationService.Cache import Cache

class CacheRunner(AbstractJobRunner):
    
    def __init__(self, approach:str, port:int, cachePath:str):
        super().__init__(approach, port)
        self.cachePath = cachePath
    
    def run(self):
        self.cache = Cache(self.cachePath, self.approach)
        self._validateCache()
        self.cache.close()
        
    def _validateCache(self):
        cacheEntries = self.cache.getAll()
        if cacheEntries == None:
            return
        
        try:
            logging.info("Validating cache for {}".format(self.approach))
            for entry in cacheEntries:
                self._validateCacheEntry(entry)
        except ConnectionRefusedError:
            return

    def _validateCacheEntry(self, assertion):
        validationResult = self._validateAssertion(assertion)
        if str(assertion[3]) != validationResult:
            logging.info("Corrected {} cache for assertion {} to {}".format(self.approach, assertion, validationResult))
            self.cache.update(assertion[0], assertion[1], assertion[2], validationResult)