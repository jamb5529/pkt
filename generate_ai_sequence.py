# This code is to generate feasible approaching index sequences from given data.

from utils import *
from filepath import *
import pandas as pd
import numpy as np
import zss
import pickle

def generate_ai_sequence(df, ast_list,best_ast_no):
 
    trajct= dict()
    for i in df.trajectoryId:
        with open(trajectories+"%s.txt"%i, 'r') as fin:
            rawpath = fin.read().splitlines()
            trajct[i] = map(int,rawpath)
    print "Length of original trajectories: %d" % len(trajct)

    del_key=[]
    print "1. Detecting the key-value paris contain missing ASTs:"
    for key in progressbar.progressbar(trajct):
        if set(trajct[key]).issubset(set(ast_list)) == False :
            del_key.append(key)

    print "2. Droping the trajectories contain missing ASTs:"        
    for key in progressbar.progressbar(del_key):
        del trajct[key]
    print "Lenght of reduced trajectories: %d" % len(trajct)

    print "3. Computing appoaching index for each trajectory:"
    best_ast = load_json(best_ast_no)
    for key, value in progressbar.progressbar(trajct.items()):
        for i in range(len(value)):
            current_ast = load_json(trajct[key][i])
            trajct[key][i] = zss.simple_distance(tree_builder(current_ast),tree_builder(best_ast))
    # save trajct dict intp pickle, if you want
    # f = open("ai_trajctory.pkl","wb")
    # pickle.dump(trajct,f)
    # f.close()
    return trajct