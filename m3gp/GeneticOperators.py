from .Constants import *
from .Individual import Individual
from .Node import Node
from random import random, randint

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#


def tournament(population):
	'''
	Selects "TOURNAMENT_SIZE" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	candidates = [randint(0,len(population)-1) for i in range(TOURNAMENT_SIZE)]
	return population[min(candidates)]


def getElite(population):
	'''
	Returns the "ELITISM_SIZE" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:ELITISM_SIZE]


def getOffspring(population):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = random()<0.5
	desc = None
	if isCross:
		isSTXO = random()<0.5
		if isSTXO:
			desc = STXO(population)
		else:
			desc = M3XO(population)
	else:
		whichMut = randint(1,3)
		if whichMut == 1:
			desc = STMUT(population)
		elif whichMut == 2:
			desc = M3ADD(population)
		else:
			desc = M3REM(population)
	ret = []
	for ind in desc:
		if ind.getDepth() < LIMIT_DEPTH:
			ret.append(ind)
	return ret

def STXO(population):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(population)
	ind2 = tournament(population)

	d1 = ind1.getDimensions()
	d2 = ind2.getDimensions()

	r1 = randint(0,len(d1)-1)
	r2 = randint(0,len(d2)-1)

	n1 = d1[r1].getRandomNode()
	n2 = d2[r2].getRandomNode()

	n1.swap(n2)

	ret = [Individual(d1), Individual(d2)]
	return ret

def M3XO(population):
	'''
	Randomly selects one dimension from each of two individuals; swaps the 
	dimensions; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(population)
	ind2 = tournament(population)

	d1 = ind1.getDimensions()
	d2 = ind2.getDimensions()

	r1 = randint(0,len(d1)-1)
	r2 = randint(0,len(d2)-1)

	d1.append(d2[r2])
	d2.append(d1[r1])
	d1.pop(r1)
	d2.pop(r2)

	ret = [Individual(d1), Individual(d2)]
	return ret

def STMUT(population):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(population)
	d1 = ind1.getDimensions()
	r1 = randint(0,len(d1)-1)
	n1 = d1[r1].getRandomNode()
	n1.swap(Node())
	ret = [Individual(d1)]
	return ret

def M3ADD(population):
	'''
	Randomly generates a new node using Grow; this node is added to the list of
	dimensions; the new Individual is returned as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(population)
	d1 = ind1.getDimensions()
	d1.append(Node())
	ret = [Individual(d1)]
	return ret

def M3REM(population):
	'''
	Randomly selects one dimensions from a single individual; that dimensions is
	removed; the new Individual is returned as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = tournament(population)
	d1 = ind1.getDimensions()
	if len(d1)>1:
		r1 = randint(0,len(d1)-1)
		d1.pop(r1)
		ret = [Individual(d1)]
	else:
		ret = []
	return ret
