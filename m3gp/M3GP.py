from .Population import Population

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#

class ClassifierNotTrainedError(Exception):
    """ You tried to use the classifier before training it. """

    def __init__(self, expression, message = ""):
        self.expression = expression
        self.message = message


class M3GP:
	population = None

	def checkIfTrained(self):
		if self.population == None:
			raise ClassifierNotTrainedError("The classifier must be trained using the fit(Tr_X, Tr_Y) method before being used.")


	def __init__(self):
		pass

	def __str__(self):
		self.checkIfTrained()
		
		return str(self.getBestIndividual())
		

	def fit(self,Tr_X, Tr_Y, Te_X = None, Te_Y = None, operators=["+","-","*","/"], max_depth = 6, 
		population_size = 500, max_generation = 100, tournament_size = 5, elitism_size = 1, 
		limit_depth = 17, threads=1, verbose = True):
		if verbose:
			print("Training a model with the following parameters: ", end="")
			print("{Operators : "+str(operators)+"}, ", end="")
			print("{Max Depth : "+str(max_depth)+"}, ", end="")
			print("{Population Size : "+str(population_size)+"}, ", end="")
			print("{Max Generation : "+str(max_generation)+"}, ", end="")
			print("{Tournament Size : "+str(tournament_size)+"}, ", end="")
			print("{Elitism Size : "+str(elitism_size)+"}, ", end="")
			print("{Depth Limit : "+str(limit_depth)+"}, ", end="")
			print("{Threads : "+str(threads)+"}, ", end="")

		self.population = Population(Tr_X, Tr_Y, Te_X, Te_Y, operators,max_depth,population_size,max_generation,tournament_size,elitism_size, limit_depth,threads, verbose)
		self.population.train()
		self.getBestIndividual().prun()


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