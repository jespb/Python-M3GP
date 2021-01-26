import pandas

from m3gp.M3GP import M3GP
from sys import argv
from m3gp.Constants import *
import os

from sklearn.model_selection import train_test_split

import numpy as np


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019-2021 J. E. Batista
#




def openAndSplitDatasets(which,seed):
	if VERBOSE:
		print( "> Opening: ", which )

	# Open dataset
	ds = pandas.read_csv(DATASETS_DIR+which)

	# Read header
	class_header = ds.columns[-1]

	return train_test_split(ds.drop(columns=[class_header]), ds[class_header], 
		train_size=TRAIN_FRACTION, random_state=seed, stratify = ds[class_header])


def run(r,dataset):
	if VERBOSE:
		print("> Starting run:")
		print("  > ID:", r)
		print("  > Dataset:", dataset)
		print()

	Tr_X, Te_X, Tr_Y, Te_Y = openAndSplitDatasets(dataset,r)

	# Train a model
	m3gp = M3GP()
	m3gp.fit_standAlone(Tr_X, Tr_Y, Te_X, Te_Y)


	# Obtain training results
	accuracy  = m3gp.getAccuracyOverTime()
	waf       = m3gp.getWaFOverTime()
	kappa     = m3gp.getKappaOverTime()
	sizes     = m3gp.getSizesOverTime()
	model_str = str(m3gp.getBestIndividual())
	times     = m3gp.getGenerationTimes()
	
	tr_acc     = accuracy[0]
	te_acc     = accuracy[1]
	tr_waf     = waf[0]
	te_waf     = waf[1]
	tr_kappa   = kappa[0]
	te_kappa   = kappa[1]
	size       = sizes[0]
	dimensions = sizes[1]

	if VERBOSE:
		print("> Ending run:")
		print("  > ID:", r)
		print("  > Dataset:", dataset)
		print("  > Final model:", model_str)
		print("  > Training accuracy:", tr_acc[-1])
		print("  > Test accuracy:", te_acc[-1])
		print()

	return (tr_acc,te_acc,
			tr_waf,te_waf,
			tr_kappa,te_kappa,
			size,dimensions,
			times,
			model_str)
			

def callm3gp():
	try:
		os.makedirs(OUTPUT_DIR)
	except:
		pass

	for dataset in DATASETS:
		if not os.path.exists(OUTPUT_DIR+"m3gp_"+ dataset):
			results = []

			# Run the algorithm several times
			for r in range(RUNS):
				results.append(run(r,dataset))

			# Write output header
			file = open(OUTPUT_DIR+"m3gp_"+ dataset , "w")
			file.write("Attribute,Run,")
			for i in range(MAX_GENERATION):
				file.write(str(i)+",")
			file.write("\n")
		
			attributes= ["Training-Accuracy","Test-Accuracy",
						 "Training-WaF", "Test-WaF",
						 "Training-Kappa", "Test-Kappa",
						 "Size","Dimensions",
						 "Time",	
						 "Final_Model"]

			# Write attributes with value over time
			for ai in range(len(attributes)-1):
				for i in range(RUNS):	
					file.write("\n"+attributes[ai]+","+str(i)+",")
					file.write( ",".join([str(val) for val in results[i][ai]]))
				file.write("\n")

			# Write the final models
			for i in range(len(results)):
				file.write("\n"+attributes[-1]+","+str(i)+",")
				file.write(results[i][-1])
			file.write("\n")

			# Write some parameters
			file.write("\n\nParameters")
			file.write("\nPOPULATION_SIZE,"+str(POPULATION_SIZE))
			file.write("\nMAX_GENERATION,"+str(MAX_GENERATION))
			file.write("\nTOURNAMENT_SIZE,"+str(TOURNAMENT_SIZE))
			file.write("\nTHREADS,"+str(THREADS))

			file.close()
		else:
			print("Filename: " + OUTPUT_DIR+"m3gp_"+ dataset +" already exists.")


if __name__ == '__main__':
	callm3gp()
