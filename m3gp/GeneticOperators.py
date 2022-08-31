from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2022 J. E. Batista
#


def tournament(rng, population,n):
	'''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	candidates = [rng.randint(0,len(population)-1) for i in range(n)]
	return population[min(candidates)]


def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]


def getOffspring(rng, population, tournament_size, dim_min, dim_max):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = rng.random()<0.5
	desc = None

	availableXO = [0,1]
	availableMT = [0,1,2] 

	if isCross:
		whichXO = availableXO[ rng.randint(0,len(availableXO)-1 ) ]
		if whichXO == 0:
			desc = STXO(rng, population, tournament_size)
		elif whichXO == 1:
			desc = M3XO(rng, population, tournament_size)
	else:
		whichMut = availableMT[ rng.randint(0,len(availableMT)-1 ) ]
		if whichMut == 0:
			desc = STMUT(rng, population, tournament_size)
		elif whichMut == 1:
			desc = M3ADD(rng, population, tournament_size, dim_max)
		elif whichMut == 2:
			desc = M3REM(rng, population, tournament_size, dim_min)
	return desc


def discardDeep(population, limit):
	ret = []
	for ind in population:
		if ind.getDepth() <= limit:
			ret.append(ind)
	return ret


def STXO(rng, population, tournament_size):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	ind2 = tournament(rng, population, tournament_size)

	d1 = ind1.getDimensions()
	d2 = ind2.getDimensions()

	r1 = rng.randint(0,len(d1)-1)
	r2 = rng.randint(0,len(d2)-1)

	n1 = d1[r1].getRandomNode(rng)
	n2 = d2[r2].getRandomNode(rng)

	n1.swap(n2)

	ret = []
	for d in [d1,d2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(d)
		ret.append(i)
	return ret

def M3XO(rng, population, tournament_size):
	'''
	Randomly selects one dimension from each of two individuals; swaps the 
	dimensions; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	ind2 = tournament(rng, population, tournament_size)

	d1 = ind1.getDimensions()
	d2 = ind2.getDimensions()

	r1 = rng.randint(0,len(d1)-1)
	r2 = rng.randint(0,len(d2)-1)

	d1.append(d2[r2])
	d2.append(d1[r1])
	d1.pop(r1)
	d2.pop(r2)

	ret = []
	for d in [d1,d2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(d)
		ret.append(i)
	return ret

def STMUT(rng, population, tournament_size):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	d1 = ind1.getDimensions()
	r1 = rng.randint(0,len(d1)-1)
	n1 = d1[r1].getRandomNode(rng)
	n = Node()
	n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
	n1.swap(n)


	ret = []
	i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
	i.copy(d1)
	ret.append(i)
	return ret

def M3ADD(rng, population, tournament_size, dim_max):
	'''
	Randomly generates a new node using Grow; this node is added to the list of
	dimensions; the new Individual is returned as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	ret = []

	if ind1.getNumberOfDimensions() < dim_max:
		d1 = ind1.getDimensions()
		n = Node()
		n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
		d1.append(n)

		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(d1)
		ret.append(i)

	return ret

def M3REM(rng, population, tournament_size, dim_min):
	'''
	Randomly selects one dimensions from a single individual; that dimensions is
	removed; the new Individual is returned as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(rng, population, tournament_size)
	ret = []

	if ind1.getNumberOfDimensions() > dim_min:
		d1 = ind1.getDimensions()
		r1 = rng.randint(0,len(d1)-1)
		d1.pop(r1)
		
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(d1)
		ret.append(i)
	
	return ret
