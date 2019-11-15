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

	def __init__(self, panda_ds):
		terminals = ["X"+str(i) for i in range(len(panda_ds.iloc[0]) - 1 )]
		setTerminals(terminals)

		if SHUFFLE:
			panda_ds = panda_ds.sample(frac=1)
		train_ds_size = int(panda_ds.shape[0]*TRAIN_FRACTION)
		
		train_ds = []
		for i in range(train_ds_size):
			train_ds.append(list(panda_ds.iloc[i]))
		test_ds = []
		for i in range(train_ds_size, panda_ds.shape[0]):
			test_ds.append(list(panda_ds.iloc[i]))
		setTrainingSet(train_ds)
		setTestSet(test_ds)

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