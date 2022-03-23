import time
import random
import copy
import numpy

"""
    The evolutionary algorithm is used to produce sets of fit solutions for
    the sudoku problems found on the Grids (1,2,3) provided by the coursework
    specification.
    
    The grids consist of a 9x9 grid and 3x3 sub grids that have digits going from 
    the range 0-9. The grids given are partially completed but need the full solution.
"""

# Grid 1 representing the partially filled up 9x9 grid given by spec
Grid1 = [[3, 0, 0, 0, 0, 5, 0, 4, 7],
         [0, 0, 6, 0, 4, 2, 0, 0, 1],
         [0, 0, 0, 0, 0, 7, 8, 9, 0],
         [0, 5, 0, 0, 1, 6, 0, 0, 2],
         [0, 0, 3, 0, 0, 0, 0, 0, 4],
         [8, 1, 0, 0, 0, 0, 7, 0, 0],
         [0, 0, 2, 0, 0, 0, 4, 0, 0],
         [5, 6, 0, 8, 7, 0, 1, 0, 0],
         [0, 0, 0, 3, 0, 0, 6, 0, 0]]

# Grid 2 representing the partially filled up 9x9 grid given by spec
Grid2 = [[0, 0, 2, 0, 0, 0, 6, 3, 4],
         [1, 0, 6, 0, 0, 0, 5, 8, 0],
         [0, 0, 7, 3, 0, 0, 2, 9, 0],
         [0, 8, 5, 0, 0, 1, 0, 0, 6],
         [0, 0, 0, 7, 5, 0, 0, 2, 3],
         [0, 0, 3, 0, 0, 0, 0, 5, 0],
         [3, 1, 4, 0, 0, 2, 0, 0, 0],
         [0, 0, 9, 0, 8, 0, 4, 0, 0],
         [7, 2, 0, 0, 4, 0, 0, 0, 9]]

# Grid 3 representing the partially filled up 9x9 grid given by spec
Grid3 = [[0, 0, 4, 0, 1, 0, 0, 6, 0],
         [9, 0, 0, 0, 0, 0, 0, 3, 0],
         [0, 5, 0, 7, 9, 6, 0, 0, 0],
         [0, 0, 2, 5, 0, 4, 9, 0, 0],
         [0, 8, 3, 0, 6, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 6, 0, 7],
         [0, 0, 0, 9, 0, 3, 0, 7, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 6, 0, 0, 0, 0, 1, 0]]

"""This line of code is utilised to decide what Grid out of the 3 grid options given
    above to pick and solve by finding the fittest solution.
"""

answer = numpy.array(Grid2)

### EVOLUTIONARY ALGORITHM ###

def evolve():
    population = create_pop()
    fitness_population = evaluate_pop(population)
    # ensures the number of generations is in the range of the termination criteria value input
    range_number = TERMINATION_GENERATION * [(9 ** 3)]
    p=0
    for gen in range(NUMBER_GENERATION):
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        # this merges the reproduced with the mating pool
        population=[]
        for y in offspring_population:
            population.append(y)
        for z in mating_pool:
            population.append(z)
        # this mutates the new population
        population = mutate_pop(population)
        fitness_population = evaluate_pop(population)
        # this prints out the evolution of the guesses
        # lets user know the fitness of the guess
        # states number of clashes that impede the correct solution
        p=min(int(q) for q in fitness_population)
        print("Generation:  " + str(gen) + "     Fittest guess:   " + str(p) + " clashes!")
        # prints solution if no clashes are found
        if p==0:
            l=fitness_population.index(p)
            print("WELL DONE!! The solution to the Sudoku has been encountered!!\n"
                  "It was obtained at the generation" + str(gen))
            return population[l]
        # the range number is contrasted with the termination generation numbers fittest guess
        # if no solution found after the termination number surpassed then
        # program prints message for user to try other parameter values
        range_number.append(p)
        p=range_number.pop(0)
        if p <= min(int(i) for i in range_number):
            print("WARNING! "
                  "Unfortunately, the fittest guess for the solution of the sudoku has " + str(min(int(s) for s in fitness_population)) + " clashes!"
                  "There has been no advancement made by program in the past" + str(TERMINATION_GENERATION) +
                  "The team suggests user inputs different parameters on the next run.")
            return False

### POPULATION-LEVEL OPERATORS ###
def create_pop():
    return [create_ind() for _ in range(POPULATION_SIZE)]

def evaluate_pop(population):
    return [evaluate_ind(individual) for individual in population]

"""
    This function returns the fittest population size multiplied by the truncation rate
"""
def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key=lambda ind_fit: ind_fit[1])
    sorted_population = [a[0] for a in sorted_population]
    return sorted_population[:int(TRUNCATION_RATE * POPULATION_SIZE)]
"""
    This function is used for the crossing over of the population that has to mate-
    Probabilities are used to decide what parents are chosen to fulfil the fittest 
    possible solution effectively.
"""
def crossover_pop(population):
    chances=[]
    children=[]
    a = 1.5
    k = len(population)
    # this variable is the chances of choosing the most disadvantaged or not useful parent in order to find the solution
    disadvantaged_parent=(a - 1.0)/(a ** k - 1)
    # for loop for producing a list stating the chances of selecting the parent
    for p in range(k):
        chances.append(disadvantaged_parent * (a ** (k - p - 1)))
    # the 2 parents are selected randomly
    for _ in range(int((1 - TRUNCATION_RATE) * POPULATION_SIZE)):
        parent=numpy.random.choice(len(population), 2, chances)
        # produces the list of the children generated from the crossing over with parents
        offspring=crossover_ind(population[parent[0]], population[parent[1]])
        children.append(offspring)
    return children

def mutate_pop(population):
    return [mutate_ind(individual) for individual in population]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###
"""
    The individuals in this function are represented in a numpy matrix.
    They are made up of rows that cannot contain the same number twice.
    The numbers have to be in the range between: 1-9
"""
def create_ind():
    individual=[]
    # this loop generates the values and mixes them in random order to make up one of the horizontal lines in the sudoku
    for s in range(0,9):
        values=list(range(1,10))
        line=answer[s, :]
        for h in line:
            if h!=0:
                values.remove(h)
        random.shuffle(values)
        f=0
        next_line=[]
        for s in line:
            if s == 0:
                s=values[f]
                f+=1
            next_line.append(s)
        individual.append(next_line)
    z=numpy.array(individual)
    return z

"""
    This function instead of checking for errors or same numbers horizontally,
    it checks for the individuals that are positioned vertically or in the 
    3x3 sub grids.
"""
def evaluate_ind(individual):
    all_clashes = 0
    # this loop is for the checking of the columns
    for r in range(0, 9):
        line=individual[:, r]
        already_present=set()
        original=[]
        for g in line:
            if g not in already_present:
                original.append(g)
                already_present.add(g)
        clash=9 - len(original)
        all_clashes+=clash
    # this loop is for the checking of the 3x3 grids (subgrid)
    for r in range(0, 3):
        for y in range(0, 3):
            subgrid = individual[r * 3:r * 3 + 3, y * 3:y * 3 + 3]
            other_subgrid=zip(*subgrid)
            three_by_three=[]
            for a in other_subgrid:
                for r in a:
                    three_by_three.append(r)
            already_present=set()
            original=[]
            for s in three_by_three:
                if s not in already_present:
                    original.append(s)
                    already_present.add(s)
            clash = 9 - len(original)
            all_clashes += clash
    return all_clashes

"""
    This function manages the crossing over of two individuals.
"""
def crossover_ind(individual1, individual2):
    offspring=copy.copy(answer)
    for z in range(0, 9):
        line_one=individual1[z, :]
        line_two=individual2[z, :]
        line_one=line_one.tolist()
        line_two=line_two.tolist()
        unit = 0
        for s in range(0, 9):
            if answer[(z, s)]==0:
                unit += 1
            else:
                line_one[s]=0
                line_two[s]=0
        crossover=random.randint(0, unit)


        merging=[]
        for j in range(0, 9):
            if line_one[j] !=0:
                if len(merging)<crossover:
                    merging.append(line_one[j])
                    line_two.remove(line_one[j])
        for c in line_two:
            if c != 0:
                merging.append(c)
        for d in range(0, 9):
            if offspring[(z, d)] == 0:
                offspring[z, d] = merging.pop(0)
    return offspring

"""
    This function allows for mutations to occur.
    The mutation rate specifies the rate of the individual mutations.
"""
def mutate_ind(individual):
    for m in range(0, 9):
        new_individuals = []
        for y in range(0, 9):
            if answer[(m, y)] == 0:
                new_individuals.append(individual[(m, y)])

        if random.random() < (MUTATION_RATE):
            random.shuffle(new_individuals)

        for h in range(0, 9):
            if answer[(m, h)] == 0:
                individual[(m, h)] = new_individuals.pop(0)
    return individual

### PARAMERS VALUES ###

NUMBER_GENERATION = 100
POPULATION_SIZE = 100
TRUNCATION_RATE = 0.5
MUTATION_RATE = 0.05
TERMINATION_GENERATION = 100

### EVOLVE! ###
# starts and finishes timer to calculate time taken for the program to find the fittest solution.
start_time=time.time()
print(evolve())
print("Overall, the program took: %s s" % (time.time() - start_time)+ " to terminate. Thank you!")