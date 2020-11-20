from .Constants import *
from .Population import Population

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

class M3GP:
	population = None

	def __init__(self):
		pass

	def fit(self,Tr_X, Tr_Y, Te_X=None, Te_Y=None):
		setTerminals(Tr_X.columns)
		Tr_X["Class"] = Tr_Y
		Tr_X = [ list(sample) for sample in Tr_X.iloc]
		Te_X["Class"] = Te_Y
		Te_X = [ list(sample) for sample in Te_X.iloc]
		setTrainingSet(Tr_X)
		setTestSet(Te_X)

		self.population = Population()
		self.population.train()
		self.getBestIndividual().prun()

	def predict(self, dataset):
		'''
		Returns the predictions for the samples in a dataset.
		'''
		return [self.population.getBestIndividual().predict(sample) for sample in dataset]

	def getBestIndividual(self):
		'''
		Returns the final M3GP model.
		'''
		return self.population.getBestIndividual()

	def getAccuracyOverTime(self):
		'''
		Returns the training and test accuracy of the best model in each generation.
		'''
		return [self.population.getTrainingAccuracyOverTime(), self.population.getTestAccuracyOverTime()]

	def getWaFOverTime(self):
		'''
		Returns the training and test WAF of the best model in each generation.
		'''
		return [self.population.getTrainingWaFOverTime(), self.population.getTestWaFOverTime()]

	def getKappaOverTime(self):
		'''
		Returns the training and test kappa values of the best model in each generation.
		'''
		return [self.population.getTrainingKappaOverTime(), self.population.getTestKappaOverTime()]

	def getSizesOverTime(self):
		'''
		Returns the size and number of dimensions of the best model in each generation.
		'''
		return [self.population.getSizeOverTime(), self.population.getNumberOfDimensionsOverTime()]

	def getGenerationTimes(self):
		'''
		Returns the time spent in each generation.
		'''
		return self.population.getGenerationTimes()