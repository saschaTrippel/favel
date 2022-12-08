import logging, copy
from datastructures.Assertion import Assertion
from InputService.ReadFiles import ReadFiles

class Input:
    cache = dict()
    
    def getInput(self, filePath:str):
        if not filePath in Input.cache.keys():
            result = self.readInput(filePath)
            Input.cache[filePath] = result
        return copy.deepcopy(Input.cache[filePath])
            
    def readInput(self, filePath:str):

        rf = ReadFiles()

        result = []
        if (filePath.endswith(".csv")):
            df = rf.getCsv(filePath)
            result = self.parseTriples(df)
            logging.info("Read {} assertions".format(len(result)))
            return result,result
        
        elif(str(filePath).lower().find("favel") != -1):
            df_train, df_test = rf.getFavel(filePath)
        elif(str(filePath).lower().find("factbench") != -1):
            df_train, df_test = rf.getFactbench(filePath)
        elif(str(filePath).lower().find("bpdp") != -1):
            df_train, df_test = rf.getBPDP(filePath)
        result_train = self.parseTriples(df_train)
        result_test = self.parseTriples(df_test)
        logging.info("Read {} training assertions, {} testing assertions".format(len(result_train),len(result_test)))
        return result_train, result_test
            
    def parseTriples(self, df):
        result = []
        for i, (s,p,o,t) in df.iterrows():
            a = Assertion(s,p,o)
            a._expectedScore = t
            result.append(a)
        return result
