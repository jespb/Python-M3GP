By using this file, you are agreeing to this product's EULA
This product can be obtained in https://github.com/jespb/Python-M3GP
Copyright ©2019-2021 J. E. Batista


This file contains information about the command and flags used in the stand-alone version of this implementation and an explanation on how to import, use and edit this implementation.


This implementation of M3GP can be used in a stand-alone fashion using the following command and flags:

$ python Main_M3GP_standalone.py
	
	[-d datasets] 
		- This flag expects a set of csv dataset names separated by ";" (e.g., a.csv;b.csv)
		- By default, the heart.csv dataset is used		

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

	[-runs number_of_runs] 
		- This flag expects an integer with the number of runs to be made;
		- By default, this values is set to 30
	
	[-tf train_fraction]
		- This flag expects a float [0;1] with the fraction of the dataset to be used in training;
		- By default, this value is set to 0.70
	
	[-ts tournament_size]
		- This flag expects an integer with the tournament size;
		- By default, this value is set to 10.

	[-t number_of_threads]
		- This flag expects an integer with the number of threads to use while evaluating the population;
		- If the value is set to 1, the multiprocessing library will not be used 
		- By default, this value is set to 1.

	[-di initial_number_of_dimension]
		- This flag expects an integer with the number of dimensions in each individual when creating the initial population;
		- By default, this value is set to 1

	[-dm maximum_number_of_dimension]
		- This flag expects an integer with the maximum number of dimensions in each individual;
		- By default, this value is set to 9999

	[-de evolution_of_the_number_of_dimensions]
		- This flag expects a string with the value "evol" or "fixed";
			- evol: The number of dimensions is evolved during the evolution;
			- fixed: The number of dimensions is fixed (The dimensions are never removed nor added).
		- By default, this flag is set to "evol"

	


How to import this implementation to your project:
	- Download this repository;
	- Copy the "m3gp/" directory to your project directory;
	- import the M3GP class using "from m3gp.M3GP import M3GP".

How to use this implementation:
	$ from m3gp.M3GP import M3GP
	$ model = M3GP()
	$ model.fit( training_x, training_y, test_x, test_y )

Arguments for model.fit:
	Tr_X 				-> Training samples
	Tr_Y 				-> Training labels
	Te_X 				-> Test samples, used in the standalone version (default: None)
	Te_Y 				-> Test labels, used in the standalone version (default: None)
	operators			-> Operators used by the individual (default: ["+","-","*","/"] )
	max_depth			-> Max initial depths of the individuals (default: 6)
	population_size		-> Population size (default: 500)
	max_generation		-> Maximum number of generations (default: 100)
	tournament_size		-> Tournament size (default: 5)
	elitism_size		-> Elitism selection size (default: 1)
	limit_depth			-> Maximum individual depth (default: 17)
	threads 			-> Number of CPU threads to be used (default: 1)

Useful methods:
	$ model = M3GP()			-> starts the model;
	$ model.fit(X, Y)			-> fits the model to the dataset;
	$ model.predict(dataset)    -> Returns a list with the prediction of the given dataset.




How to edit this implementation:
	Fitness Function ( m3gp.Individual ):
		- Change the getFitness() method to use your own fitness function;
		- This implementation assumes that a higher fitness is always better. To change this, edit the __gt__ method in this class;
		- You may use the getTrainingPredictions() and getTrainingSet() to obtain the models prediction and the training set;
		- You can also explore the behind the standard fitness function;
		- Warning: M3GP is a slow method and, as such, I do not recomend complex fitness functions. You should invest in fast evaluation methods to train a population.

	Classification method ( m3gp.Individual ):
		- Change the trainModel() method to use your own classifier;
		- Assuming it is a scykit-learn implementation, you may only need to change the first few lines of this method;
		- Warning: M3GP is a slow method and, as such, I do not recomend complex classification model. You should invest in fast classification methods to train a population and the use a more complex method (if you wish) on the final model.


Reference:
    Muñoz, L., Trujillo, L., & Silva, S. (2015). M3GP – multiclass classification with GP. In Genetic Programming - 18th European Conference, EuroGP 2015, Proceedings (Vol. 9025, pp. 78-91). (Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics); Vol. 9025). Springer-Verlag. https://doi.org/10.1007/978-3-319-16501-1_7
