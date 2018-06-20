
# build AST Tree and compute the zss edit distance between different ASTs
from __future__ import division
import json
import csv
import numpy as np
import zss
from os import listdir
from os.path import splitext
from itertools import imap, chain
from operator import sub
from filepath import *
import progressbar 
from scipy.special import logit
from sklearn.metrics import confusion_matrix
from scipy.special import logit

# define the tree structure that can be inputed in to zss
class Node(object):
    def __init__(self, id=None, label=None,level=0):
        self.id = id
        self.label = label
        self.level = level
        self.children = []

    def __repr__(self):        
        return '\n{indent}Node({id},{label},{children})'.format(
                                         indent = self.level*'\t', 
                                         id = self.id,
                                         label = self.label,
                                         children = repr(self.children))
    def add_child(self, child):
        self.children.append(child)    

def tree_builder(obj, level=0):
    node = Node(id=obj['id'], label=obj['type'], level=level)
    for child in obj.get('children',[]):
        node.add_child(tree_builder(child, level=level+1))
    return node

# load ast json file
def load_json(ast_no):
    with open(asts+"%s.json"%ast_no) as f:
        return json.load(f)

# the ast file are named using number from 1 to 79553, but some files are missing. To implement cycle
# we need first to get all the ast json file name without .json suffix
def get_ast_lists (asts):
    #listdir(ast_path)
    ast_lists =[]
    for data_file in sorted(listdir(asts)):
        ast_lists.append (splitext(data_file)[0]) # get the name of each ast file without suffix
    ast_lists = np.sort(map(int, ast_lists)) #convert list to sorted numeric
    return ast_lists

def metrics(confusion_matrix):
    tn = confusion_matrix[0,0]
    fp = confusion_matrix[0,1]
    fn = confusion_matrix[1,0]
    tp = confusion_matrix[1,1]
    condition_negative = fp + tn
    condition_postive = tp + fn
    accuracy = (tp+tn)/(tn+fp+fn+tp)
    recall = tp/condition_postive
    fnr = fn/ condition_postive
    specificity = tn / condition_negative
    dor = logit(recall)-logit(1-specificity)
    return accuracy, recall, specificity,dor