#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 10:38:36 2020

@author: adigo10
"""

import pandas as pd
import numpy as np
import warnings

warnings.simplefilter("ignore")
dataset_train = pd.read_csv('Airlines Data CrowdStrike - RawTest_v5.csv')
dataset_train.head(10)

#Training Dataset Size
print("Shape of Traning Data is",dataset_train.shape)
dataset_train.describe()
grouped = dataset_train.groupby('SourceAirportID')
print("Class size:\n", grouped.size())

#Unique Value Counts
print("Source Airports' count:",dataset_train['SourceAirportID'].nunique())
print("Destination Airports' count:",dataset_train['DestinationAirportID'].nunique())

#Source Airports Array
src_arpt = dataset_train['SourceAirportID'].values
"""print(src_arpt)"""
print("Size of Source Airport Array:",src_arpt.size)

#Array of Destination Airports
dest_arpt = dataset_train['DestinationAirportID'].values
"""print(dest_arpt)"""
print("Size of Destination Airport Array:",dest_arpt.size)

#Dijkstra's Shortest Path Algorithm

adjacancy_mat = pd.crosstab(dataset_train['SourceAirportID'],dataset_train['DestinationAirportID'])

idx = adjacancy_mat.columns.union(adjacancy_mat.index)
adjacancy_mat = adjacancy_mat.reindex(index=idx,columns=idx,fill_value=0)
adjacancy_mat.to_csv('Adj_Mat.csv')
adjacancy_mat.head()
"""print("Size of Adjacancy Matrix is:",adjacancy_mat.shape)"""

#using networkx api
import networkx as nx
input_data = pd.read_csv('Adj_Mat.csv', index_col=0)
G = nx.DiGraph(input_data.values)
nx.draw(G)

input_data = pd.read_csv('Adj_Mat.csv', index_col=0)
input_data.head(3)
nx.shortest_path_length(G, source=0, target=1799)
labels = np.array(input_data.columns)
indexes = list(np.arange(0,2000,1))

#dictionary for airports
arpt = {}
for key in labels:
    for value in indexes:
        arpt[key] = value
        indexes.remove(value)
        break
"""print(arpt)"""

#testing 
test_dataset = pd.read_csv('testdata.csv')
test_dataset.head()
test_set = test_dataset.drop('PairID',axis=1)
test_set.head()

result = []
len(result)

nx.shortest_path_length(G, source=arpt['ADW'], target=arpt['ADV'])
for i,j in zip(test_set['SourceAirportID'],test_set['DestinationAirportID']):
    try:
        n=nx.shortest_path_length(G, source=arpt[i], target=arpt[j])-1
        result.append(n)
    except nx.NetworkXNoPath:
        result.append(-1)
        

len(result)

cnt=0;
for i in result:
    if i==9:
        cnt=cnt+1;
print(cnt)
test_dataset.shape

#output/submission csv
output = pd.DataFrame({'PairID':test_dataset.PairID,'Hops':result})
output.to_csv('submission.csv',index=False)
print('Submission FILE generated')