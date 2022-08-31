from .Population import Population

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
	population = None

	operators = None
	max_initial_depth = None
	population_size = None
	max_generation = None
	tournament_size = None
	elitism_size = None
	limit_depth =None
	dim_min = None
	dim_max = None
	threads = None
	verbose = None

	random_state = 42
	rng = None # random number generator

	def checkIfTrained(self):
		if self.population == None:
			raise ClassifierNotTrainedError("The classifier must be trained using the fit(Tr_X, Tr_Y) method before being used.")


	def __init__(self, operators=[("+",2),("-",2),("*",2),("/",2)], max_initial_depth = 6, population_size = 500, 
		max_generation = 100, tournament_size = 5, elitism_size = 1, limit_depth = 17, 
		dim_min = 1, dim_max = 9999, threads=1, random_state = 42, verbose = True, model_name="MahalanobisDistanceClassifier", fitnessType="Accuracy"):

		if sum( [0 if op in [("+",2),("-",2),("*",2),("/",2)] else 0 for op in operators ] ) > 0:
			print( "[Warning] Some of the following operators may not be supported:", operators)
		self.operators = operators
		self.max_initial_depth = max_initial_depth
		self.population_size = population_size
		self.max_generation = max_generation
		self.tournament_size = tournament_size
		self.elitism_size = elitism_size
		self.limit_depth = limit_depth
		self.dim_min = max(1, dim_min)
		self.dim_max = max(1, dim_max)
		self.threads = max(1, threads)

		self.random_state = random_state
		self.rng = Random(random_state)
		self.model_name = model_name
		self.fitnessType = fitnessType

		self.verbose = verbose
		pass

	def __str__(self):
		self.checkIfTrained()
		
		return str(self.getBestIndividual())
		

	def fit(self,Tr_X, Tr_Y, Te_X = None, Te_Y = None):
		if self.verbose:
			print("  > Parameters")
			print("    > Random State:       "+str(self.random_state))
			print("    > Operators:          "+str(self.operators))
			print("    > Population Size:    "+str(self.population_size))
			print("    > Max Generation:     "+str(self.max_generation))
			print("    > Tournament Size:    "+str(self.tournament_size))
			print("    > Elitism Size:       "+str(self.elitism_size))
			print("    > Max Initial Depth:  "+str(self.max_initial_depth))
			print("    > Max Depth:          "+str(self.limit_depth))
			print("    > Minimum Dimensions: "+str(self.dim_min))
			print("    > Maximum Dimensions: "+str(self.dim_max))
			print("    > Wrapped Model:      "+self.model_name)
			print("    > Fitness Type:       "+self.fitnessType)
			print("    > Threads:            "+str(self.threads))
			print()


		self.population = Population(Tr_X, Tr_Y, Te_X, Te_Y, self.operators, self.max_initial_depth,
			self.population_size, self.max_generation, self.tournament_size, self.elitism_size, 
			self.limit_depth, self.dim_min, self.dim_max, self.threads, self.rng, self.verbose, self.model_name, self.fitnessType)
		self.population.train()

		self.getBestIndividual().prun(min_dim = self.dim_min, simp=True)


	def predict(self, dataset):
		'''
		Returns the predictions for the samples in a dataset.
		'''
		self.checkIfTrained()

		return self.population.getBestIndividual().predict(dataset)

	def getBestIndividual(self):
		'''
		Returns the final M3GP model.
		'''
		self.checkIfTrained()

		return self.population.getBestIndividual()

	def getAccuracyOverTime(self):
		'''
		Returns the training and test accuracy of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.population.getTrainingAccuracyOverTime(), self.population.getTestAccuracyOverTime()]

	def getWaFOverTime(self):
		'''
		Returns the training and test WAF of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.population.getTrainingWaFOverTime(), self.population.getTestWaFOverTime()]

	def getKappaOverTime(self):
		'''
		Returns the training and test kappa values of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.population.getTrainingKappaOverTime(), self.population.getTestKappaOverTime()]

	def getMSEOverTime(self):
		'''
		Returns the training and test mean squared error values of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.population.getTrainingMSEOverTime(), self.population.getTestMSEOverTime()]

	def getSizesOverTime(self):
		'''
		Returns the size and number of dimensions of the best model in each generation.
		'''
		self.checkIfTrained()

		return [self.population.getSizeOverTime(), self.population.getNumberOfDimensionsOverTime()]

	def getGenerationTimes(self):
		'''
		Returns the time spent in each generation.
		'''
		self.checkIfTrained()

		return self.population.getGenerationTimes()