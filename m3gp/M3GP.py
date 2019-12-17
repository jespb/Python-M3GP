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

	def getGen(self):
		return self.population.getCurrentGeneration()

	def getBestIndividual(self):
		return self.population.getBestIndividual()

	def getAccuracyOverTime(self):
		return [self.population.getTrainingAccuracyOverTime(), self.population.getTestAccuracyOverTime()]

	def getSizesOverTime(self):
		return [self.population.getSizeOverTime(), self.population.getNumberOfDimensionsOverTime()]