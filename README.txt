By using this file, you are agreeing to this product's EULA
This product can be obtained in https://github.com/jespb/Python-M3GP
Copyright ©2019 J. E. Batista

This implementation of M3GP uses the following command and flags:

$ python Main_M3GP.py
	
	[-d datasets] 
		- This flag expects a set of csv dataset names separated by ";" (e.g., a.csv;b.csv)
		- By default, the heart.csv dataset is used		

	[-dontshuffle]
		- By using this flag, the dataset will not be shuffled;
		- By default, the dataset is shuffled.

	[-dsdir dir] 
		- States the dataset directory. 
		- By default "datasets/" is used 
		- Use "-dsdir ./" for the root directory	

	[-es elite_size]
		- This flag expects an integer with the elite size;
		- By default, the elite has size 1.

	[-md max_depth]
		- This flag expects an integer with the maximum initial depth for the trees;
		- By default, this value is set to 6.		

	[-mg max_generation]
		- This flag expects an integer with the maximum number of generations;
		- By default, this value is set to 100.

	[-odir dir] 
		- States the output directory. 
		- By default "results/" is used 
		- Use "-odir ./" for the root directory
	
	[-op operators]
		- This flag excepts a set of operators separated by ";"
		- Allowed operators: +;-;*;/
		- By default, the used operators are the sum, subtraction, multiplication and protected division.		

	[-ps population_size]
		- This flag expects an integer with the size of the population;
		- By default, this value is set to 500.

	[-r] 
		- States the this is a regression problem. 
		- By default the GSGP tries to classify samples as 0 or 1

	[-runs number_of_runs] 
		- This flag expects an integer with the number of runs to be made;
		- By default, this values is set to 30
	
	[-tf train_fraction]
		- This flag expects a float [0;1] with the fraction of the dataset to be used in training;
		- By default, this value is set to 0.70
	
	[-ts tournament_size]
		- This flag expects an integer with the tournament size;
		- By default, this value is set to 10.
