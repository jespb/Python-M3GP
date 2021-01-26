from .Node import Node
from .Constants import *
from .Util import *
from .MahalanobisDistanceClassifier import MahalanobisDistanceClassifier
from .EuclideanDistanceClassifier import EuclideanDistanceClassifier

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


	fitness = None

	model_name = ["MahalanobisDistanceClassifier", "EuclideanDistanceClassifier"][0]
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


	def trainModel(self):
		'''
		Trains the classifier which will be used in the fitness function
		'''
		if self.model == None:
			if self.model_name == "MahalanobisDistanceClassifier":
				self.model = MahalanobisDistanceClassifier()
			if self.model_name == "EuclideanDistanceClassifier":
				self.model = EuclideanDistanceClassifier()
			

			ds = getTrainingSet()
			X = [s[:-1] for s in ds]
			hyper_X = self.convert(X)
			Y = [s[-1] for s in ds]
			self.model.fit(hyper_X,Y)




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



	def getTrainingPredictions(self):
		'''
		Returns the individual's training predictions.
		'''
		self.trainModel()
		if self.trainingPredictions == None:
			X = [sample[:-1] for sample in getTrainingSet() ]
			self.trainingPredictions = self.predict(X)
	
		return self.trainingPredictions

	def getTestPredictions(self):

		'''
		Returns the individual's test predictions.
		'''
		self.trainModel()
		if self.testPredictions == None:
			X = [sample[:-1] for sample in getTestSet() ]
			self.testPredictions = self.predict(X)

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

	def convert(self, X):
		'''
		Returns the converted input space.
		'''
		return [self.calculate(sample) for sample in X]


	def predict(self, X):
		'''
		Returns the class prediction of a sample.
		'''
		if self.model == None:
			self.trainModel()
			
		hyper_X = self.convert(X)
		predictions = self.model.predict(hyper_X)

		return predictions



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
		self.model = None

		if simp:
			# Simplify dimensions
			for d in self.dimensions:
				done = False
				while not done:
					state = str(d)
					d.prun()
					done = state == str(d)

