from .Individual import Individual
from .Constants import *
from .GeneticOperators import getElite, getOffspring

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

class Population:
	population = None
	bestIndividual = None
	currentGeneration = 0

	trainingAccuracyOverTime = None
	testAccuracyOverTime = None
	sizeOverTime = None
	dimensionsOverTime = None


	def __init__(self):
		self.population = []
		while len(self.population) < POPULATION_SIZE:
			self.population.append(Individual())

		self.trainingAccuracyOverTime = []
		self.testAccuracyOverTime = []
		self.sizeOverTime = []
		self.dimensionsOverTime = []


	def stoppingCriteria(self):
		genLimit = self.currentGeneration >= MAX_GENERATION
		perfectTraining = \
				self.bestIndividual != None and \
				self.bestIndividual.getTrainingAccuracy() == 1
		
		return genLimit or perfectTraining


	def train(self):
		while not self.stoppingCriteria():
			self.nextGeneration()
			self.currentGeneration += 1
			self.trainingAccuracyOverTime.append(self.bestIndividual.getTrainingAccuracy())
			self.testAccuracyOverTime.append(self.bestIndividual.getTestAccuracy())
			self.sizeOverTime.append(self.bestIndividual.getSize())
			self.dimensionsOverTime.append(self.bestIndividual.getNumberOfDimensions())
		while self.currentGeneration < MAX_GENERATION:
			self.currentGeneration += 1
			self.trainingAccuracyOverTime.append(self.bestIndividual.getTrainingAccuracy())
			self.testAccuracyOverTime.append(self.bestIndividual.getTestAccuracy())
			self.sizeOverTime.append(self.bestIndividual.getSize())
			self.dimensionsOverTime.append(self.bestIndividual.getNumberOfDimensions())

	def nextGeneration(self):
		# Sort the population from best to worse
		self.population.sort(reverse=True)

		# Update best individual
		if(self.bestIndividual == None or self.bestIndividual<self.population[0]):
			self.bestIndividual = self.population[0]

		# Generating Next Generation
		newPopulation = []
		newPopulation.extend(getElite(self.population))
		while len(newPopulation) < POPULATION_SIZE:
			newPopulation.extend(getOffspring(self.population))
		self.population = newPopulation[:POPULATION_SIZE]

		# Debug
		print("Gen #"+str(self.currentGeneration)+":  Training: "+str(self.bestIndividual.getTrainingAccuracy()) +" // Test: "+ str(self.bestIndividual.getTestAccuracy()))


	def predict(self, sample):
		return "Population Not Trained" if self.bestIndividual == None else self.bestIndividual.predict(sample)

	def getBestIndividual(self):
		return self.bestIndividual

	def getCurrentGeneration(self):
		return self.currentGeneration

	def getTrainingAccuracyOverTime(self):
		return self.trainingAccuracyOverTime

	def getTestAccuracyOverTime(self):
		return self.testAccuracyOverTime

	def getSizeOverTime(self):
		return self.sizeOverTime

	def getNumberOfDimensionsOverTime(self):
		return self.dimensionsOverTime
