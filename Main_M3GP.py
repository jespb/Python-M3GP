import pandas

from m3gp.M3GP import M3GP
from sys import argv
from m3gp.Constants import *
import os

import numpy as np


# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#




def openAndSplitDatasets(which,seed):
	if VERBOSE:
		print( "> Opening: ", which )

	# Open dataset
	ds = pandas.read_csv(DATASETS_DIR+which)

	# Set features as float
	col = list(ds)
	for i in range(len(col)-1):
		ds[col[i]] = ds[col[i]].astype(float)


	# Shuffle dataset
	if SHUFFLE:
		ds = ds.sample(frac=1,random_state=seed) 

	# Read header
	class_header = ds.columns[-1]
	terminals = list(ds.columns[:-1])

	# Obtain list of classes
	classes = list( set( ds[ class_header ] ) )

	# Split the dataset maintaining the class balance
	ret = [ [] for i in range(2)]
	for c in classes:
		classe = ds.loc[ds[class_header] == c]
		for i in range(classe.shape[0]):
			if  i < TRAIN_FRACTION * len(classe):
				ret[0].append(list(classe.iloc[i]))
			else:
				ret[1].append(list(classe.iloc[i]))

	# Convert dataset to Pandas
	ret[0] = pandas.DataFrame( np.array(ret[0]))
	ret[1] = pandas.DataFrame( np.array(ret[1]))
	ret[0].columns = terminals+[class_header]
	ret[1].columns = terminals+[class_header]

	# Split Features from Class
	ret[0] = ( ret[0].drop(class_header, axis = 1), ret[0][class_header] )
	ret[1] = ( ret[1].drop(class_header, axis = 1), ret[1][class_header] ) 


	if VERBOSE:
		print("   > Attributes: ", terminals)
		print("   > Classes: ", classes)
		print("   > Training set size: ", len(ret[0][0]))
		print("   > Test set size: ", len(ret[1][0]))
		print()


	return (ret[0][0], ret[0][1], ret[1][0], ret[1][1])


def run(r,dataset):
	if VERBOSE:
		print("> Starting run:")
		print("  > ID:", r)
		print("  > Dataset:", dataset)
		print()

	Tr_X, Tr_Y, Te_X, Te_Y = openAndSplitDatasets(dataset,r)

	# Train a model
	m3gp = M3GP(Tr_X, Tr_Y, Te_X, Te_Y)

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
			try:
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
			except:
				print("[ERROR]", dataset)

if __name__ == '__main__':
	callm3gp()
