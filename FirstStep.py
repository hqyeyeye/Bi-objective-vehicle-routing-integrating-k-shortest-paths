# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 08:41:28 2021

@author: huqio
"""

"The implementation is largely influenced by the Yen's algorithm in Wikipedia\
and beegeesquare's implementation on github"

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
    
#redefine the network and find the total risk for each path    
#G_network_distance

#get the risk for a certain path

#getEdge and drawP are for drawing
def getEdge(p):
   draw_edge = []
   for i in range(len(p)-1):
       a = (p[i],p[i+1])
       draw_edge.append(a)
   return draw_edge


def drawP(G_network,p,pos):
#    c,p = nx.single_source_dijkstra(G_network,"Ann_Arbor","Seattle")
    #print(p)
#    pos = nx.spring_layout(G_network)
    draw_edge = getEdge(p)      
    nx.draw_networkx_nodes(G_network, pos,
                           node_size=100,
                           alpha=0.8)
    nx.draw_networkx_nodes(G_network, pos,nodelist=p,
                           node_size=100,
                           alpha=0.8)
    nx.draw_networkx_edges(G_network, pos, width=1, alpha=0.5)
    nx.draw_networkx_edges(G_network, pos, edgelist=draw_edge, \
                           width=5, alpha=0.5,edge_color='r')
    nx.draw_networkx_labels(G_network, pos,font_size=25)
#    plt.show()
#    name = ""
#    a = name.join(p)
#    t = "{}"


#    plt.close()

# Yen's algorithm for K-shortest paths in an edge-weighted graph G (undirected
# or directed)

# Cost/weight of path p in graph G
def pweight(G,p):
    w = 0;
    for i in range(len(p)-1): 
#        print(p[i])
        w += G[p[i]][p[i+1]]['weight'];
    return w

    
        

# Copy edge (a,z) of G, remove it, and return the copy.
# This can become expensive!
def cprm(G,a,z):
    ec = G[a][z]['weight'];
    G.remove_edge(a,z);
    return (a,z,ec)

# Copy node n of G, remove it, and return the copy.
# This can become expensive!
def cprmnode(G,n):
    ec = deepcopy(G[n]);
    G.remove_node(n);
    return (n,ec)

# K shortest paths in G from 'source' to 'target'
def yen(G,source,target,K):
    # Determine the shortest path from the source to the sink.
    (c,p) = nx.single_source_dijkstra(G,source,target);
    A = [p];  A_cost = [c];
    # Initialize the set to store the potential kth shortest path.
    B = queue.PriorityQueue();

    for k in range(1,K):
        # The spur node ranges from the first node to the next to last node in the previous k-shortest path.
        for i in range(len(A[k-1])-1):
            
            # Spur node is retrieved from the previous k-shortest path, k − 1.
            sn = A[k-1][i];
            # The sequence of nodes from the source to the spur node of the previous k-shortest path.
            rp = A[k-1][:i];
            
            # We store the removed edges
            removed_edges = [];  removed_root_edges = [];  removed_root_nodes=[];
            # Remove the root paths

            # for each node rootPathNode in rootPath except spurNode:
            #   remove rootPathNode from Graph;
            for j in range(len(rp)):
                
                
                extra_edges = deepcopy(G.edges(rp[j]));
                
                for eg in extra_edges:
                  
                    src=eg[0];
                    tgt=eg[1];
                    removed_root_edges.append(cprm(G,src,tgt));
              
                removed_root_nodes.append(cprmnode(G,rp[j]));



            erp = A[k-1][:i+1];  # extended root path
            for p in A:
                if erp == p[:i+1] and G.has_edge(p[i],p[i+1]):
                    removed_edges.append(cprm(G,p[i],p[i+1]));
            # The spur path
            DONE = 0
            try:
                (csp,sp) = nx.single_source_dijkstra(G,sn,target)
            except:
                # there is no spur path if sn is not connected to the target
                sp = [];  csp = None; DONE = 1;
                #return (A, A_cost)
            # Add back the edges that were removed
            for nd in removed_root_nodes: G.add_node(nd[0]);
            for re in removed_root_edges: G.add_edge(re[0],re[1],weight=re[2]);
            for re in removed_edges: G.add_edge(re[0],re[1],weight=re[2]);
            if len(sp) > 0:
                # The potential k-th shortest path (the root path may be empty)
                pk = rp + sp;
#                print(pk)
                cpk = pweight(G,pk);
                # Add the potential k-shortest path to the heap
                B.put((cpk,pk));
            


        if B.empty():
            print ('There are only', k, 'shortest paths for this pair');
            break;
        # The shortest path in B that is not already in A is the new k-th shortest path
        while not B.empty():
            cost, path = B.get();
            if path not in A:
                A.append(path);
                A_cost.append(cost);
                break;

    return (A, A_cost)





#src='Nashville';
#tgt='Gary';
#k=100;
#
#k_path, path_costs=yen(G_network,src,tgt,k);
#print("Possible paths:",k_path)
#print("Distance for each path:",path_costs)
