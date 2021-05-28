from .Node import Node
from .MahalanobisDistanceClassifier import MahalanobisDistanceClassifier

import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import cohen_kappa_score


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#

class Individual:
	training_X = None
	training_Y = None

	operators = None
	terminals = None
	max_depth = None

	dimensions = None
	size = 0
	depth = 0

	trainingPredictions = None
	testPredictions = None
	fitness = None

	model_name = ["MahalanobisDistanceClassifier"][0]
	model = None

	fitnessType = ["Accuracy", "WAF"][0]

	def __init__(self, operators, terminals, max_depth):
		self.operators = operators
		self.terminals = terminals
		self.max_depth = max_depth

	def create(self,n_dims=1):
		self.dimensions = []
		for i in range(n_dims):
			n = Node()
			n.create(self.operators, self.terminals, self.max_depth, full=True)
			self.dimensions.append(n)
		
	def copy(self, dim):
		self.dimensions = dim



	def __gt__(self, other):
		sf = self.getFitness()
		sd = self.getNumberOfDimensions()
		ss = self.getSize()

		of = other.getFitness()
		od = other.getNumberOfDimensions()
		os = other.getSize()

		return (sf > of) or \
				(sf == of and sd < od) or \
				(sf == of and sd == od and ss < os)

	def __ge__(self, other):
		return self.getFitness() >= other.getFitness()

	def __str__(self):
		return ",".join([str(d) for d in self.dimensions])


	def fit(self, Tr_x, Tr_y):
		'''
		Trains the classifier which will be used in the fitness function
		'''
		if self.model is None:
			self.training_X = Tr_x
			self.training_Y = Tr_y

			if self.model_name == "MahalanobisDistanceClassifier":
				self.model = MahalanobisDistanceClassifier()
			if self.model_name == "EuclideanDistanceClassifier":
				self.model = RidgeClassifierCV()
			

			hyper_X = self.convert(Tr_x)

			self.model.fit(hyper_X,Tr_y)


	def getSize(self):
		'''
		Returns the total number of nodes within an individual.
		'''
		if not self.size:
			self.size = sum(n.getSize() for n in self.dimensions)
		return self.size

	def getDepth(self):
		'''
		Returns the depth of individual.
		'''
		if not self.depth:
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
		if self.fitness is None:
			self.getTrainingPredictions()

			if self.fitnessType == "Accuracy":
				acc = accuracy_score(self.trainingPredictions, self.training_Y)
				self.fitness = acc 

			if self.fitnessType == "WAF":
				waf = f1_score(self.trainingPredictions, self.training_Y, average="weighted")
				self.fitness = waf 

		return self.fitness


	def getTrainingPredictions(self):
		if self.trainingPredictions is None:
			self.trainingPredictions = self.predict(self.training_X)

		return self.trainingPredictions

	def getTestPredictions(self, X):
		if self.testPredictions is None:
			self.testPredictions = self.predict(X)

		return self.testPredictions


	
	def getAccuracy(self, X,Y,pred=None):
		'''
		Returns the individual's accuracy.
		'''
		if pred == "Tr":
			pred = self.getTrainingPredictions()
		elif pred == "Te":
			pred = self.getTestPredictions(X)
		else:
			pred = self.predict(X)

		return accuracy_score(pred, Y)


	def getWaF(self, X, Y,pred=None):
		'''
		Returns the individual's WAF.
		'''
		if pred == "Tr":
			pred = self.getTrainingPredictions()
		elif pred == "Te":
			pred = self.getTestPredictions(X)
		else:
			pred = self.predict(X)

		return f1_score(pred, Y, average="weighted")


	def getKappa(self, X, Y,pred=None):
		'''
		Returns the individual's kappa value.
		'''
		if pred == "Tr":
			pred = self.getTrainingPredictions()
		elif pred == "Te":
			pred = self.getTestPredictions(X)
		else:
			pred = self.predict(X)

		return cohen_kappa_score(pred, Y)



	def calculate(self, sample):
		'''
		Return the position of a sample in the output space.
		'''
		return [self.dimensions[i].calculate(sample) for i in range(len(self.dimensions))]


	def convert(self, X):
		'''
		Returns the converted input space.
		'''
		ret = pd.DataFrame()
		for i in range(len(self.dimensions)):
			a = self.dimensions[i].calculate(X)
			ret["#"+str(i)] = a
		return ret


	def predict(self, X):
		'''
		Returns the class prediction of a sample.
		'''
			
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
		ind = Individual(self.operators, self.terminals, self.max_depth)
		ind.copy(dup)
		ind.fit(self.training_X, self.training_Y)

		while i < len(dup) and len(dup) > 1:
			dup2 = dup[:]
			dup2.pop(i)
			ind2 = Individual(self.operators, self.terminals, self.max_depth)
			ind2.copy(dup2)
			ind2.fit(self.training_X, self.training_Y)

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
		self.fit(self.training_X, self.training_Y)


		if simp:
			# Simplify dimensions
			for d in self.dimensions:
				done = False
				while not done:
					state = str(d)
					d.prun(self.training_X)
					done = state == str(d)



