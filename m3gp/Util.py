import numpy as np
from sklearn.neighbors import DistanceMetric


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
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


def mahalanobisDistance_fromDistanceMetric(v1,v2,invCovarianceMatrix):
	'''
	Returns the mahalanobis distance between two points
	'''
	return DistanceMetric.get_metric('mahalanobis', VI = invCovarianceMatrix)
	
def mahalanobisDistance(v1,v2,invCovarianceMatrix):
	'''
	Returns the mahalanobis distance between two points
	'''
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

def euclideanDistance(v1,v2):
	return sum([(v1[i]-v2[i])**2 for i in range(len(v1))])**0.5


def inverseMatrix(m):
	'''
	Returns the inverse of the matrix m, if possible,
	otherwise returns the diagonal matrix
	'''
	try:
		return np.linalg.inv(np.array(m))
	except:
		return np.eye( len(m) )
