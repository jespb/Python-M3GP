import numpy as np

from copy import deepcopy

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

def getInverseCovarianceMatrix(cluster):
	ret = []
	for i in range(len(cluster[0])):
		ret.append([0]*len(cluster[0]))
	for d1 in range(len(cluster[0])):
		for d2 in range(len(cluster[0])):
			for x in range(len(cluster)):
				ret[d1][d2] += cluster[x][d1]*cluster[x][d2]/len(cluster)
	return np.array(inverseMatrix(ret))

def distance(v1,v2,invCovarianceMatrix):
	dist = 2
	if dist == 1:
		return euclideanDistance(v1,v2)
	else:
		return mahalanobisDistance(v1,v2,invCovarianceMatrix)

def euclideanDistance(v1,v2):
	return sum([(v1[i]-v2[i])**2 for i in range(len(v1))])**0.5

def mahalanobisDistance(v1,v2,invCovarianceMatrix):
	x = np.array(v1)
	y = np.array(v2)

	sub = np.subtract(x,y)
	mult = np.matmul(sub,invCovarianceMatrix)
	if (len(invCovarianceMatrix)==1):
		mult = [mult]
	mult2 = np.matmul(mult,sub.transpose())
	if(mult2 < 0):
		return euclideanDistance(v1,v2)

	return mult2**0.5


def inverseMatrix(m):
	m = deepcopy(m)
	n = len(m)
	inv = np.eye(n)
	d = 0

	for i in range(n):
		if m[i][i]==0:
			for k in range(i+1,n):
				if m[k][i] != 0:
					tmp = m[i]
					m[i] = m[k]
					m[k] = tmp

					tmp = inv[i]
					inv[i] = inv[k]
					inv[k] = tmp

					break
		if m[i][i] == 0:
			return np.eye(n)

		for y in range(i+1,n):
			d = -m[y][i] / m[i][i]
			for k in range(n):
				inv[y][k] += inv[i][k]*d
				m[y][k] += m[i][k]*d

	if m[n-1][n-1] == 0:
		return np.eye(n)

	for i in range(n):
		d = m[i][i]
		for k in range(n):
			inv[i][k] /= d 
			m[i][k] /= d 

	for x in range(n-1,0,-1):
		for y in range(x-1,-1,-1):
			d =  -m[y][x]
			for k in range(n):
				inv[y][k] += inv[x][k] * d 
			m[y][x] += m[x][x] * d 
	return inv