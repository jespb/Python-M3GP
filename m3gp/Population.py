from .Individual import Individual
from .GeneticOperators import getElite, getOffspring, discardDeep
import multiprocessing as mp
import time

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#

class Population:
	operators = None
	max_depth = None
	population_size = None
	max_generation = None
	tournament_size = None
	elitism_size = None
	limit_depth = None
	verbose = None
	threads = None
	terminals = None


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

	generationTimes = None

	dim_max = None
	dim_evol = None


	def __init__(self, Tr_x, Tr_y, Te_x, Te_y, operators, max_depth, population_size,
		max_generation, tournament_size, elitism_size, limit_depth, dim_init, 
		dim_max, dim_evol, threads, verbose):

		self.Tr_x = Tr_x
		self.Tr_y = Tr_y
		self.Te_x = Te_x
		self.Te_y = Te_y

		self.terminals = list(Tr_x.columns)
		self.operators = operators
		self.max_depth = max_depth
		self.population_size = population_size
		self.max_generation = max_generation
		self.tournament_size = tournament_size
		self.elitism_size = elitism_size
		self.limit_depth = limit_depth
		self.threads = threads
		self.verbose = verbose

		self.dim_max = dim_max
		self.dim_evol = dim_evol

		self.population = []

		while len(self.population) < self.population_size:
			ind = Individual(self.operators, self.terminals, self.max_depth)
			ind.create(n_dims = dim_init)
			self.population.append(ind)

		self.bestIndividual = self.population[0]
		self.bestIndividual.fit(self.Tr_x, self.Tr_y)


		if not self.Te_x is None:
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
		'''
		Returns True if the stopping criteria was reached.
		'''
		genLimit = self.currentGeneration >= self.max_generation
		perfectTraining = self.bestIndividual.getFitness() == 1
		
		return genLimit  or perfectTraining


	def train(self):
		'''
		Training loop for the algorithm.
		'''
		if self.verbose:
			print("> Running log:")

		while self.currentGeneration < self.max_generation:
			if not self.stoppingCriteria():
				t1 = time.time()
				self.nextGeneration()
				t2 = time.time()
				duration = t2-t1
			else:
				duration = 0
			self.currentGeneration += 1
			
			if not self.Te_x is None:
				self.trainingAccuracyOverTime.append(self.bestIndividual.getAccuracy(self.Tr_x, self.Tr_y, pred="Tr"))
				self.testAccuracyOverTime.append(self.bestIndividual.getAccuracy(self.Te_x, self.Te_y, pred="Te"))
				self.trainingWaFOverTime.append(self.bestIndividual.getWaF(self.Tr_x, self.Tr_y, pred="Tr"))
				self.testWaFOverTime.append(self.bestIndividual.getWaF(self.Te_x, self.Te_y, pred="Te"))
				self.trainingKappaOverTime.append(self.bestIndividual.getKappa(self.Tr_x, self.Tr_y, pred="Tr"))
				self.testKappaOverTime.append(self.bestIndividual.getKappa(self.Te_x, self.Te_y, pred="Te"))
				self.sizeOverTime.append(self.bestIndividual.getSize())
				self.dimensionsOverTime.append(self.bestIndividual.getNumberOfDimensions())
				self.generationTimes.append(duration)

		if self.verbose:
			print()



	def nextGeneration(self):
		'''
		Generation algorithm: the population is sorted; the best individual is pruned;
		the elite is selected; and the offspring are created.
		'''
		begin = time.time()
		
		# Calculates the accuracy of the population using multiprocessing
		if self.threads > 1:
			with mp.Pool(processes= self.threads) as pool:
				model = pool.map(fitIndividuals, [(ind, self.Tr_x, self.Tr_y) for ind in self.population] )
				for i in range(len(self.population)):
					self.population[i].model = model[i][0]
					self.population[i].trainingPredictions = model[i][1]
					self.population[i].training_X = self.Tr_x
					self.population[i].training_Y = self.Tr_y
		else:
			[ ind.fit(self.Tr_x, self.Tr_y) for ind in self.population]
			[ ind.getFitness() for ind in self.population ]

		# Sort the population from best to worse
		self.population.sort(reverse=True)


		# Update best individual
		if self.population[0] > self.bestIndividual:
			self.bestIndividual = self.population[0]
			if self.dim_evol != "fixed":
				self.bestIndividual.prun(simp=False)

		# Generating Next Generation
		newPopulation = []
		newPopulation.extend(getElite(self.population, self.elitism_size))
		while len(newPopulation) < self.population_size:
			offspring = getOffspring(self.population, self.tournament_size, self.dim_max, self.dim_evol)
			offspring = discardDeep(offspring, self.max_depth)
			newPopulation.extend(offspring)
		self.population = newPopulation[:self.population_size]


		end = time.time()

		# Debug
		if self.verbose and self.currentGeneration%5==0:
			if not self.Te_x is None:
				print("   > Gen #"+str(self.currentGeneration)+":  Tr-Acc: "+ "%.6f" %self.bestIndividual.getAccuracy(self.Tr_x, self.Tr_y)+" // Te-Acc: "+ "%.6f" %self.bestIndividual.getAccuracy(self.Te_x, self.Te_y) + " // Time: " + str(end- begin) )
			else:
				print("   > Gen #"+str(self.currentGeneration)+":  Tr-Acc: "+ "%.6f" %self.bestIndividual.getAccuracy(self.Tr_x, self.Tr_y))


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

def fitIndividuals(a):
	ind,x,y = a
	ind.fit(x,y)
	
	return ( ind.model, ind.predict(x) )

def getTrainingPredictions(ind):
	return ind.getTrainingPredictions()
