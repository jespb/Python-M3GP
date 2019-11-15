import pandas

from m3gp.M3GP import M3GP
from sys import argv
from m3gp.Constants import *
import os

import time

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-M3GP
#
# Copyright ©2019 J. E. Batista
#


timestamp = time.strftime("%Y%m%d_%H%M")



def callm3gp():
	try:
		os.makedirs(OUTPUT_DIR)
	except:
		pass

	for dataset in DATASETS:#["trio_brasil.csv","trio_congo.csv","trio_mocambique.csv","trio_combo.csv"]:#["mcd3.csv","mcd10.csv","brasil.csv","movl.csv","heart.csv","vowel.csv","wav.csv","yeast.csv","seg.csv"]:
		openFile(OUTPUT_DIR+"tmp_m3gp_"+timestamp + "_"+dataset)
		writeToFile(dataset+"\n")
		toWrite=[]
		for i in range(RUNS):
			print(i,"# run with the", dataset,"dataset")
			p = pandas.read_csv(DATASETS_DIR+dataset)
			m3gp = M3GP(p)

			writeToFile(",")
			for i in range(MAX_GENERATION):
				writeToFile(str(i)+",")
			
			accuracy = m3gp.getAccuracyOverTime()
			sizes = m3gp.getSizesOverTime()
			toWrite.append([accuracy[0],accuracy[1],sizes[0],sizes[1],str(m3gp.getBestIndividual())])
			
			writeToFile("\nTraining-Accuracy,")
			for val in accuracy[0]:
				writeToFile(str(val)+",")
			
			writeToFile("\nTest-Accuracy,")
			for val in accuracy[1]:
				writeToFile(str(val)+",")
			
			writeToFile("\nDimensions,")
			for val in sizes[0]:
				writeToFile(str(val)+",")
			
			writeToFile("\nSize,")
			for val in sizes[1]:
				writeToFile(str(val)+",")

			writeToFile("\n"+str(m3gp.getBestIndividual())+"\n")
		
		closeFile()

		openFile(OUTPUT_DIR+"m3gp_"+timestamp + "_"+dataset) 
		writeToFile("Attribute,Run,")
		for i in range(MAX_GENERATION):
			writeToFile(str(i)+",")
		writeToFile("\n")
		
		attributes= ["Training-Accuracy","Test-Accuracy","Dimensions","Size","Final_Model"]
		for ai in range(len(toWrite[0])-1):
			for i in range(len(toWrite)):
				writeToFile("\n"+attributes[ai]+","+str(i)+",")
				for val in toWrite[i][ai]:
					writeToFile(str(val)+",")
				#writeToFile(",".join(toWrite[i][ai]))
			writeToFile("\n\n")
		for i in range(len(toWrite)):
			writeToFile("\n"+attributes[-1]+","+str(i)+",")
			writeToFile(str(toWrite[i][-1]))
		writeToFile("\n\n")

		
		closeFile()
		os.remove(OUTPUT_DIR+"tmp_m3gp_"+timestamp + "_"+dataset)

callm3gp()