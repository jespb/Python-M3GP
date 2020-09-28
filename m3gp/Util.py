import numpy as np
from sklearn.neighbors import DistanceMetric

from copy import deepcopy

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

def getInverseCovarianceMatrix(cluster):
	'''
	Returns the inverse covariance matrix, obtained from a cluster
	'''
	ret = []
	for i in range(len(cluster[0])):
		ret.append([0]*len(cluster[0]))
	for d1 in range(len(cluster[0])):
		for d2 in range(len(cluster[0])):
			for x in range(len(cluster)):
				ret[d1][d2] += cluster[x][d1]*cluster[x][d2]/len(cluster)
	return np.array(inverseMatrix(ret))


def mahalanobisDistance(v1,v2,invCovarianceMatrix):
	'''
	Returns the mahalanobis distance between two points
	'''
	dist = DistanceMetric.get_metric('mahalanobis', VI = invCovarianceMatrix)
	return dist.pairwise([v1,v2])[0][-1]


def inverseMatrix(m):
	'''
	Returns the inverse of the matrix m, if possible,
	otherwise returns the diagonal matrix
	'''
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
