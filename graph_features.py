import sys
import numpy as np
from collections import Counter
from functools import reduce

infile = sys.argv[1]
file = open(infile, 'r')

#find the largest node in the graph
maxNode = 0
for line in file:
    u,v = line.split()
    if(int(u) > maxNode): maxNode = int(u)
    if(int(v) > maxNode): maxNode = int(v)
file.close()

#build a list of lists representing an adjacency matrix
adjMatrix = np.zeros((maxNode, maxNode), dtype = np.int)

file = open(infile, 'r')
for line in file:
    u,v = line.split()
    iu = int(u) - 1
    iv = int(v) - 1
    adjMatrix[iu][iv] = 1
    adjMatrix[iv][iu] = 1
file.close()

def degreeDist(matrix):
    nodeDegrees = reduce(lambda x,y: x+y, matrix[:])
    frequencies = Counter(nodeDegrees).values()
    keys = Counter(nodeDegrees).keys()
    return zip(keys, frequencies)

def clusteringCoeff(matrix):
    friends = []

    for row in matrix[:]:
         friends.append(np.where(row == 1))

    globalCC = 0.0

    for node in friends:
        degree = len(node[0])
        triangles = 0

        for x in node[0]:
            triangles += len(np.intersect1d(friends[x][0], node[0]))
        if(degree > 1):
            localCC = float(triangles) / (degree * (degree - 1))
            globalCC += localCC

    globalCC /= matrix[0].shape[0]
    return globalCC

print "Clustering Coefficient: "
print clusteringCoeff(adjMatrix)
print "\n\nDegree Distribution: "
print degreeDist(adjMatrix)
