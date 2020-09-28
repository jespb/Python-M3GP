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

		self.population = Population()
		self.population.train()
		self.getBestIndividual().prun()

	def predict(self, sample):
		'''
		Returns the predicted class for a sample.
		'''
		return self.population.getBestIndividual().predict(sample)

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