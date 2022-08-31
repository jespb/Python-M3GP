from .Individual import Individual
from .GeneticOperators import getElite, getOffspring, discardDeep
import multiprocessing as mp
import time

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2022 J. E. Batista
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
	rng = None # random number generator
	terminals = None


	population = None
	bestIndividual: Individual = None
	currentGeneration = 0

	fitnessType = None

	trainingAccuracyOverTime = None
	testAccuracyOverTime = None
	trainingWaFOverTime = None
	testWaFOverTime = None
	trainingKappaOverTime = None
	testKappaOverTime = None
	trainingMSEOverTime = None
	testMSEOverTime = None
	sizeOverTime = None
	dimensionsOverTime = None

	generationTimes = None

	dim_min = None
	dim_max = None


	def __init__(self, Tr_x, Tr_y, Te_x, Te_y, operators, max_depth, population_size,
		max_generation, tournament_size, elitism_size, limit_depth, dim_min, 
		dim_max, threads, rng, verbose, model_name, fitnessType):

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
		self.rng = rng
		self.verbose = verbose
		self.model_name = model_name
		self.fitnessType = fitnessType

		self.dim_min = dim_min
		self.dim_max = dim_max

		self.population = []

		while len(self.population) < self.population_size:
			ind = Individual(self.operators, self.terminals, self.max_depth, self.model_name, self.fitnessType)
			ind.create(self.rng, n_dims = dim_min)
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
			self.trainingMSEOverTime = []
			self.testMSEOverTime = []
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
				if self.fitnessType in ["Accuracy", "2FOLD", "WAF"]:
					self.trainingAccuracyOverTime.append(self.bestIndividual.getAccuracy(self.Tr_x, self.Tr_y, pred="Tr"))
					self.testAccuracyOverTime.append(self.bestIndividual.getAccuracy(self.Te_x, self.Te_y, pred="Te"))
					self.trainingWaFOverTime.append(self.bestIndividual.getWaF(self.Tr_x, self.Tr_y, pred="Tr"))
					self.testWaFOverTime.append(self.bestIndividual.getWaF(self.Te_x, self.Te_y, pred="Te"))
					self.trainingKappaOverTime.append(self.bestIndividual.getKappa(self.Tr_x, self.Tr_y, pred="Tr"))
					self.testKappaOverTime.append(self.bestIndividual.getKappa(self.Te_x, self.Te_y, pred="Te"))
					self.trainingMSEOverTime.append(0)
					self.testMSEOverTime.append(0)
				elif self.fitnessType in ["MSE"]:
					self.trainingAccuracyOverTime.append(0)
					self.testAccuracyOverTime.append(0)
					self.trainingWaFOverTime.append(0)
					self.testWaFOverTime.append(0)
					self.trainingKappaOverTime.append(0)
					self.testKappaOverTime.append(0)
					self.trainingMSEOverTime.append(self.bestIndividual.getMSE(self.Tr_x, self.Tr_y, pred="Tr"))
					self.testMSEOverTime.append(self.bestIndividual.getMSE(self.Te_x, self.Te_y, pred="Te"))
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
				results = pool.map(fitIndividuals, [(ind, self.Tr_x, self.Tr_y) for ind in self.population] )
				for i in range(len(self.population)):
					self.population[i].trainingPredictions = results[i][0]
					self.population[i].fitness = results[i][1]
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
			self.bestIndividual.prun(min_dim = self.dim_min)

		# Generating Next Generation
		newPopulation = []
		newPopulation.extend(getElite(self.population, self.elitism_size))
		while len(newPopulation) < self.population_size:
			offspring = getOffspring(self.rng, self.population, self.tournament_size, self.dim_min, self.dim_max)
			offspring = discardDeep(offspring, self.limit_depth)
			newPopulation.extend(offspring)
		self.population = newPopulation[:self.population_size]


		end = time.time()


		# Debug
		if self.verbose and self.currentGeneration%5==0:
			if not self.Te_x is None:
				print("   > Gen #%2d:  Tr-Score: %.6f // Te-Score: %.6f  // Time: %s" % (self.currentGeneration, self.bestIndividual.getTrainingMeasure(), self.bestIndividual.getTestMeasure(self.Te_x, self.Te_y), str(end- begin) )  )
			else:
				print("   > Gen #%2d:  Tr-Score: %.6f // Time: %s" % (self.currentGeneration, self.bestIndividual.getTrainingMeasure(), str(end- begin) )  )


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

	def getTrainingMSEOverTime(self):
		return self.trainingMSEOverTime

	def getTestMSEOverTime(self):
		return self.testMSEOverTime

	def getSizeOverTime(self):
		return self.sizeOverTime

	def getNumberOfDimensionsOverTime(self):
		return self.dimensionsOverTime

	def getGenerationTimes(self):
		return self.generationTimes



def fitIndividuals(a):
	ind,x,y = a
	ind.getFitness(x,y)

	ret = []
	if "FOLD" in ind.fitnessType:
		ret.append(None)
	else:
		ret.append(ind.getTrainingPredictions())
	ret.append(ind.getFitness())

	
	return ret 

