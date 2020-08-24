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
		return self.population.getBestIndividual().predict(sample)

	def getGen(self):
		return self.population.getCurrentGeneration()

	def getBestIndividual(self):
		return self.population.getBestIndividual()

	def getAccuracyOverTime(self):
		return [self.population.getTrainingAccuracyOverTime(), self.population.getTestAccuracyOverTime()]

	def getWaFOverTime(self):
		return [self.population.getTrainingWaFOverTime(), self.population.getTestWaFOverTime()]

	def getKappaOverTime(self):
		return [self.population.getTrainingKappaOverTime(), self.population.getTestKappaOverTime()]

	def getSizesOverTime(self):
		return [self.population.getSizeOverTime(), self.population.getNumberOfDimensionsOverTime()]

	def getGenerationTimes(self):
		return self.population.getGenerationTimes()