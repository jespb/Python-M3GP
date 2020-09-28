from .Node import Node
from .Constants import *
from .Util import *

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score



# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

class Individual:
	trainingPredictions = None
	testPredictions = None

	size = None
	depth = None

	dimensions = None

	invCovarianceMatrix = None
	classCentroids = None
	classes = None

	fitness = None

	model = None


	fitnessType = ["Accuracy", "WAF"][0]

	def __init__(self, dim = None):
		if dim == None:
			self.dimensions = [Node(full=True)]
		else:
			self.dimensions = dim

	def __gt__(self, other):
		sf = self.getFitness()
		sd = len(self.getDimensions())
		ss = self.getSize()

		of = other.getFitness()
		od = len(other.getDimensions())
		os = other.getSize()

		return (sf > of) or \
				(sf == of and sd < od) or \
				(sf == of and sd == od and ss < os)

	def __ge__(self, other):
		return self.getFitness() >= other.getFitness()

	def __str__(self):
		return ",".join([str(d) for d in self.dimensions])



	def getSize(self):
		'''
		Returns the total number of nodes within an individual.
		'''
		if self.size == None:
			self.size = sum(n.getSize() for n in self.dimensions)
		return self.size

	def getDepth(self):
		'''
		Returns the depth of individual.
		'''
		if self.depth == None:
			self.depth = max([dimension.getDepth() for dimension in self.dimensions])
		return self.depth 

	def getDimensions(self):
		'''
		Returns a deep clone of the individual's list of dimensions.
		'''
		ret = []
		for dim in self.dimensions:
			ret.append(dim.clone())
		return ret


	def getNumberOfDimensions(self):
		'''
		Returns the total number of dimensions within the individual.
		'''
		return len(self.dimensions)



	def getFitness(self):
		'''
		Returns the individual's fitness.
		'''
		if self.fitness == None:
			if self.fitnessType == "Accuracy":
				acc = self.getTrainingAccuracy()
				self.fitness = acc 

			if self.fitnessType == "WAF":
				waf = self.getTrainingWaF()
				self.fitness = waf 

		return self.fitness

	def getTrainingPredictions(self,ds=None):
		'''
		Returns the individual's training predictions.
		'''
		if self.trainingPredictions == None:
			if ds == None:
				ds = getTrainingSet()

			self.makecluster(ds)
			
			self.trainingPredictions = self.predict_all(ds)
	
		return self.trainingPredictions

	def getTestPredictions(self):

		'''
		Returns the individual's test predictions.
		'''
		if self.testPredictions == None:
			self.makecluster()
			ds = getTestSet()
			self.testPredictions = self.predict_all(ds)

		return self.testPredictions


	def getTrainingAccuracy(self):
		'''
		Returns the individual's training accuracy.
		'''
		self.getTrainingPredictions()

		ds = getTrainingSet()
		y = [ str(s[-1]) for s in ds]
		return accuracy_score(self.trainingPredictions, y)
	
	def getTestAccuracy(self):
		'''
		Returns the individual's test accuracy.
		'''
		self.getTestPredictions()

		ds = getTestSet()
		y = [ str(s[-1]) for s in ds]
		return accuracy_score(self.testPredictions, y)

	def getTrainingWaF(self):
		'''
		Returns the individual's training WAF.
		'''
		self.getTrainingPredictions()

		ds = getTrainingSet()
		y = [ str(s[-1]) for s in ds]
		return f1_score(self.trainingPredictions, y, average = "weighted")

	def getTestWaF(self):
		'''
		Returns the individual's test WAF.
		'''
		self.getTestPredictions()

		ds = getTestSet()
		y = [ str(s[-1]) for s in ds]
		return f1_score(self.testPredictions, y, average="weighted")

	def getTrainingKappa(self):
		'''
		Returns the individual's training kappa value.
		'''
		self.getTrainingPredictions()

		ds = getTrainingSet()
		y = [ str(s[-1]) for s in ds]
		return cohen_kappa_score(self.trainingPredictions, y)

	def getTestKappa(self):
		'''
		Returns the individual's test kappa value.
		'''
		self.getTestPredictions()

		ds = getTestSet()
		y = [ str(s[-1]) for s in ds]
		return cohen_kappa_score(self.testPredictions, y)



	def calculate(self, sample):
		'''
		Return the position of a sample in the output space.
		'''
		return [self.dimensions[i].calculate(sample) for i in range(len(self.dimensions))]

	def predict(self, sample):
		'''
		Returns the class prediction of a sample.
		'''
		pred = self.calculate(sample)

		pick_d = mahalanobisDistance(pred, self.classCentroids[0],self.invCovarianceMatrix[0])
		pick = self.classes[0]
		
		for i in range(len(self.classes)):
			d = mahalanobisDistance(pred, self.classCentroids[i],self.invCovarianceMatrix[i])
			if d < pick_d:
				pick_d = d
				pick = self.classes[i]
		
		return pick

	def predict_all(self, dataset):
		'''
		Returns the class predictions of the samples in a dataset.
		'''
		return [ self.predict(s) for s in dataset]



	def makecluster(self, ds = None):
		'''
		Calculates the class clusters in the output space.
		'''
		if self.invCovarianceMatrix != None:
			return

		if ds == None:
			ds = getTrainingSet()

		self.classes = []
		clusters = []
		for sample in ds:
			if not str(sample[-1]) in self.classes:
				self.classes.append(str(sample[-1]))
				clusters.append([])

		for sample in ds:
			index = self.classes.index(str(sample[-1]))
			coor = self.calculate(sample)
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


	def prun(self,simp=True):
		'''
		Remove the dimensions that degrade the fitness.
		If simp==True, also simplifies each dimension.
		'''
		dup = self.dimensions[:]
		i = 0
		ind = Individual(dup)

		while i < len(dup) and len(dup) > 1:
			dup2 = dup[:]
			dup2.pop(i)
			ind2 = Individual(dup2)

			if ind2 >= ind:
				ind = ind2
				dup = dup2
				i-=1
			i+=1
	
		self.dimensions = dup
		self.trainingAccuracy = None
		self.testAccuracy = None
		self.size = None
		self.depth = None
		self.invCovarianceMatrix = None
		self.classCentroids = None
		self.classes = None
		self.makecluster()

		if simp:
			# Simplify dimensions
			for d in self.dimensions:
				done = False
				while not done:
					state = str(d)
					d.prun()
					done = state == str(d)

