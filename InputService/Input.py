import logging
import pandas as pd
from datastructures.Assertion import Assertion
from InputService.ReadFiles import ReadFiles

class Input:
    
    def getInput(self, filePath:str):
        
        rf = ReadFiles()
        
        result = []
        if (filePath.endswith(".csv")):
            df = rf.getCsv(filePath)
        elif(str(filePath).lower().find("favel") != -1):
            df = rf.getFavel(filePath)
        elif(str(filePath).lower().find("factbench") != -1):
            df = rf.getFactbench(filePath)
        elif(str(filePath).lower().find("bpdp") != -1):
            df = rf.getBPDP(filePath)
        result = self.parseTriples(df)
        logging.info("Read {} assertions".format(len(result)))
        return result
            
    def parseTriples(self, df):
        result = []
        for i, (s,p,o,t) in df.iterrows():
            result.append(Assertion(s,p,o))
        return result