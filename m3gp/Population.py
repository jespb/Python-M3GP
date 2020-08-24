from .Individual import Individual
from .Constants import *
from .GeneticOperators import getElite, getOffspring
import multiprocessing as mp
import time
import datetime

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
	trainingWaFOverTime = None
	testWaFOverTime = None
	trainingKappaOverTime = None
	testKappaOverTime = None
	sizeOverTime = None
	dimensionsOverTime = None

	generationTime = None


	def __init__(self):
		self.population = []
		while len(self.population) < POPULATION_SIZE:
			self.population.append(Individual())
		self.bestIndividual = self.population[0]

		self.trainingAccuracyOverTime = []
		self.testAccuracyOverTime = []
		self.trainingWaFOverTime = []
		self.testWaFOverTime = []
		self.trainingKappaOverTime = []
		self.testKappaOverTime = []
		self.sizeOverTime = []
		self.dimensionsOverTime = []
		self.generationTimes = []


	def stoppingCriteria(self):
		genLimit = self.currentGeneration >= MAX_GENERATION
		perfectTraining = self.bestIndividual.getFitness() == 1
		
		return genLimit  or perfectTraining


	def train(self):
		if VERBOSE:
			print("> Running log:")

		while self.currentGeneration < MAX_GENERATION:
			
			if not self.stoppingCriteria():
				t1 = time.time()
				self.nextGeneration()
				t2 = time.time()
				duration = t2-t1
			else:
				duration = 0

			self.currentGeneration += 1
			self.trainingAccuracyOverTime.append(self.bestIndividual.getTrainingAccuracy())
			self.testAccuracyOverTime.append(self.bestIndividual.getTestAccuracy())
			self.trainingWaFOverTime.append(self.bestIndividual.getTrainingWaF())
			self.testWaFOverTime.append(self.bestIndividual.getTestWaF())
			self.trainingKappaOverTime.append(self.bestIndividual.getTrainingKappa())
			self.testKappaOverTime.append(self.bestIndividual.getTestKappa())
			self.sizeOverTime.append(self.bestIndividual.getSize())
			self.dimensionsOverTime.append(self.bestIndividual.getNumberOfDimensions())
			self.generationTimes.append(duration)

		if VERBOSE:
			print()



	def nextGeneration(self):
		begin = datetime.datetime.now()
		
		begin = str(begin.hour)+"h"+str(begin.minute)+"m"+str(begin.second)

		# Calculates the accuracy of the population using multiprocessing
		if THREADS > 1:
			with mp.Pool(processes= THREADS) as pool:
				ds = getTrainingSet()
				fitArray = pool.map(getTrainingPredictions, [(ind,ds) for ind in self.population] )
				for i in range(len(self.population)):
					self.population[i].trainingPredictions = fitArray[i][0]
					self.population[i].classes = fitArray[i][1]
					self.population[i].invCovarienceMatrix =fitArray[i][2]
					self.population[i].classCentroids = fitArray[i][3]
	        


		# Sort the population from best to worse
		self.population.sort(reverse=True)

		# Update best individual
		if self.population[0] > self.bestIndividual:
			self.bestIndividual = self.population[0]
			self.bestIndividual.prun(simp=False)

		# Generating Next Generation
		newPopulation = []
		newPopulation.extend(getElite(self.population))
		while len(newPopulation) < POPULATION_SIZE:
			newPopulation.extend(getOffspring(self.population))
		self.population = newPopulation[:POPULATION_SIZE]

		end = datetime.datetime.now()
		end = str(end.hour)+"h"+str(end.minute)+"m"+str(end.second)

		# Debug
		if VERBOSE and self.currentGeneration%5==0:
			print("   > Gen #"+str(self.currentGeneration)+":  Tr-Acc: "+ "%.6f" %self.bestIndividual.getTrainingAccuracy()+" // Te-Acc: "+ "%.6f" %self.bestIndividual.getTestAccuracy() + " // Begin: " + begin + " // End: " + end)


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

	def getTrainingWaFOverTime(self):
		return self.trainingWaFOverTime

	def getTestWaFOverTime(self):
		return self.testWaFOverTime

	def getTrainingKappaOverTime(self):
		return self.trainingKappaOverTime

	def getTestKappaOverTime(self):
		return self.testKappaOverTime

	def getSizeOverTime(self):
		return self.sizeOverTime

	def getNumberOfDimensionsOverTime(self):
		return self.dimensionsOverTime

	def getGenerationTimes(self):
		return self.generationTimes


def calculateIndividualAccuracy_MultiProcessing(ind, fitArray, indIndex):
	fitArray[indIndex] = ind.getTrainingAccuracy()

def getTrainingPredictions(tup):
	ind,ds = tup
	return [ind.getTrainingPredictions(ds), ind.classes, ind.invCovarianceMatrix, ind.classCentroids]
