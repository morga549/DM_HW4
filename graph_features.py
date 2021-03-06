import sys
import numpy as np
from collections import Counter
from functools import reduce
import matplotlib.pyplot as plt

infile = sys.argv[1]
file = open(infile, 'r')

#find the largest node in the graph
maxNode = 0
for line in file:
    u,v = line.split()
    if(int(u) > maxNode): maxNode = int(u)
    if(int(v) > maxNode): maxNode = int(v)
file.close()

# build adjacency matrix of graph
adjMatrix = np.zeros((maxNode, maxNode), dtype = np.int)

# fill the adjacency matrix
file = open(infile, 'r')
for line in file:
    u,v = line.split()
    iu = int(u) - 1
    iv = int(v) - 1
    adjMatrix[iu][iv] = 1
    adjMatrix[iv][iu] = 1
file.close()

# calculates the degree distribution of a graph
def degreeDist(matrix):
    nodeDegrees = reduce(lambda x,y: x+y, matrix[:]) # list containing the degree of each node in the graph
    frequencies = Counter(nodeDegrees).values() # get the frequencies of each degree
    keys = Counter(nodeDegrees).keys() # degree associated with each frequency
    plt.scatter(keys, frequencies)
    plt.show()

    probabilies = [(float(x) / sum(frequencies)) for x in frequencies] # list containing the probabilies of each degree frequency
    plt.scatter(keys, probabilies)
    plt.xscale('log')
    plt.yscale('log')
    plt.show()
    return zip(keys, frequencies)

# calculates the clustering Coefficient of a graph
def clusteringCoeff(matrix):
    friends = []

    for row in matrix[:]:
         friends.append(np.where(row == 1)) # list of neighbors for each node

    globalCC = 0.0

    for node in friends:
        degree = len(node[0]) # number of neighbors you have
        triangles = 0 # of connections between neighbors

        for x in node[0]:
            triangles += len(np.intersect1d(friends[x][0], node[0]))
        if(degree > 1):
            localCC = float(triangles) / (degree * (degree - 1)) # Clustering Coefficient of the current node
            globalCC += localCC

    globalCC /= matrix[0].shape[0] # average Clustering Coefficient of the graph
    return globalCC

print "Clustering Coefficient: "
print clusteringCoeff(adjMatrix)
print "\n\nDegree Distribution: "
print degreeDist(adjMatrix)
