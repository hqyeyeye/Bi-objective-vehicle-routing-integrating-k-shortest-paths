# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 11:09:23 2021

@author: huqio
"""
import networkx as nx
from copy import deepcopy
import queue
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, text
#from mpl_toolkits.basemap import Basemap as Basemap
#import names
import csv
#import math
import numpy as np
import pandas as pd
from FirstStep import yen
#nodes_file=csv.reader(open('nodes.csv','r'));
#links_file=csv.reader(open('lk_risks.csv','r'));
nodes_file=csv.reader(open('nodes_chi_nash.csv','r'));
links_file=csv.reader(open('links_chi_nash_0201.csv','r'));

G_network=nx.Graph()
G_network_distance=nx.Graph()

G_network=nx.Graph()
G_network_distance=nx.Graph()
tmp=0
for row in nodes_file:
    if (tmp>0):
        G_network.add_node(row[0])
        G_network_distance.add_node(row[0])      
    tmp=+1
    
tmp=0
for row in links_file:
    if (tmp>0): # Ignores the first line in the file
#        print(tmp)
        G_network.add_edge(row[1],row[2]);
        G_network[row[1]][row[2]]['weight']=float(row[4]);
        G_network_distance.add_edge(row[1],row[2]);
        G_network_distance[row[1]][row[2]]['weight']=float(row[3]);      
    tmp+=1;



src='Nashville';
tgt='Gary';
k=100;

k_path, path_costs=yen(G_network,src,tgt,k);
print("Possible paths:",k_path)
print("Distance for each path:",path_costs)



from obj import OptimizePath
pareto_list,dataset=OptimizePath(k_path,8.2)    
#print(dataset)


#get gps for the points for all the path for Jupyter plotly later
def k_path_plot(path_list):
    city=[]
    rank=[]
    lat=[]
    lon=[]
    geom=[]
    df=pd.read_csv("nodes_location_chi_nash.csv")
    for i in range(len(k_path)):
        for j in k_path[i]:
            city.append(j)
            a=i+1
            rank.append(a)
            temp = df.loc[df['Name']==j]
            b=temp["Y"].values[0]
            c=temp["X"].values[0]
            d=temp["geom"].values[0]
            lat.append(b)
            lon.append(c)
            geom.append(d)
            
    ls=[city,lat,lon,geom,rank]
    result=pd.DataFrame(ls).transpose()
    result.columns=['city','lat','lon','geom','k_shortest_path']
    return(result)
    
path_before_Pareto=k_path_plot(k_path)
path_before_Pareto.to_csv("100path_travel_time_NumRisk.csv")


#def k_path_rank(path_list,pareto_list):
#    city=[]
#    rank=[]
#    lat=[]
#    lon=[]
#    geom=[]
#    minimum=min(pareto_list)
#    diff=1-minimum
#    new_list=[x+diff for x in pareto_list]
#    df=pd.read_csv("nodes_location_chi_nash.csv")
#    for i in range(len(k_path)):
#        for j in k_path[i]:
#            city.append(j)
#            rank.append(new_list[i])
#            temp = df.loc[df['Name']==j]
#            b=temp["Y"].values[0]
#            c=temp["X"].values[0]
#            d=temp["geom"].values[0]
#            lat.append(b)
#            lon.append(c)
#            geom.append(d)            
#    ls=[city,lat,lon,geom,rank]
#    result=pd.DataFrame(ls).transpose()
#    result.columns=['city','lat','lon','geom','rank']
#    return(result)
#    
#path_after_Pareto=k_path_rank(k_path,pareto_list)
#path_after_Pareto.to_csv("100path_TrueTime_glmProb.csv")

#result=k_path_rank(k_path,pareto_list)
#result.to_csv("100path_cart_rank.csv")
#
#print(dataset)

def write_result(dataset,pareto_list):
    travel_time=[]
    NCE=[]
    rank=[]
    for i in range(len(dataset)):
        a=dataset[i].vec[0]
        b=dataset[i].vec[1]
        diff=1-min(pareto_list)
        c=dataset[i].paretoStatus+diff
        travel_time.append(a)
        NCE.append(b)
        rank.append(c)
    result_list=[travel_time,NCE,rank]
    result_list1=pd.DataFrame(result_list).transpose()
    result_list1.columns=['Real_travle_time','NCEs','Pareto_rank']
    return result_list1
rrr=write_result(dataset,pareto_list)
