from sys import argv

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#

OPERATORS = ["+","-","*","/"]
MAX_DEPTH = 6
POPULATION_SIZE = 500
MAX_GENERATION = 100
TRAIN_FRACTION = 0.70
TOURNAMENT_SIZE = 5
ELITISM_SIZE = 1
SHUFFLE = True
LIMIT_DEPTH=17
RUNS = 30
VERBOSE = True
THREADS = 1


DATASETS_DIR = "datasets/"
OUTPUT_DIR = "results/"

DATASETS = ["heart.csv"]
OUTPUT = "Classification"




if "-dsdir" in argv:
	DATASETS_DIR = argv[argv.index("-dsdir")+1]
if "-odir" in argv:
	OUTPUT_DIR = argv[argv.index("-odir")+1]
if "-d" in argv:
	DATASETS = argv[argv.index("-d")+1].split(";")
if "-r" in argv:
	OUTPUT = "Regression"
if "-runs" in argv:
	RUNS = int(argv[argv.index("-runs")+1])
if "-op" in argv:
	OPERATORS = argv[argv.index("-op")+1].split(";")
if "-md" in argv:
	MAX_DEPTH = int(argv[argv.index("-md")+1])
if "-ps" in argv:
	POPULATION_SIZE = int(argv[argv.index("-ps")+1])
if "-mg" in argv:
	MAX_GENERATION = int(argv[argv.index("-mg")+1])
if "-tf" in argv:
	TRAIN_FRACTION = float(argv[argv.index("-tf")+1])
if "-ts" in argv:
	TOURNAMENT_SIZE = int(argv[argv.index("-ts")+1])
if "-es" in argv:
	ELITISM_SIZE = int(argv[argv.index("-es")+1])
if "-dontshuffle" in argv:
	SHUFFLE = False
if "-s" in argv:
	VERBOSE = False
if "-t" in argv:
	THREADS = int(argv[argv.index("-t")+1])




terminals = None

def setTerminals(l):
	global terminals 
	terminals = l
def getTerminals():
	return terminals



trainingSet = None

def setTrainingSet(ds):
	global trainingSet
	trainingSet = ds
def getTrainingSet():
	return trainingSet



testSet = None

def setTestSet(ds):
	global testSet
	testSet = ds
def getTestSet():
	return testSet
