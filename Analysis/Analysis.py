from os import path
import pandas as pd
import matplotlib.pyplot as plt

def loadPaths():
    paths = dict()
    favelPath = path.realpath(__file__)
    pathLst = favelPath.split('/')
    favelPath = "/".join(pathLst[:-2])
    
    paths["Overview"] = path.join(favelPath, "Evaluation/Overview.xlsx")
    paths["Analysis"] = path.join(favelPath, "Analysis/")
    return paths
    

def readOverview():
    return pd.read_excel(PATHS["Overview"])

def getBpdp(df):
    return df.loc[df['Dataset'] == "BPDP_Dataset"]

def getFactBench(df):
    return df.loc[df['Dataset'] == "factbench-clean"]

def getFavel(df):
    return df.loc[df['Dataset'] == "FinalDataset_Hard"]

def plotImprovement(df):
    df = df[["Improvement"]]
    plot = df.plot(kind="box", figsize=(3.5, 5.5))
    fig = plot.get_figure()
    fig.savefig(path.join(PATHS["Analysis"], "improvement.pdf"))


def plotPerformanceStdDev(df):
    df = df[["Testing AUC-ROC Mean", "Testing AUC-ROC Std. Dev."]]
    plot = df.plot(x="Testing AUC-ROC Mean", y="Testing AUC-ROC Std. Dev.", kind="scatter")
    fig = plot.get_figure()
    fig.savefig(path.join(PATHS["Analysis"], "performance-stdDev.pdf"))
    
PATHS = loadPaths()

df = readOverview()
plotImprovement(df)
plotPerformanceStdDev(df)
