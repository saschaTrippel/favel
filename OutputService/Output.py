import pandas as pd
import csv
from OutputService.GerbilFormat import GerbilFormat

class Output(GerbilFormat):

    def getCleanOutput(self):
        
        result = []

        with open('./OutputService/Outputs/rawOutputs/Output_Raw.csv', 'r') as file:
            for line in file.readlines():
                result.append(self.parseLine(line))

        r = "".join(map(str, result))        
                 
        with open('./OutputService/Outputs/rawOutputs/Output_Clean.csv', 'w+') as file:
            file.write(r) 

        df = pd.read_csv("./OutputService/Outputs/rawOutputs/Output_Clean.csv", sep=";", header=None)
        df.to_csv("./OutputService/Outputs/rawOutputs/Output_Clean.csv", header=["approach", "subject", "predicate", "object", "score"], index=False)
    
    def approachOutput(self,approach:str):

        df = None

        df = pd.read_csv("./OutputService/Outputs/rawOutputs/Output_Clean.csv")

        df[approach] = df.loc[(df["approach"]==approach), ["score"]]  
        df.drop("approach", inplace=True, axis=1)
        df.drop("score", inplace=True, axis=1)

        newdf = df.dropna(axis=0, how='any', inplace=False)
        newdf.to_csv("./OutputService/Outputs/approachOutputs/Output_{}.csv".format(approach),index=False)

        return(newdf)
            
    def allApproaches(self):

        df1 = self.approachOutput("adamic_adar")
        df2 = self.approachOutput("copaal")
        df3 = self.approachOutput("degree_product")
        df4 = self.approachOutput("jaccard")
        df5 = self.approachOutput("katz")
        df6 = self.approachOutput("kl")
        df7 = self.approachOutput("kl_rel")
        df8 = self.approachOutput("ks")
        df9 = self.approachOutput("pathent")
        df10 = self.approachOutput("simrank")
        dff = []
        dfs = [df1,df2,df3,df4,df5,df6,df7,df8,df9,df10]
        for i in range(len(dfs) - 1):
            if not dfs[i].empty:
                dff.append(dfs[i])
        if len(dff)>1:
            for i in range(len(dff) - 1):
                dff[i+1] = pd.merge(dff[i],dff[i+1], validate ="many_to_one")

            dff[i+1].to_csv("./OutputService/Outputs/Output.csv",index=False)
        else:
            dff[0].to_csv("./OutputService/Outputs/Output.csv",index=False)            


    def parseLine(self, line:str):
        line = line.replace('(', '')
        line = line.replace("'", '')
        line = line.replace(')', '')
        line = line.replace('<', '')    
        line = line.replace('>', '')
        line = line.replace(', ', ';')
        return(line) 

    def gerbilFormat(self):
        gerbil = self.getGerbilFormat()