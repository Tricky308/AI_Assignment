from Graph_Creator import *
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import timeit



def create_individual():
    # Hard coding 50 number of vertices just as it is in Graph_Creator
    # 0 = Red, 1 = Green, 2 = Blue
    individual = []
    for i in range(50):
        individual.append(random.randint(0, 2))
    return individual


def create_population(n_pop):
    population = [create_individual() for _ in range(n_pop)]
    return population


def fitness_func(graph, individual):
    score_arr = [1 for _ in range(50)]
    for i in range(len(graph)):
        if individual[(graph[i])[0]] == individual[(graph[i])[1]]:
            score_arr[(graph[i])[0]] = 0
            score_arr[(graph[i])[1]] = 0

    score = 0
    for i in range(50):
        score += score_arr[i]

    return score


def best_fitness_func(graph, population):
    best_val, best_indi = fitness_func(graph, population[0]), population[0]
    for i in range(len(population)):
        temp = fitness_func(graph, population[i])
        if best_val < temp:
            best_val = temp
            best_indi = population[i]

    # score_arr = [fitness_func(graph, population[i]) for i in range(len(population))]
    return best_val, best_indi


def fitness_proportionate_selection(graph, population):
    # This selection method has been prescribed in the textbook
    # Normalizing fitness function to probabilities
    # Probability of Individial i being selected
    # = (fitness value of Individial i + 1) / (Sum of fitness values of all individuals + size of population)
    # Above normalization function selected to avoid zero probability of selection
    # for individuals with fitness value = 0

    selected = []
    pop_fitness = sum([fitness_func(graph, individual) for individual in population]) + len(population)
    indi_prob = [((fitness_func(graph, individual) + 1) / pop_fitness) for individual in population]

    for i in range(len(population)):
        indice = (np.random.choice(len(population), 1, replace=False, p=indi_prob))
        selected.append(population[indice[0]])

    return selected


def tournament_selection(graph, population):
    # Binary Tournament selection
    # Each outer loop adds N/2 individuals to the new_pop list hence the outer loop is run twice
    selected = []
    for _ in range(2):
        random.shuffle(population)
        for i in range(0, len(population) - 1, 2):
            if fitness_func(graph, population[i]) < fitness_func(graph, population[i + 1]):
                selected.append(population[i + 1])
            else:
                selected.append(population[i])
    return selected


def crossover1P(parent1, parent2, prob_cross):
    # One-point Crossover
    child1 = parent1.copy()
    child2 = parent2.copy()
    temp = random.uniform(0, 1)
    if temp <= prob_cross:
        point = random.randint(1, 48)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

    return child1, child2

def crossover2P(parent1, parent2, prob_cross):
    # Two-point Crossover
    child1 = parent1.copy()
    child2 = parent2.copy()
    temp = random.uniform(0, 1)
    if temp <= prob_cross:
        point1 = random.randint(1, 48)
        point2 = random.randint(1, 48)
        if point1 < point2:
            p1 = point1
            p2 = point2
        else:
            p1 = point2
            p2 = point1

        child1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
        child2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]

    return child1, child2

def uniform_crossover(parent1, parent2, prob_cross):
    #Uniform Crossover
    child1 = []
    child2 = []
    temp = random.uniform(0, 1)
    if temp <= prob_cross:
        for i in range(50):
            temp2 = random.randint(0, 1)
            if temp2 == 0:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])

    return child1, child2



def mutation(individual, prob_mut):
    temp = random.uniform(0, 1)
    if temp <= prob_mut:
        position = random.randint(0, 49)
        individual[position] = random.randint(0, 2)



def genetic_algorithm(s_id, c_id, graph, prob_mut, prob_cross, n_pop, n_gen):
    # s_id and c_id to choose the selection and crossover function
    GA_start = timeit.default_timer()
    best_fitness_list = []
    best_individual_list = []
    population = create_population(n_pop)
    best_fitness_value, best_individual = best_fitness_func(graph, population)
    gen = 0
    best_fitness_list.append(best_fitness_value)
    best_individual_list.append(best_individual)

    while best_fitness_value != 50 and gen != n_gen:

        GA_end = timeit.default_timer()
        if GA_end - GA_start > 44.5:
            break

        gen += 1
        # Selection
        if s_id == 1:
            population = tournament_selection(graph, population)
        else:
            population = fitness_proportionate_selection(graph, population)

        new_population = []
        random.shuffle(population)

        # Crossover
        for i in range(0, n_pop - 1, 2):
            if c_id == 1:
                child1, child2 = crossover1P(population[i], population[i + 1], prob_cross)
            elif c_id == 2:
                child1, child2 = crossover2P(population[i], population[i + 1], prob_cross)
            else:
                child1, child2 = uniform_crossover(population[i], population[i + 1], prob_cross)

            new_population.append(child1)
            new_population.append(child2)

        # Mutation
        for individual in new_population:
            mutation(individual, prob_mut)

        population = new_population
        best_fitness_value, best_individual = best_fitness_func(graph, population)
        best_fitness_list.append(best_fitness_value)
        best_individual_list.append(best_individual)

    return best_fitness_list, best_individual_list, gen

def main():

    start = timeit.default_timer()
    gc = Graph_Creator()
    # gc.CreateCSVFileForRandomGraph(500)
    edge_set_size_input = "200"
    graph = gc.ReadGraphfromCSVfile(edge_set_size_input)

    best_fitness_list, best_individual_list, gen = genetic_algorithm(1, 1, graph, 0.8, 0.2, 100, 100000)

    best_fitness = best_fitness_list[gen]
    best_individual = best_individual_list[gen]
    #gen_list = [i for i in range(len(best_fitness_list))]

    print("Roll no : 2019B3A70256G")
    print("Number of edges : ", end="")
    print(edge_set_size_input)
    print("Best state :")
    for i in range(49):
        print(i, end="")
        print(":", end="")
        if best_individual[i] == 0:
            print("R, ", end="")
        elif best_individual[i] == 1:
            print("G, ", end="")
        elif best_individual[i] == 2:
            print("B, ", end="")

        if i == 21 or i == 41:
            print()


    print("49:", end="")
    if best_individual[49] == 0:
        print("R")
    elif best_individual[49] == 1:
        print("G")
    elif best_individual[49] == 2:
        print("B")

    print("Fitness Value of best state : ", end="")
    print(best_fitness)
    print("Time taken : ", end="")
    end = timeit.default_timer()
    time_taken = end - start
    print("%.2f seconds" % time_taken)
    """
    stringtest = "BGGBRRRBGRBBGBRRRRGBRGRBRRGBRGGBGGBBRRGGGRBRBRGBBG"
    # 0 = Red, 1 = Green, 2 = Blue
    individual = []
    for i in stringtest:
        if i == "R":
            individual.append(0)
        elif i == "G":
            individual.append(1)
        elif i == "B":
            individual.append(2)

    print(fitness_func(graph, individual))
    """





if __name__ == '__main__':
    main()
