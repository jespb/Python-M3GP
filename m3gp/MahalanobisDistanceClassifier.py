from .Util import *

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


		self.classes = []
		clusters = []
		for sample in Y:
			if not sample in self.classes:
				self.classes.append(sample)
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