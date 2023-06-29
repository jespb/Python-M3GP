from .Individual import Individual
from .GeneticOperators import getElite, getOffspring, discardDeep
import multiprocessing as mp
import time

from random import Random

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2022 J. E. Batista
#

class ClassifierNotTrainedError(Exception):
    """ You tried to use the classifier before training it. """

    def __init__(self, expression, message = ""):
        self.expression = expression
        self.message = message


class M3GP:

	## __INIT__ arguments
	operators = None
	max_initial_depth = None
	population_size = None
	threads = None
	random_state = 42
	rng = None # random number generator

	max_depth = None
	max_generation = None
	tournament_size = None
	elitism_size = None
	dim_min = None
	dim_max = None

	model_name = None 
	fitnessType = None

	verbose = None


	## FIT arguments
	terminals = None

	population = None
	currentGeneration = 0
	bestIndividual: Individual = None

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



	def checkIfTrained(self):
		if self.population == None:
			raise ClassifierNotTrainedError("The classifier must be trained using the fit(Tr_X, Tr_Y) method before being used.")



	def __init__(self, operators=[("+",2),("-",2),("*",2),("/",2)], max_initial_depth = 6, population_size = 500, 
		max_generation = 100, tournament_size = 5, elitism_size = 1, max_depth = 17, 
		dim_min = 1, dim_max = 9999, threads=1, random_state = 42, verbose = True, model_name="MahalanobisDistanceClassifier", fitnessType="Accuracy"):

		if sum( [0 if op in [("+",2),("-",2),("*",2),("/",2)] else 0 for op in operators ] ) > 0:
			print( "[Warning] Some of the following operators may not be supported:", operators)

		self.operators = operators

		self.max_initial_depth = max_initial_depth
		self.population_size = population_size
		self.threads = max(1, threads)
		self.random_state = random_state
		self.rng = Random(random_state)

		self.max_depth = max_depth
		self.max_generation = max_generation
		self.tournament_size = tournament_size
		self.elitism_size = elitism_size
		self.dim_min = max(1, dim_min)
		self.dim_max = max(1, dim_max)

		self.model_name = model_name
		self.fitnessType = fitnessType

		self.verbose = verbose





	def __str__(self):
		self.checkIfTrained()
		return str(self.getBestIndividual())
		



	def getCurrentGeneration(self):
		return self.currentGeneration


	def getBestIndividual(self):
		'''
		Returns the final M3GP model.
		'''
		self.checkIfTrained()

		return self.bestIndividual

	def getAccuracyOverTime(self):
		'''
		Returns the training and test accuracy of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.trainingAccuracyOverTime, self.testAccuracyOverTime]

	def getWaFOverTime(self):
		'''
		Returns the training and test WAF of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.trainingWaFOverTime, self.testWaFOverTime]

	def getKappaOverTime(self):
		'''
		Returns the training and test kappa values of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.trainingKappaOverTime, self.testKappaOverTime]

	def getMSEOverTime(self):
		'''
		Returns the training and test mean squared error values of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.trainingMSEOverTime, self.testMSEOverTime]

	def getSizesOverTime(self):
		'''
		Returns the size and number of dimensions of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.sizeOverTime, self.dimensionsOverTime]

	def getGenerationTimes(self):
		'''
		Returns the time spent in each generation.
		'''
		self.checkIfTrained()

		return self.generationTimes










	def fit(self,Tr_x, Tr_y, Te_x = None, Te_y = None):
		if self.verbose:
			print("  > Parameters")
			print("    > Random State:       "+str(self.random_state))
			print("    > Operators:          "+str(self.operators))
			print("    > Population Size:    "+str(self.population_size))
			print("    > Max Generation:     "+str(self.max_generation))
			print("    > Tournament Size:    "+str(self.tournament_size))
			print("    > Elitism Size:       "+str(self.elitism_size))
			print("    > Max Initial Depth:  "+str(self.max_initial_depth))
			print("    > Max Depth:          "+str(self.max_depth))
			print("    > Minimum Dimensions: "+str(self.dim_min))
			print("    > Maximum Dimensions: "+str(self.dim_max))
			print("    > Wrapped Model:      "+self.model_name)
			print("    > Fitness Type:       "+self.fitnessType)
			print("    > Threads:            "+str(self.threads))
			print()

		self.Tr_x = Tr_x
		self.Tr_y = Tr_y
		self.Te_x = Te_x
		self.Te_y = Te_y
		self.terminals = list(Tr_x.columns)


		self.population = []

		while len(self.population) < self.population_size:
			ind = Individual(self.operators, self.terminals, self.max_depth, self.model_name, self.fitnessType)
			ind.create(self.rng, n_dims = self.dim_min)
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



		'''
		Training loop for the algorithm.
		'''
		if self.verbose:
			print("  > Running log:")

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


		# prun the final individual
		self.getBestIndividual().prun(min_dim = self.dim_min, simp=True)




	def stoppingCriteria(self):
		'''
		Returns True if the stopping criteria was reached.
		'''
		genLimit = self.currentGeneration >= self.max_generation
		perfectTraining = self.bestIndividual.getFitness() == 1
		
		return genLimit  or perfectTraining




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
			offspring = discardDeep(offspring, self.max_depth)
			newPopulation.extend(offspring)
		self.population = newPopulation[:self.population_size]


		end = time.time()


		# Debug
		if self.verbose and self.currentGeneration%5==0:
			if not self.Te_x is None:
				print("   > Gen #%2d:  Fitness: %.6f // Tr-Score: %.6f // Te-Score: %.6f  // Time: %.4f" % (self.currentGeneration, self.bestIndividual.getFitness(), self.bestIndividual.getTrainingMeasure(), self.bestIndividual.getTestMeasure(self.Te_x, self.Te_y), end- begin )  )
			else:
				print("   > Gen #%2d:  Fitness: %.6f // Tr-Score: %.6f // Time: %.4f" % (self.currentGeneration, self.bestIndividual.getFitness(),  self.bestIndividual.getTrainingMeasure(), end- begin )  )






	def predict(self, dataset):
		'''
		Returns the predictions for the samples in a dataset.
		'''
		self.checkIfTrained()

		return self.getBestIndividual().predict(dataset)

		return "Population Not Trained" if self.bestIndividual == None else self.bestIndividual.predict(sample)


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






