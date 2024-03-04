This is a, easy-to-use, scikit-learn inspired version of the M3GP algorithm.


By using this file, you are agreeing to this product's EULA
This product can be obtained in https://github.com/jespb/Python-M3GP
Copyright ©2019-2024 J. E. Batista


This file contains information about the command and flags used in the stand-alone version of this implementation and an explanation on how to import, use and edit this implementation.




This implementation of M3GP can be used in a stand-alone fashion using the following command and flags:

$ python Main_M3GP_standalone.py
	
    [-d datasets] 
        - This flag expects a set of csv dataset names separated by ";" (e.g., "a.csv;b.csv")
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
        - This flag excepts a set of operators and their number of arguments, separated by ";"
        - Allowed operators: +,2 ; -,2 ; *,2 ; /,2
        - By default, the used operators are the sum, subtraction, multiplication and protected division: "+,2;-,2;*,2;/,2"	

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
	
    [-di minimum_number_of_dimension]
        - This flag expects an integer with the minimum number of dimensions in each individual;
        - This flag affects the number of dimensions in the initial individuals;
        - By default, this value is set to 1

    [-dm maximum_number_of_dimension]
        - This flag expects an integer with the maximum number of dimensions in each individual;
        - By default, this value is set to 9999

    [-rs random state]
        - This flag expects an integer with the seed to be used by the M3GP algorithm;
        - By default, this value is set to 42


	

How to import this implementation to your project:
    - Download this repository;
    - Copy the "m3gp/" directory to your project directory;
    - import the M3GP class using "from m3gp.M3GP import M3GP".

How to use this implementation:
    $ from m3gp.M3GP import M3GP
    $ model = M3GP()
    $ model.fit( training_x, training_y, test_x (optional), test_y (optional) )

Arguments for M3GP():
    operators		-> Operators used by the individual (default: [("+",2),("-",2),("*",2),("/",2)] )
    max_depth		-> Max initial depths of the individuals (default: 6)
    population_size	-> Population size (default: 500)
    max_generation	-> Maximum number of generations (default: 100)
    tournament_size	-> Tournament size (default: 5)
    elitism_size	-> Elitism selection size (default: 1)
    limit_depth		-> Maximum individual depth (default: 17)
    threads 		-> Number of CPU threads to be used (default: 1)
    random_state	-> Random state (default: 42)
    dim_min		-> Minimum number of dimensions (default: 1)
    dim_max		-> Maximum number of dimensions (default: 9999) #The algorithm will not reach this value

Arguments for model.fit():
    Tr_X 		-> Training samples
    Tr_Y 		-> Training labels
    Te_X 		-> Test samples, used in the standalone version (default: None)
    Te_Y 		-> Test labels, used in the standalone version (default: None)

Useful methods:
    $ model = M3GP()	-> starts the model;
    $ model.fit(X, Y)	-> fits the model to the dataset;
    $ model.predict(X)	-> Returns a list with the prediction of the given dataset.




How to edit this implementation:
    Fitness Function ( m3gp.Individual ):
        - Change the getFitness() method to use your own fitness function;
        - This implementation assumes that a higher fitness is always better. To change this, edit the __gt__ method in this class;
        - Warning: Since M3GP is a slow method, a fitness function that escalates well with the number of features is recommended. 

    Classification method ( m3gp.Individual ):
        - Change the createModel() method to use your own classifier;
        - Assuming it is a scykit-learn implementation, you may only need to change one line in this method;
        - Warning: Since M3GP is a slow method, a learning algorithm that escalates well with the number of features is recommended.

   


Citation: 
    If you use this implementation, please cite one of the works below, where the implementation is also used:

    @inproceedings{Batista2022,
  	doi = {10.1109/cec55065.2022.9870343},
  	url = {https://doi.org/10.1109/cec55065.2022.9870343},
  	year = {2022},
  	month = jul,
  	publisher = {{IEEE}},
  	author = {Joao E. Batista and Sara Silva},
  	title = {Comparative study of classifier performance using automatic feature construction by M3GP},
  	booktitle = {2022 {IEEE} Congress on Evolutionary Computation ({CEC})}
    }

    @Article{rs13091623,
        AUTHOR = {Batista, João E. and Cabral, Ana I. R. and Vasconcelos, Maria J. P. and Vanneschi, Leonardo and Silva, Sara},
        TITLE = {Improving Land Cover Classification Using Genetic Programming for Feature Construction},
        JOURNAL = {Remote Sensing},
        VOLUME = {13},
        YEAR = {2021},
        NUMBER = {9},
        ARTICLE-NUMBER = {1623},
        URL = {https://www.mdpi.com/2072-4292/13/9/1623},
        ISSN = {2072-4292},
        DOI = {10.3390/rs13091623}
    }

    @INPROCEEDINGS{9185630,
        author={Batista, João E. and Silva, Sara},
        booktitle={2020 IEEE Congress on Evolutionary Computation (CEC)}, 
        title={Improving the Detection of Burnt Areas in Remote Sensing using Hyper-features Evolved by M3GP}, 
        year={2020},
        pages={1-8},
        doi={10.1109/CEC48606.2020.9185630}
    }




Reference:
    Muñoz, L., Trujillo, L., & Silva, S. (2015). M3GP – multiclass classification with GP. In Genetic Programming - 18th European Conference, EuroGP 2015, Proceedings (Vol. 9025, pp. 78-91). (Lecture Notes in Computer Science (including subseries Lecture Notes in Artificial Intelligence and Lecture Notes in Bioinformatics); Vol. 9025). Springer-Verlag. https://doi.org/10.1007/978-3-319-16501-1_7
