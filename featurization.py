# create feature vector
import pickle
from utils import *
from filepath import *
import pandas as pd
import numpy as np

def featurization(idMap):
    
    file = open('ai_trajctory.pkl','r')
    tjct = pickle.load(file)
    
    df = pd.read_csv(idMap)
    # data filtering 1: filter the row where trajectoryId is missing
    df = df[df.trajectoryId.isin(list(tjct.keys()))]

    # data filtering 2: filter the row where secretId is not in attemptSet
    attempt_set = np.loadtxt(attemptSet)
    df = df[df.secretId.isin(attempt_set)]

    #insert a label row
    df.insert(2,'aiScore',0)
    df.insert(3,'attempts',1)
    df.insert(4,'response',1)
    df.insert(5,'label', 0)

    # assigning value to 'label'
    perfect_set = np.loadtxt(perfectSet)
    perfect_stu = df.secretId.isin(perfect_set)
    df['label'][perfect_stu]=1

    #assigning value to 'aiScore', 'attempts' and 'response'
    for ind, row in df.iterrows():
        df.at[ind,'attempts'] = len(tjct[row.trajectoryId])
        df.at[ind,'aiScore'] = np.mean(tjct[row.trajectoryId])
        if tjct[row.trajectoryId][-1] !=0:
            df.at[ind,'response'] = 0
    return df