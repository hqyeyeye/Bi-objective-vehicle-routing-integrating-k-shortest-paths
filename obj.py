"The implementation is largely influenced by the Yen's algorithm in Wikipedia and beegeesquare's implementation on github"
"the code of Pareto Ranking is from matthewjwoodruff on github"
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
nodes_file=csv.reader(open('nodes_chi_nash.csv','r'));
links_file=csv.reader(open('links_chi_nash_0201.csv','r'));

#G_network=nx.Graph()
G_network_distance=nx.Graph()

#G_network=nx.Graph()
G_network_distance=nx.Graph()
tmp=0
for row in nodes_file:
    if (tmp>0):
#        G_network.add_node(row[0])
        G_network_distance.add_node(row[0])      
    tmp=+1
    
tmp=0
for row in links_file:
    if (tmp>0): # Ignores the first line in the file
#        print(tmp)
#        G_network.add_edge(row[1],row[2]);
#        G_network[row[1]][row[2]]['weight']=float(row[4]);
        G_network_distance.add_edge(row[1],row[2]);
        G_network_distance[row[1]][row[2]]['weight']=float(row[3]);      
    tmp+=1;


def GetSpeed(start,end,old_time):
    df=pd.read_csv("speed.csv")
    if old_time-int(old_time)<=0.5:
        time=int(old_time)
    else:
        time=int(old_time)+1        
    speed = df[(df['starting']==start)&\
              (df['ending']==end)&(df['time']==time)]['speed'].values[0]
    return speed

#GetSpeed('Nashville', 'Clarksville',8.2)


def GetArrivalTime(path,begin_time):
    travel_time=[]
    arrival_time=begin_time
    arrival_list=[begin_time]
    for i in range(len(path)-1):
        speed=GetSpeed(path[i],path[i+1],arrival_time)
#        use the distance netword to find the true travel time
        t=G_network_distance[path[i]][path[i+1]]['weight'] / speed
        travel_time.append(t)
        arrival_time=arrival_time + t
        arrival_list.append(arrival_time)
    total_drive=sum(travel_time)
    return arrival_list, total_drive      

#GetArrivalTime(k_path[0],8)
    
def GetRisk(start,end,old_time):
    df=pd.read_csv("links_risk_0201.csv")
    if old_time-int(old_time)<=0.5:
        time=int(old_time)
    else:
        time=int(old_time)+1 
    risk = df[(df['starting']==start)&\
              (df['ending']==end)&(df['time']==time)]['cart.Yes'].values[0]
    return risk

#GetRisk('Nashville', 'Clarksville',8.3)

#result=GetRisk("Auburn","Birmingham",8.3)
def PathObj(path,begin_time):
    arrival_time,cumulative_time=GetArrivalTime(path,begin_time)
    risk=[]
# if the risk is 0 or 1, please use the below code    
#    for i in range(len(path)-1):
#        temp=GetRisk(path[i],path[i+1],arrival_time[i])
#        risk.append(temp)
##        print(risk)
#    total_risk=sum(risk)
#if the risk represents the probability beween 0 and 1, please use this
   
    for i in range(len(path)-1):
#        print(i)
        temp=1-GetRisk(path[i],path[i+1],arrival_time[i])
        risk.append(temp)
#    print(risk)
    no_risk_prob = np.prod(risk)
    total_risk=1-no_risk_prob
        
#    print("total risk,", total_risk)
    obj1=cumulative_time
    obj2=total_risk
    return obj1,obj2

#PathObj(k_path[0],8)

class Datapoint:
    """Defines a point in K-dimensional space"""
    def __init__(self,id):

        self.id = id # datapoint id (0,..N-1)
        self.vec = [] # the K-dim vector
        self.paretoStatus = -1 # -1=dont know, 1=pareto, 0=not pareto
        self.dominatedCount = 0 # number of datapoints that dominate this point
        self.dominatingSet = [] # set of vectors this one is dominating

    def addNumber(self,num):
        """Adds a number to one dimension of this datapoint"""
        self.vec.append(num)

    def addToDominatingSet(self,id2):
        """Add id of dominating point"""
        self.dominatingSet.append(id2)

    def dominates(self,other):
        """Returns true if self[k]>=other[k] for all k and self[k]>other[k] for at least one k"""
        assert isinstance(other,Datapoint)
        gte=0 # count of self[k]>=other[k]
        gt=0 # count of self[k]>other[k]
        for k in range(len(self.vec)):
            if self.vec[k] >= other.vec[k]:
                gte+=1
                if self.vec[k] > other.vec[k]:
                    gt+=1
            
        return (gte==len(self.vec) and (gt>0))

    def __repr__(self):
        return self.vec.__repr__()+": "+str(self.paretoStatus)
    
def nondominated_sort(dataset):
    """Nondominated Sorting, generates ranking w/ higher number = better pareto front"""

    # pairwise comparisons
    for n in range(len(dataset)):
        for m in range(len(dataset)):
            if dataset[m].dominates(dataset[n]):
                dataset[n].dominatedCount+=1
                dataset[m].addToDominatingSet(n)

    # find first pareto front
    front = []
    front2 = []
    tmpLevel = 10 # temporary value for Pareto level, will re-adjust later
    for n in range(len(dataset)):
        if dataset[n].dominatedCount == 0:
            dataset[n].paretoStatus = tmpLevel
            front.append(n)

    # iteratively peel off pareto fronts
    while len(front) != 0:
        tmpLevel-=1
        for f in front:
            for s in dataset[f].dominatingSet:
                dataset[s].dominatedCount -= 1
                if dataset[s].dominatedCount == 0:
                    front2.append(s)
                    dataset[s].paretoStatus = tmpLevel
        front = front2 
        front2 = []
#    print(front,front2)
    

def create_dataset(path_list,begin_time):
    """Given a list of vectors, create list of datapoints"""
    dataset = []
#    list1=[]
#    list2=[]
#    for k in range(len(raw_vectors)):
#        for n,v in enumerate(raw_vectors[k]):
#            if k == 0:
#                dataset.append(Datapoint(n))
#            dataset[n].addNumber(v)
    for i in range(len(path_list)):
        new_datapoint = Datapoint(i)
        obj1,obj2 = PathObj(path_list[i],begin_time)
        new_datapoint.addNumber(obj1)
        new_datapoint.addNumber(obj2)
#        list1.append(obj1)
#        list2.append(obj2)
        dataset.append(new_datapoint)  
#    print(dataset)    
    return dataset

def OptimizePath(path_list,begin_time):
    dataset = create_dataset(path_list,begin_time)
    nondominated_sort(dataset)
    print("After sorting, we got this dataset:")
    print("-----------")
    print(dataset)
    
    pareto_list=[]
    for i in range(len(dataset)):
        pareto_list.append(dataset[i].paretoStatus)
    for i in pareto_list:
        minpos = pareto_list.index(min(pareto_list)) 
    print("Best_path is:", path_list[minpos])
    print("The total travel time and the risk are:", dataset[minpos])
    return (pareto_list,dataset)


