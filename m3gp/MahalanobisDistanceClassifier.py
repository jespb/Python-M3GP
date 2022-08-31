import numpy as np

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2022 J. E. Batista
#

#
#   This classifier receives panda DataFrames and converts it to standard types
# to avoid "Infinite" values in the matrices.
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
	return inverseMatrix(ret)
	
def mahalanobisDistance(v1,v2,invCovarianceMatrix):
	'''
	Returns the mahalanobis distance between two points
	'''
	if invCovarianceMatrix is None:
		return euclideanDistance(v1,v2)

	x = np.array(v1)
	y = np.array(v2)

	sub = np.subtract(x,y)
	mult = np.matmul(sub,invCovarianceMatrix)
	if (len(invCovarianceMatrix)==1):
		mult = [mult]
	mult2 = np.matmul(mult,sub.transpose())

	if(mult2 < 0):
		#print("mult2 < 0")
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
		return None



class MahalanobisDistanceClassifier:

	invCovarianceMatrix = None
	classCentroids = None
	classes = None

	def __init__(self):
		pass

	def fit(self,X,Y):
		'''
		Calculates the class clusters in the output space.
		'''
		if self.invCovarianceMatrix != None:
			return

		X = [ list(sample) for sample in X.iloc ]
		Y = list(Y)

		self.classes = list(set(Y))
		clusters = []
		for i in self.classes:
			clusters.append([])

		for sample_index in range(len(X)):
			index = self.classes.index(Y[sample_index])
			coor = X[sample_index]
			clusters[index].append(coor)

		self.invCovarianceMatrix = []
		for cluster in clusters:
			m = getInverseCovarianceMatrix(cluster)
			self.invCovarianceMatrix.append(m)

		self.classCentroids = []
		for cluster in clusters:
			self.classCentroids.append([0 for i in range(len(cluster[0]))])
			for sample in cluster:
				self.classCentroids[-1] = [self.classCentroids[-1][i] + sample[i]/len(cluster) for i in range(len(self.classCentroids[-1]))]



	def predict(self, X):		
		predictions = []
		X = [ list(sample) for sample in X.iloc ]

		for sample in X:
			pick_d = mahalanobisDistance(sample, self.classCentroids[0],self.invCovarianceMatrix[0])
			pick = self.classes[0]
		
			for i in range(len(self.classes)):
				d = mahalanobisDistance(sample, self.classCentroids[i],self.invCovarianceMatrix[i])
				if d < pick_d:
					pick_d = d
					pick = self.classes[i]
		
			predictions.append(pick)
		return predictions