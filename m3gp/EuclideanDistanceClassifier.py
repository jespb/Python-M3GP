from .Util import *

class EuclideanDistanceClassifier:

	classCentroids = None
	classes = None

	def __init__(self):
		pass

	def fit(self,X,Y):
		'''
		Calculates the class clusters in the output space.
		'''

		self.classes = []
		clusters = []
		for sample in Y:
			if not str(sample) in self.classes:
				self.classes.append(str(sample))
				clusters.append([])

		for sample_index in range(len(X)):
			index = self.classes.index(str(Y[sample_index]))
			coor = X[sample_index]
			clusters[index].append(coor)


		self.classCentroids = []
		for cluster in clusters:
			self.classCentroids.append([0 for i in range(len(cluster[0]))])
			for sample in cluster:
				self.classCentroids[-1] = [self.classCentroids[-1][i] + sample[i]/len(cluster) for i in range(len(self.classCentroids[-1]))]



	def predict(self, X):		
		predictions = []
		for sample in X:

			pick_d = euclideanDistance(sample, self.classCentroids[0])
			pick = self.classes[0]
		
			for i in range(len(self.classes)):
				d = euclideanDistance(sample, self.classCentroids[i])
				if d < pick_d:
					pick_d = d
					pick = self.classes[i]
		
			predictions.append(pick)
		return predictions