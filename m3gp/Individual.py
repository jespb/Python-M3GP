from .Node import Node
from .Constants import *
from .Util import *
import pandas as pd
import numpy as np

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

class Individual:
	trainingAccuracy = None
	testAccuracy = None
	size = None
	depth = None

	dimensions = None

	invCovarianceMatrix = None
	classCentroids = None
	classes = None

	def __init__(self, dim = None):
		if dim == None:
			self.dimensions = [Node()]
		else:
			self.dimensions = dim
		self.makecluster()

	def __gt__(self, other):
		betterAccuracy = self.getTrainingAccuracy() >  other.getTrainingAccuracy()
		sameAccuracy = self.getTrainingAccuracy() == other.getTrainingAccuracy()
		hasLessDimensions = len(self.dimensions) < len(other.dimensions)
		return betterAccuracy or (sameAccuracy and hasLessDimensions)

	def __str__(self):
		return ",".join([str(d) for d in self.dimensions])

	def calculate(self, sample):
		return [self.dimensions[i].calculate(sample) for i in range(len(self.dimensions))]

	def predict(self, sample):
		pred = self.calculate(sample)
		pick_d = distance(pred, self.classCentroids[0],self.invCovarianceMatrix[0])
		pick = self.classes[0]
		for i in range(len(self.classes)):
			d = distance(pred, self.classCentroids[i],self.invCovarianceMatrix[i])
			if d < pick_d:
				pick_d = d
				pick = self.classes[i]
		return pick

	def getSize(self):
		if self.size == None:
			self.size = sum(n.getSize() for n in self.dimensions)
		return self.size

	def getDepth(self):
		if self.depth == None:
			self.depth = max([dimension.getDepth() for dimension in self.dimensions])
		return self.depth 

	def getDimensions(self):
		ret = []
		for dim in self.dimensions:
			ret.append(dim.clone())
		return ret

	def getNumberOfDimensions(self):
		return len(self.dimensions)

	def getTrainingAccuracy(self):
		if self.trainingAccuracy == None:
			hits = 0
			ds = getTrainingSet()
			for i in range(len(ds)):
				if self.predict(ds[i]) == str(ds[i][-1]):
					hits += 1
			self.trainingAccuracy = hits/len(ds) 
		return self.trainingAccuracy
	
	def getTestAccuracy(self):
		if self.testAccuracy == None:
			hits = 0
			ds = getTestSet()
			for i in range(len(ds)):
				if self.predict(ds[i]) == str(ds[i][-1]):
					hits += 1
			self.testAccuracy = hits/len(ds) 
		return self.testAccuracy


	def makecluster(self):
		if self.invCovarianceMatrix != None:
			return

		self.classes = []
		clusters = []
		for sample in getTrainingSet():
			if not str(sample[-1]) in self.classes:
				self.classes.append(str(sample[-1]))
				clusters.append([])

		for sample in getTrainingSet():
			index = self.classes.index(str(sample[-1]))
			coor = self.calculate(sample)
			clusters[index].append(coor)

		self.invCovarianceMatrix = []
		for cluster in clusters:
			m = np.array(getInverseCovarianceMatrix(cluster))
			self.invCovarianceMatrix.append(m)

		self.classCentroids = []
		for cluster in clusters:
			self.classCentroids.append([0 for i in range(len(cluster[0]))])
			for sample in cluster:
				self.classCentroids[-1] = [self.classCentroids[-1][i] + sample[i]/len(cluster) for i in range(len(self.classCentroids[-1]))]
